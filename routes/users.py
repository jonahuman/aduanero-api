from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime
from models import User, db

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['firstName', 'lastName', 'nationality', 'dateOfBirth', 
                          'phoneNumber', 'address']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Verificar si el email ya existe (si se proporciona)
        if data.get('email'):
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        try:
            birth_date = datetime.fromisoformat(data['dateOfBirth'].replace('Z', '+00:00')).date()
        except (ValueError, KeyError):
            return jsonify({'error': 'Fecha de nacimiento inválida'}), 400
            
        user = User(
            email=data.get('email', f"user_{int(datetime.utcnow().timestamp())}@temp.com"),
            password_hash=generate_password_hash('temp123'),  # Password temporal
            first_name=data['firstName'],
            last_name=data['lastName'],
            nationality=data['nationality'],
            date_of_birth=birth_date,
            phone_number=data['phoneNumber'],
            address=data['address']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear usuario'}), 500

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = User.query
        
        # Aplicar filtro de búsqueda si se proporciona
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.first_name.ilike(search_filter),
                    User.last_name.ilike(search_filter),
                    User.email.ilike(search_filter),
                    User.nationality.ilike(search_filter)
                )
            )
        
        # Paginación
        users = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuarios'}), 500

@users_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuario'}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar campos si se proporcionan
        if data.get('firstName'):
            user.first_name = data['firstName']
        if data.get('lastName'):
            user.last_name = data['lastName']
        if data.get('nationality'):
            user.nationality = data['nationality']
        if data.get('phoneNumber'):
            user.phone_number = data['phoneNumber']
        if data.get('address'):
            user.address = data['address']
        if data.get('dateOfBirth'):
            user.date_of_birth = datetime.fromisoformat(data['dateOfBirth'].replace('Z', '+00:00')).date()
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar usuario'}), 500

@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar usuario'}), 500