#!/usr/bin/env python3
import os
import sys
from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, User, Document, CustomsRecord
from app import app

def init_database():
    """Inicializar base de datos con datos de prueba"""
    print("Inicializando base de datos...")
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        
        # Verificar si ya existe el usuario admin
        admin = User.query.filter_by(email='admin@aduana.gov').first()
        if not admin:
            print("Creando usuario administrador...")
            admin = User(
                email='admin@aduana.gov',
                password_hash=generate_password_hash('admin123'),
                first_name='Administrador',
                last_name='Sistema',
                nationality='Nacional',
                date_of_birth='1990-01-01',
                phone_number='+1234567890',
                address='Oficina Central de Aduanas',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario administrador creado")
        else:
            print("✅ Usuario administrador ya existe")
        
        print("✅ Base de datos inicializada correctamente")

def run_server():
    """Ejecutar servidor Flask"""
    print("Iniciando servidor Flask en puerto 5000...")
    print("API disponible en: http://localhost:5000")
    print("Endpoints principales:")
    print("  - POST /api/auth/login")
    print("  - GET  /api/users/")
    print("  - POST /api/documents/upload")
    print("  - GET  /api/customs/records")
    print("\nCredenciales de prueba:")
    print("  Email: admin@aduana.gov")
    print("  Password: admin123")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    try:
        init_database()
        run_server()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)