import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print("🚀 Iniciando servidor API Aduanero...")
    print("🌐 Servidor disponible en: http://localhost:3000")
    print("📋 Credenciales admin: admin@aduana.gov / admin123")
    
    # Ejecutar app.py directamente
    exec(open('app.py').read())