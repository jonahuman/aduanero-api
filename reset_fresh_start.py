#!/usr/bin/env python3
"""
Script para empezar desde cero - Base de datos limpia
"""
import requests
import json

BASE_URL = "http://localhost:3000/api"

def reset_database():
    """Limpiar toda la base de datos"""
    try:
        print("Limpiando base de datos...")
        response = requests.delete(f"{BASE_URL}/setup/reset-database")
        
        if response.status_code == 200:
            print("Base de datos limpiada exitosamente")
            return True
        else:
            print(f"Error limpiando base de datos: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error conectando al servidor: {e}")
        return False

def create_admin():
    """Crear usuario administrador"""
    try:
        print("Creando usuario administrador...")
        data = {
            "email": "admin@aduana.gov",
            "password": "admin123",
            "firstName": "Administrador",
            "lastName": "Sistema",
            "nationality": "Nacional"
        }
        
        response = requests.post(f"{BASE_URL}/setup/admin", json=data)
        
        if response.status_code in [200, 201]:
            print("Usuario administrador creado")
            return True
        else:
            print(f"Error creando admin: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"Error creando admin: {e}")
        return False

def check_stats():
    """Verificar estadísticas iniciales"""
    try:
        # Primero hacer login
        login_data = {
            "email": "admin@aduana.gov",
            "password": "admin123"
        }
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if login_response.status_code != 200:
            print("No se pudo hacer login para verificar estadisticas")
            return False
        
        token = login_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Obtener estadísticas
        stats_response = requests.get(f"{BASE_URL}/customs/stats", headers=headers)
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print("Estadisticas iniciales:")
            print(f"   Usuarios: {stats['users']['total']}")
            print(f"   Documentos: {stats['documents']['total']}")
            print(f"   Registros aduaneros: {stats['customs_records']['total']}")
            return True
        else:
            print("No se pudieron obtener estadisticas")
            return False
            
    except Exception as e:
        print(f"Error verificando estadisticas: {e}")
        return False

def main():
    print("EMPEZAR DESDE CERO - Sistema Aduanero")
    print("=" * 50)
    
    # Paso 1: Limpiar base de datos
    if not reset_database():
        print("Asegurate de que el servidor este ejecutandose: python app.py")
        return
    
    # Paso 2: Crear admin
    if not create_admin():
        return
    
    # Paso 3: Verificar estadisticas
    check_stats()
    
    print("=" * 50)
    print("LISTO! Base de datos limpia y lista para usar")
    print("Credenciales admin: admin@aduana.gov / admin123")
    print("Frontend: http://localhost:5173")
    print("API: http://localhost:3000")
    print("")
    print("Ahora puedes:")
    print("   1. Hacer login en el frontend")
    print("   2. Registrar usuarios desde el flujo completo")
    print("   3. Ver los datos guardados en MySQL")

if __name__ == "__main__":
    main()