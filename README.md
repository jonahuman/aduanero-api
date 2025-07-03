# API Sistema Aduanero

API REST desarrollada en Flask para el sistema de gestión aduanera.

## 🚀 Características

- 🔐 Autenticación JWT
- 👥 Gestión de usuarios
- 📄 Subida y gestión de documentos
- 🏦 Registros aduaneros
- 📊 Base de datos MySQL
- 🌐 CORS habilitado para frontend React
- ⚙️ Endpoints de configuración

## 🛠️ Instalación

1. **Clonar repositorio:**
```bash
git clone <repository-url>
cd aduanero-api
```

2. **Crear entorno virtual:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
copy .env.example .env
# Editar .env con tus configuraciones
```

5. **Generar claves de seguridad:**
```bash
python generate_keys.py
```

6. **Inicializar base de datos:**
```bash
python init_db.py
```

7. **Ejecutar la aplicación:**
```bash
python app.py
```

## Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/verify` - Verificar token
- `POST /api/auth/logout` - Cerrar sesión

### Usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/` - Listar usuarios
- `GET /api/users/<id>` - Obtener usuario
- `PUT /api/users/<id>` - Actualizar usuario
- `DELETE /api/users/<id>` - Eliminar usuario

### Documentos
- `POST /api/documents/upload` - Subir documento
- `GET /api/documents/user/<user_id>` - Documentos de usuario
- `PUT /api/documents/<id>/review` - Revisar documento
- `GET /api/documents/` - Listar todos los documentos
- `DELETE /api/documents/<id>` - Eliminar documento

### Registros Aduaneros
- `POST /api/customs/records` - Crear registro
- `GET /api/customs/records` - Listar registros
- `GET /api/customs/records/<id>` - Obtener registro
- `PUT /api/customs/records/<id>` - Actualizar registro
- `DELETE /api/customs/records/<id>` - Eliminar registro
- `GET /api/customs/stats` - Estadísticas
- `POST /api/customs/process-user` - Procesar usuario completo

## 🔑 Credenciales

Ver `docs/CREDENCIALES.md` para credenciales completas.

**Por defecto:**
- Email: admin@aduana.gov
- Password: admin123

**Crear admin personalizado:**
```bash
POST /api/setup/admin
```

## 📁 Estructura del proyecto

```
aduanero-api/
├── app.py              # Aplicación principal
├── models.py           # Modelos de base de datos
├── config.py           # Configuraciones
├── requirements.txt    # Dependencias
├── docs/              # Documentación
│   ├── ENDPOINTS.md   # API endpoints
│   └── CREDENCIALES.md # Credenciales
├── routes/            # Rutas de la API
│   ├── auth.py        # Autenticación
│   ├── users.py       # Usuarios
│   ├── documents.py   # Documentos
│   └── customs.py     # Registros aduaneros
├── mysql/             # Scripts SQL
├── uploads/           # Archivos subidos
└── scripts/           # Scripts de utilidad
```

## 📚 Documentación

- **API Endpoints:** `docs/ENDPOINTS.md`
- **Credenciales:** `docs/CREDENCIALES.md`
- **Base de datos:** `mysql/aduanero_bbdd.sql`

## 🛠️ Scripts de Utilidad

- `generate_keys.py` - Generar claves de seguridad
- `init_db.py` - Inicializar base de datos
- `test_api.py` - Probar endpoints
- `start.sh` - Iniciar servidor (Linux/Mac)
- `start_server.bat` - Iniciar servidor (Windows)

## 🌐 Puerto

La API corre en `http://localhost:3000`

## 📊 Base de Datos

- **Motor:** MySQL
- **Base de datos:** `aduanero_bbdd`
- **Configuración:** Ver `.env.example`