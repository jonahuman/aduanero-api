from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuración
    from config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    # Crear directorio de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registrar blueprints
    from app.auth.routes import auth_bp
    from app.users.routes import users_bp
    from app.documents.routes import documents_bp
    from app.customs.routes import customs_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(documents_bp, url_prefix='/api/documents')
    app.register_blueprint(customs_bp, url_prefix='/api/customs')
    
    # Ruta de salud
    @app.route('/api/health')
    def health():
        return {'status': 'ok'}
    
    return app