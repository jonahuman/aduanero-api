from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    documents = db.relationship('Document', foreign_keys='Document.user_id', backref='user', lazy=True, cascade='all, delete-orphan')
    customs_records = db.relationship('CustomsRecord', foreign_keys='CustomsRecord.user_id', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'nationality': self.nationality,
            'dateOfBirth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'phoneNumber': self.phone_number,
            'address': self.address,
            'isAdmin': self.is_admin,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'passport' or 'id_card'
    document_number = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'type': self.type,
            'documentNumber': self.document_number,
            'expirationDate': self.expiration_date.isoformat() if self.expiration_date else None,
            'fileUrl': self.file_url,
            'status': self.status,
            'uploadedAt': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'reviewedAt': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'notes': self.notes
        }

class CustomsRecord(db.Model):
    __tablename__ = 'customs_records'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pendiente', nullable=False)  # 'activo', 'inactivo', 'pendiente'
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        try:
            # Obtener datos del usuario de forma segura
            if self.user:
                user_data = {
                    'id': self.user.id,
                    'firstName': self.user.first_name,
                    'lastName': self.user.last_name,
                    'email': self.user.email,
                    'nationality': self.user.nationality,
                    'phoneNumber': self.user.phone_number,
                    'address': self.user.address
                }
                
                # Obtener documentos de forma segura
                documents_data = []
                try:
                    if hasattr(self.user, 'documents') and self.user.documents:
                        documents_data = [doc.to_dict() for doc in self.user.documents]
                except:
                    documents_data = []
            else:
                user_data = None
                documents_data = []
                
        except Exception as e:
            user_data = None
            documents_data = []
        
        return {
            'id': self.id,
            'userId': self.user_id,
            'user': user_data,
            'documents': documents_data,
            'status': self.status,
            'processedAt': self.processed_at.isoformat() if self.processed_at else None,
            'notes': self.notes
        }