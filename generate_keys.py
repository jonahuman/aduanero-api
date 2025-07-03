import secrets
import os

def generate_secure_keys():
    """Generar claves seguras para Flask y JWT"""
    
    # Generar claves aleatorias seguras
    secret_key = secrets.token_urlsafe(32)
    jwt_secret_key = secrets.token_urlsafe(32)
    
    print("Claves generadas:")
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret_key}")
    
    # Leer archivo .env actual
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    
    # Actualizar o agregar las claves
    updated_lines = []
    secret_updated = False
    jwt_updated = False
    
    for line in lines:
        if line.startswith('SECRET_KEY='):
            updated_lines.append(f'SECRET_KEY={secret_key}\n')
            secret_updated = True
        elif line.startswith('JWT_SECRET_KEY='):
            updated_lines.append(f'JWT_SECRET_KEY={jwt_secret_key}\n')
            jwt_updated = True
        else:
            updated_lines.append(line)
    
    # Agregar claves si no existían
    if not secret_updated:
        updated_lines.append(f'SECRET_KEY={secret_key}\n')
    if not jwt_updated:
        updated_lines.append(f'JWT_SECRET_KEY={jwt_secret_key}\n')
    
    # Escribir archivo .env actualizado
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    print("Archivo .env actualizado con claves seguras")

if __name__ == '__main__':
    generate_secure_keys()