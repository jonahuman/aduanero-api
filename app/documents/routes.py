from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from app.models import Document, User
from app import db

documents_bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    try:
        user_id = request.form.get('userId')
        doc_type = request.form.get('type')
        document_number = request.form.get('documentNumber')
        expiration_date = request.form.get('expirationDate')
        
        if not all([user_id, doc_type, document_number, expiration_date]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        if doc_type not in ['passport', 'id_card']:
            return jsonify({'error': 'Tipo de documento inválido'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Tipo de archivo no permitido'}), 400
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        
        document = Document(
            user_id=user_id,
            type=doc_type,
            document_number=document_number,
            expiration_date=datetime.fromisoformat(expiration_date.replace('Z', '+00:00')).date(),
            file_url=f"/uploads/{unique_filename}",
            status='pending'
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'Documento subido exitosamente',
            'document': document.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': 'Error al subir documento'}), 500

@documents_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_documents(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        documents = Document.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener documentos'}), 500