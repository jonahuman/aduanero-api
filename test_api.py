#!/usr/bin/env python3
"""
Script para probar la API
"""
import requests
import json

BASE_URL = "http://localhost:3000/api"

def test_health():
    """Probar endpoint de salud"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        return False

def test_login():
    """Probar login con credenciales admin"""
    try:
        data = {
            "email": "admin@aduana.gov",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso")
            print(f"   Usuario: {result['user']['firstName']} {result['user']['lastName']}")
            return result['access_token']
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return None

def test_protected_endpoint(token):
    """Probar endpoint protegido"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/verify", headers=headers)
        
        if response.status_code == 200:
            print("✅ Endpoint protegido: OK")
            return True
        else:
            print(f"❌ Endpoint protegido falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en endpoint protegido: {e}")
        return False

def main():
    print("🧪 Probando API Sistema Aduanero...")
    print("-" * 40)
    
    # Test 1: Health check
    if not test_health():
        print("💡 Asegúrate de que el servidor esté ejecutándose")
        return
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("💡 Verifica las credenciales o la base de datos")
        return
    
    # Test 3: Endpoint protegido
    test_protected_endpoint(token)
    
    print("-" * 40)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    main()