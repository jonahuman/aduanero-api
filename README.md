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

## 📝 **Empezar desde Cero (Base de Datos Limpia)**

### 🚨 **IMPORTANTE: Servidor debe estar ejecutándose**

Antes de limpiar la base de datos, **SIEMPRE** asegúrate de que el servidor API esté corriendo:

```bash
# Terminal 1 - Iniciar servidor API
python app.py
```

**Verificar que el servidor esté funcionando:**
- Deberías ver: `Running on http://0.0.0.0:3000`
- Probar en navegador: `http://localhost:3000/api/health`
- Respuesta esperada: `{"status": "ok", "timestamp": "..."}`

### 🧹 **Limpiar y Resetear Base de Datos**

**Opción 1 - Script Automático (Recomendado):**
```bash
# Terminal 2 - Con servidor corriendo en Terminal 1
python reset_fresh_start.py
```

**Opción 2 - Manual:**
```bash
# 1. Limpiar base de datos
curl -X DELETE http://localhost:3000/api/setup/reset-database

# 2. Crear admin
curl -X POST http://localhost:3000/api/setup/admin \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@aduana.gov","password":"admin123"}'
```

### ⚠️ **Errores Comunes y Soluciones**

**Error: "No se puede establecer una conexión"**
```
Error conectando al servidor: HTTPConnectionPool(host='localhost', port=3000)
```

**Solución:**
1. Verificar que el servidor esté corriendo: `python app.py`
2. Esperar a ver el mensaje: `Running on http://0.0.0.0:3000`
3. Probar health check: `http://localhost:3000/api/health`
4. Ejecutar reset: `python reset_fresh_start.py`

**Error: "Puerto ya en uso"**
```
Address already in use
```

**Solución:**
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### 📊 **Verificar Estado Inicial**

Después del reset, las estadísticas deberían mostrar:
- **Usuarios Registrados:** 0 (admin no cuenta)
- **Documentos Procesados:** 0
- **Pendientes:** 0
- **Rechazados:** 0

### 🔄 **Flujo Completo de Reset**

```bash
# Paso 1: Iniciar servidor
python app.py
# Esperar mensaje: "Running on http://0.0.0.0:3000"

# Paso 2: En otra terminal, resetear
python reset_fresh_start.py

# Paso 3: Verificar en navegador
# http://localhost:3000/api/health

# Paso 4: Login en frontend
# http://localhost:5173
# Credenciales: admin@aduana.gov / admin123
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

**Administrador (después del reset):**
- Email: admin@aduana.gov
- Password: admin123

**Crear admin personalizado:**
```bash
POST /api/setup/admin
```

**⚠️ Nota:** El administrador NO cuenta como usuario en las estadísticas.

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