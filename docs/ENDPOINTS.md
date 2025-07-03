# API Endpoints - Sistema Aduanero

**Base URL:** `http://localhost:3000/api`

## 🔐 Autenticación

### POST /auth/login
Iniciar sesión de usuario

**Body (raw JSON):**
```json
{
  "email": "admin@aduana.gov",
  "password": "admin123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "uuid",
    "email": "admin@aduana.gov",
    "firstName": "Administrador",
    "lastName": "Sistema",
    "isAdmin": true
  }
}
```

### GET /auth/verify
Verificar token JWT (requiere Authorization header)
```json
// Headers
Authorization: Bearer <token>

// Response 200
{
  "user": {
    "id": "uuid",
    "email": "admin@aduana.gov",
    "firstName": "Administrador",
    "lastName": "Sistema"
  }
}
```

### POST /auth/logout
Cerrar sesión (requiere Authorization header)
```json
// Response 200
{
  "message": "Sesión cerrada exitosamente"
}
```

## 👥 Usuarios

### POST /users/
Crear nuevo usuario (requiere autenticación)

**Body (raw JSON):**
```json
{
  "firstName": "Juan",
  "lastName": "Pérez",
  "nationality": "Mexicano",
  "dateOfBirth": "1990-05-15",
  "phoneNumber": "+52123456789",
  "address": "Calle Principal 123",
  "email": "juan@email.com"
}
```

**Response 201:**
```json
{
  "message": "Usuario creado exitosamente",
  "user": {
    "id": "uuid",
    "firstName": "Juan",
    "lastName": "Pérez",
    "nationality": "Mexicano",
    "dateOfBirth": "1990-05-15",
    "phoneNumber": "+52123456789",
    "address": "Calle Principal 123"
  }
}
```

### GET /users/
Listar usuarios con paginación (requiere autenticación)
```json
// Query params: ?page=1&per_page=10&search=juan

// Response 200
{
  "users": [...],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

### GET /users/{id}
Obtener usuario específico
```json
// Response 200
{
  "user": {
    "id": "uuid",
    "firstName": "Juan",
    "lastName": "Pérez"
  }
}
```

### PUT /users/{id}
Actualizar usuario

**Body (raw JSON):**
```json
{
  "firstName": "Juan Carlos",
  "phoneNumber": "+52987654321"
}
```

**Response 200:**
```json
{
  "message": "Usuario actualizado exitosamente",
  "user": {...}
}
```

### DELETE /users/{id}
Eliminar usuario (solo admin)
```json
// Response 200
{
  "message": "Usuario eliminado exitosamente"
}
```

## 📄 Documentos

### POST /documents/upload
Subir documento (requiere autenticación)
```json
// Form Data
userId: "uuid"
type: "passport" | "id_card"
documentNumber: "A1234567"
expirationDate: "2025-12-31"
file: <archivo>

// Response 201
{
  "message": "Documento subido exitosamente",
  "document": {
    "id": "uuid",
    "type": "passport",
    "documentNumber": "A1234567",
    "status": "pending"
  }
}
```

### GET /documents/user/{userId}
Obtener documentos de un usuario
```json
// Response 200
{
  "documents": [
    {
      "id": "uuid",
      "type": "passport",
      "documentNumber": "A1234567",
      "status": "pending",
      "fileUrl": "/uploads/filename.pdf"
    }
  ]
}
```

### PUT /documents/{id}/review
Revisar documento (solo admin)

**Body (raw JSON):**
```json
{
  "status": "approved",
  "notes": "Documento válido"
}
```

**Response 200:**
```json
{
  "message": "Documento revisado exitosamente",
  "document": {...}
}
```

### GET /documents/
Listar todos los documentos (solo admin)
```json
// Query params: ?page=1&per_page=10&status=pending

// Response 200
{
  "documents": [...],
  "total": 50,
  "pages": 5,
  "current_page": 1
}
```

### DELETE /documents/{id}
Eliminar documento
```json
// Response 200
{
  "message": "Documento eliminado exitosamente"
}
```

## 🏛️ Registros Aduaneros

### POST /customs/records
Crear registro aduanero (solo admin)

**Body (raw JSON):**
```json
{
  "userId": "uuid",
  "status": "activo",
  "notes": "Registro aprobado"
}
```

**Response 201:**
```json
{
  "message": "Registro aduanero creado exitosamente",
  "record": {
    "id": "uuid",
    "userId": "uuid",
    "status": "activo",
    "processedAt": "2024-01-15T10:30:00Z"
  }
}
```

### GET /customs/records
Listar registros aduaneros
```json
// Query params: ?page=1&per_page=10&status=activo&search=juan

