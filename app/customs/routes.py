from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models import CustomsRecord, User, Document
from app import db

customs_bp = Blueprint('customs', __name__)

@customs_bp.route('/records', methods=['GET'])
@jwt_required()
def get_customs_records():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        search = request.args.get('search', '')
        
        query = CustomsRecord.query.join(User)
        
        if status_filter and status_filter != 'todos':
            if status_filter in ['activo', 'inactivo', 'pendiente']:
                query = query.filter(CustomsRecord.status == status_filter)
        
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
        
        query = query.order_by(CustomsRecord.processed_at.desc())
        
        records = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'records': [record.to_dict() for record in records.items],
            'total': records.total,
            'pages': records.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener registros aduaneros'}), 500

@customs_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_customs_stats():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Permisos insuficientes'}), 403
        
        total_users = User.query.count()
        total_documents = Document.query.count()
        approved_documents = Document.query.filter_by(status='approved').count()
        pending_documents = Document.query.filter_by(status='pending').count()
        rejected_documents = Document.query.filter_by(status='rejected').count()
        
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
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        user_data = data.get('userData')
        documents_data = data.get('documents', [])
        
        if not user_data:
            return jsonify({'error': 'Datos de usuario requeridos'}), 400
        
        user = User(
            email=user_data.get('email', f"user_{datetime.utcnow().timestamp()}@temp.com"),
            password_hash='temp_hash',
            first_name=user_data['firstName'],
            last_name=user_data['lastName'],
            nationality=user_data['nationality'],
            date_of_birth=datetime.fromisoformat(user_data['dateOfBirth'].replace('Z', '+00:00')).date(),
            phone_number=user_data['phoneNumber'],
            address=user_data['address']
        )
        
        db.session.add(user)
        db.session.flush()
        
        customs_record = CustomsRecord(
            user_id=user.id,
            status='pendiente',
            notes='Registro creado automáticamente tras completar datos personales y documentos',
            processed_by=current_user_id
        )
        
        db.session.add(customs_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario procesado exitosamente',
            'user': user.to_dict(),
            'customs_record': customs_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al procesar usuario'}), 500