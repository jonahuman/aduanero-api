import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Importar desde app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    # Importar después de cargar variables de entorno
    from app import app, db
    from models import User
    from werkzeug.security import generate_password_hash
    from datetime import datetime
    
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        
        # Crear admin si no existe
        admin = User.query.filter_by(email='admin@aduana.gov').first()
        if not admin:
            admin = User(
                email='admin@aduana.gov',
                password_hash=generate_password_hash('admin123'),
                first_name='Administrador',
                last_name='Sistema',
                nationality='Nacional',
                date_of_birth=datetime(1990, 1, 1).date(),
                phone_number='+1234567890',
                address='Oficina Central de Aduanas',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado")
        else:
            print("Usuario admin ya existe")
        
        print("Base de datos lista!")

if __name__ == '__main__':
    init_database()