// Response 200
{
  "records": [
    {
      "id": "uuid",
      "userId": "uuid",
      "user": {...},
      "documents": [...],
      "status": "activo",
      "processedAt": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 30,
  "pages": 3,
  "current_page": 1
}
```

### GET /customs/records/{id}
Obtener registro específico
```json
// Response 200
{
  "record": {
    "id": "uuid",
    "user": {...},
    "documents": [...],
    "status": "activo"
  }
}
```

### PUT /customs/records/{id}
Actualizar registro (solo admin)

**Body (raw JSON):**
```json
{
  "status": "inactivo",
  "notes": "Registro suspendido"
}
```

**Response 200:**
```json
{
  "message": "Registro actualizado exitosamente",
  "record": {...}
}
```

### DELETE /customs/records/{id}
Eliminar registro (solo admin)
```json
// Response 200
{
  "message": "Registro eliminado exitosamente"
}
```

### GET /customs/stats
Obtener estadísticas (solo admin)
```json
// Response 200
{
  "users": {
    "total": 100
  },
  "documents": {
    "total": 250,
    "approved": 200,
    "pending": 30,
    "rejected": 20
  },
  "customs_records": {
    "total": 80,
    "active": 60,
    "inactive": 10,
    "pending": 10
  }
}
```

### POST /customs/process-user
Procesar usuario completo (crear usuario + registro aduanero)

**Body (raw JSON):**
```json
{
  "userData": {
    "firstName": "María",
    "lastName": "González",
    "nationality": "Mexicana",
    "dateOfBirth": "1985-03-20",
    "phoneNumber": "+52555123456",
    "address": "Av. Reforma 456"
  }
}
```

**Response 201:**
```json
{
  "message": "Usuario procesado exitosamente",
  "user": {...},
  "customs_record": {...}
}
```

## 🏥 Salud y Configuración

### GET /health
Verificar estado del servidor
```json
// Response 200
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### GET /setup/check
Verificar configuración del sistema
```json
// Response 200
{
  "database_connected": true,
  "admin_exists": true,
  "setup_complete": true
}
```

### POST /setup/admin
Crear usuario administrador con credenciales personalizadas (solo desarrollo)

**Body (raw JSON):**
```json
{
  "email": "admin@aduana.gov",
  "password": "admin123",
  "firstName": "Administrador",
  "lastName": "Sistema",
  "nationality": "Nacional",
  "phoneNumber": "+1234567890",
  "address": "Oficina Central de Aduanas"
}
```

**Campos requeridos:** `email`, `password`
**Campos opcionales:** `firstName`, `lastName`, `nationality`, `phoneNumber`, `address`

**Response 201:**
```json
{
  "message": "Admin creado exitosamente"
}
```

**Response 200 (si ya existe):**
```json
{
  "message": "Admin ya existe"
}
```

**Response 400 (datos faltantes):**
```json
{
  "error": "Email y contraseña son requeridos"
}
```

### DELETE /setup/delete-admin
Eliminar usuario administrador (limpieza de base de datos)

**Body (raw JSON):**
```json
{
  "email": "admin@aduana.gov"
}
```

**Response 200:**
```json
{
  "message": "Admin eliminado exitosamente"
}
```

**Response 404 (no encontrado):**
```json
{
  "message": "Admin no encontrado"
}
```

**Response 400 (email faltante):**
```json
{
  "error": "Email es requerido"
}
```

## 🔒 Autenticación

Todos los endpoints (excepto `/auth/login` y `/health`) requieren el header:
```
Authorization: Bearer <jwt_token>
```

## 📝 Códigos de Estado

- `200` - Éxito
- `201` - Creado
- `400` - Solicitud inválida
- `401` - No autorizado
- `403` - Prohibido (permisos insuficientes)
- `404` - No encontrado
- `500` - Error interno del servidor

## 🗄️ Base de Datos

Los datos se guardan automáticamente en MySQL:
- **Base de datos:** `aduanero_bbdd`
- **Tablas:** `users`, `documents`, `customs_records`
- **Conexión:** `mysql+pymysql://root:flerr@localhost/aduanero_bbdd`