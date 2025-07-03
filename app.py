from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Usar configuración desde config.py
from config import config
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Inicializar extensiones
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

# Crear directorio de uploads si no existe
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except Exception as e:
    print(f"Error creando directorio uploads: {e}")

# Importar y configurar base de datos
from models import db, User, Document, CustomsRecord
db.init_app(app)

# Importar rutas
from routes.auth import auth_bp
from routes.users import users_bp
from routes.documents import documents_bp
from routes.customs import customs_bp

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(documents_bp, url_prefix='/api/documents')
app.register_blueprint(customs_bp, url_prefix='/api/customs')

# Endpoint público para crear admin (solo desarrollo)
@app.route('/api/setup/admin', methods=['POST'])
def create_admin_endpoint():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        admin = User.query.filter_by(email=data['email']).first()
        if admin:
            return jsonify({'message': 'Admin ya existe'}), 200
        
        admin = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            first_name=data.get('firstName', 'Administrador'),
            last_name=data.get('lastName', 'Sistema'),
            nationality=data.get('nationality', 'Nacional'),
            date_of_birth=datetime(1990, 1, 1).date(),
            phone_number=data.get('phoneNumber', '+1234567890'),
            address=data.get('address', 'Oficina Central de Aduanas'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({'message': 'Admin creado exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

# Endpoint para servir archivos subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir archivos subidos"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404

@app.route('/api/activity/summary', methods=['GET'])
@jwt_required()
def get_activity_summary():
    """Obtener resumen de actividad del día"""
    try:
        from datetime import date
        today = date.today()
        
        # Actividad del día
        users_today = User.query.filter(
            User.created_at >= today,
            User.is_admin == False
        ).count()
        
        docs_today = Document.query.filter(
            Document.uploaded_at >= today
        ).count()
        
        records_today = CustomsRecord.query.filter(
            CustomsRecord.processed_at >= today
        ).count()
        
        return jsonify({
            'today': {
                'users': users_today,
                'documents': docs_today,
                'records': records_today
            },
            'date': today.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/setup/check', methods=['GET'])
def setup_check():
    try:
        admin_exists = User.query.filter_by(email='admin@aduana.gov').first() is not None
        return jsonify({
            'database_connected': True,
            'admin_exists': admin_exists,
            'setup_complete': admin_exists
        })
    except Exception as e:
        return jsonify({
            'database_connected': False,
            'error': str(e)
        }), 500

@app.route('/api/setup/delete-admin', methods=['DELETE'])
def delete_admin_endpoint():
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email es requerido'}), 400
        
        admin = User.query.filter_by(email=data['email'], is_admin=True).first()
        if not admin:
            return jsonify({'message': 'Admin no encontrado'}), 404
        
        db.session.delete(admin)
        db.session.commit()
        
        return jsonify({'message': 'Admin eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/setup/reset-database', methods=['DELETE'])
def reset_database():
    """Limpiar toda la base de datos para empezar desde cero"""
    try:
        # Eliminar todos los registros en orden correcto (por las foreign keys)
        CustomsRecord.query.delete()
        Document.query.delete()
        User.query.delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Base de datos limpiada exitosamente',
            'status': 'ready_for_fresh_start'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/activity/recent', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Obtener actividad reciente del sistema"""
    try:
        limit = request.args.get('limit', 10, type=int)
        activities = []
        
        # Documentos recientes (aprobados, rechazados, pendientes)
        recent_docs = Document.query.order_by(Document.uploaded_at.desc()).limit(limit).all()
        for doc in recent_docs:
            user_name = f"{doc.user.first_name} {doc.user.last_name}" if doc.user else "Usuario desconocido"
            
            if doc.status == 'approved':
                action = 'Documento aprobado'
                activity_type = 'success'
            elif doc.status == 'rejected':
                action = 'Documento rechazado'
                activity_type = 'error'
            else:
                action = 'Documento subido'
                activity_type = 'info'
            
            activities.append({
                'id': doc.id,
                'action': action,
                'user': user_name,
                'time': doc.uploaded_at.isoformat() if doc.uploaded_at else None,
                'type': activity_type,
                'details': f"Tipo: {doc.type}, Número: {doc.document_number}"
            })
        
        # Usuarios recientes
        recent_users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).limit(limit).all()
        for user in recent_users:
            activities.append({
                'id': user.id,
                'action': 'Nuevo usuario registrado',
                'user': f"{user.first_name} {user.last_name}",
                'time': user.created_at.isoformat() if user.created_at else None,
                'type': 'info',
                'details': f"Nacionalidad: {user.nationality}"
            })
        
        # Registros aduaneros recientes
        recent_records = CustomsRecord.query.order_by(CustomsRecord.processed_at.desc()).limit(limit).all()
        for record in recent_records:
            user_name = f"{record.user.first_name} {record.user.last_name}" if record.user else "Usuario desconocido"
            
            if record.status == 'activo':
                action = 'Registro aduanero activado'
                activity_type = 'success'
            elif record.status == 'inactivo':
                action = 'Registro aduanero desactivado'
                activity_type = 'error'
            else:
                action = 'Registro aduanero creado'
                activity_type = 'info'
            
            activities.append({
                'id': record.id,
                'action': action,
                'user': user_name,
                'time': record.processed_at.isoformat() if record.processed_at else None,
                'type': activity_type,
                'details': f"Estado: {record.status}"
            })
        
        # Ordenar por tiempo (más recientes primero) y limitar
        activities.sort(key=lambda x: x['time'] or '', reverse=True)
        activities = activities[:limit]
        
        return jsonify({
            'activities': activities,
            'total': len(activities)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

def create_admin_user():
    """Crear usuario admin por defecto"""
    try:
        admin = User.query.filter_by(email='admin@aduana.gov').first()
        if not admin:
            admin = User(
                email='admin@aduana.gov',
                password_hash=generate_password_hash('admin123'),
                first_name='Administrador',
                last_name='Sistema',
                nationality='Nacional',
                date_of_birth=datetime(1990, 1, 1),
                phone_number='+1234567890',
                address='Oficina Central de Aduanas',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado exitosamente")
    except Exception as e:
        print(f"Error creando usuario admin: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            create_admin_user()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=3000)