from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy.orm import joinedload
from models import CustomsRecord, User, Document, db

customs_bp = Blueprint('customs', __name__)

@customs_bp.route('/records', methods=['POST'])
@jwt_required()
def create_customs_record():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        data = request.get_json()
        user_id = data.get('userId')
        status = data.get('status', 'pendiente')
        notes = data.get('notes', '')
        
        if not user_id:
            return jsonify({'error': 'ID de usuario es requerido'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if status not in ['activo', 'inactivo', 'pendiente']:
            return jsonify({'error': 'Estado inválido'}), 400
        
        # Verificar si ya existe un registro para este usuario
        existing_record = CustomsRecord.query.filter_by(user_id=user_id).first()
        if existing_record:
            return jsonify({'error': 'Ya existe un registro aduanero para este usuario'}), 400
        
        record = CustomsRecord(
            user_id=user_id,
            status=status,
            notes=notes,
            processed_by=current_user_id
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': 'Registro aduanero creado exitosamente',
            'record': record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear registro aduanero'}), 500

@customs_bp.route('/records', methods=['GET'])
@jwt_required()
def get_customs_records():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        search = request.args.get('search', '')
        
        # Usar eager loading para evitar problemas de lazy loading
        query = CustomsRecord.query.options(
            db.joinedload(CustomsRecord.user).joinedload(User.documents)
        )
        
        # Aplicar filtro de estado
        if status_filter and status_filter != 'todos':
            if status_filter in ['activo', 'inactivo', 'pendiente']:
                query = query.filter(CustomsRecord.status == status_filter)
        
        # Aplicar filtro de búsqueda
        if search:
            search_filter = f"%{search}%"
            query = query.join(User).filter(
                db.or_(
                    User.first_name.ilike(search_filter),
                    User.last_name.ilike(search_filter),
                    User.email.ilike(search_filter),
                    User.nationality.ilike(search_filter)
                )
            )
        
        # Ordenar por fecha de procesamiento (más recientes primero)
        query = query.order_by(CustomsRecord.processed_at.desc())
        
        records = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Convertir a dict de forma segura
        records_data = []
        for record in records.items:
            try:
                records_data.append(record.to_dict())
            except Exception as e:
                # Si falla to_dict(), crear un dict básico
                records_data.append({
                    'id': record.id,
                    'userId': record.user_id,
                    'user': {
                        'firstName': record.user.first_name if record.user else 'Desconocido',
                        'lastName': record.user.last_name if record.user else '',
                        'email': record.user.email if record.user else '',
                        'nationality': record.user.nationality if record.user else ''
                    } if record.user else None,
                    'documents': [],
                    'status': record.status,
                    'processedAt': record.processed_at.isoformat() if record.processed_at else None,
                    'notes': record.notes
                })
        
        return jsonify({
            'records': records_data,
            'total': records.total,
            'pages': records.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        print(f"Error en get_customs_records: {e}")  # Para debug
        return jsonify({'error': 'Error al obtener registros aduaneros'}), 500

@customs_bp.route('/records/<record_id>', methods=['GET'])
@jwt_required()
def get_customs_record(record_id):
    try:
        record = CustomsRecord.query.get(record_id)
        
        if not record:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        return jsonify({'record': record.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener registro'}), 500

@customs_bp.route('/records/<record_id>', methods=['PUT'])
@jwt_required()
def update_customs_record(record_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        record = CustomsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        data = request.get_json()
        
        if data.get('status') and data['status'] in ['activo', 'inactivo', 'pendiente']:
            record.status = data['status']
        
        if data.get('notes') is not None:
            record.notes = data['notes']
        
        record.updated_at = datetime.utcnow()
        record.processed_by = current_user_id
        
        db.session.commit()
        
        return jsonify({
            'message': 'Registro actualizado exitosamente',
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar registro'}), 500

@customs_bp.route('/records/<record_id>/toggle-status', methods=['PUT'])
@jwt_required()
def toggle_record_status(record_id):
    """Cambiar estado entre activo/inactivo"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        record = CustomsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        # Cambiar estado
        if record.status == 'activo':
            record.status = 'inactivo'
            message = 'Registro desactivado'
        elif record.status == 'inactivo':
            record.status = 'activo'
            message = 'Registro activado'
        else:  # pendiente
            record.status = 'activo'
            message = 'Registro activado'
        
        record.updated_at = datetime.utcnow()
        record.processed_by = current_user_id
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'record': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al cambiar estado'}), 500

@customs_bp.route('/records/<record_id>', methods=['DELETE'])
@jwt_required()
def delete_customs_record(record_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        record = CustomsRecord.query.get(record_id)
        if not record:
            return jsonify({'error': 'Registro no encontrado'}), 404
        
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message': 'Registro eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar registro'}), 500

@customs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_customs_stats():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        # Estadísticas de usuarios (sin contar admins)
        total_users = User.query.filter_by(is_admin=False).count()
        
        # Estadísticas de documentos
        total_documents = Document.query.count()
        approved_documents = Document.query.filter_by(status='approved').count()
        pending_documents = Document.query.filter_by(status='pending').count()
        rejected_documents = Document.query.filter_by(status='rejected').count()
        
        # Estadísticas de registros aduaneros
        total_records = CustomsRecord.query.count()
        active_records = CustomsRecord.query.filter_by(status='activo').count()
        inactive_records = CustomsRecord.query.filter_by(status='inactivo').count()
        pending_records = CustomsRecord.query.filter_by(status='pendiente').count()
        
        return jsonify({
            'users': {
                'total': total_users
            },
            'documents': {
                'total': total_documents,
                'approved': approved_documents,
                'pending': pending_documents,
                'rejected': rejected_documents
            },
            'customs_records': {
                'total': total_records,
                'active': active_records,
                'inactive': inactive_records,
                'pending': pending_records
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener estadísticas'}), 500

@customs_bp.route('/process-user', methods=['POST'])
@jwt_required()
def process_user_registration():
    """
    Procesa el registro completo de un usuario (datos personales + documentos)
    y crea automáticamente el registro aduanero
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Obtener datos
        user_data = data.get('userData')
        
        if not user_data:
            return jsonify({'error': 'Datos de usuario requeridos'}), 400
        
        # Buscar si el usuario ya existe (por el ID que viene del frontend)
        user_id = user_data.get('userId')
        if user_id:
            user = User.query.get(user_id)
            if user:
                # Verificar si ya tiene registro aduanero
                existing_record = CustomsRecord.query.filter_by(user_id=user.id).first()
                if not existing_record:
                    # Crear registro aduanero
                    customs_record = CustomsRecord(
                        user_id=user.id,
                        status='pendiente',
                        notes='Registro creado tras completar el flujo de documentos',
                        processed_by=current_user_id
                    )
                    
                    db.session.add(customs_record)
                    db.session.commit()
                    
                    return jsonify({
                        'message': 'Usuario procesado exitosamente',
                        'user': user.to_dict(),
                        'customs_record': customs_record.to_dict()
                    }), 201
                else:
                    return jsonify({
                        'message': 'Usuario ya tiene registro aduanero',
                        'user': user.to_dict(),
                        'customs_record': existing_record.to_dict()
                    }), 200
        
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al procesar usuario'}), 500