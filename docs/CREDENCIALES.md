# Credenciales del Sistema Aduanero

## 🔑 Credenciales por Defecto

### Administrador
- **Email:** `admin@aduana.gov`
- **Password:** `admin123`
- **Permisos:** Acceso completo al sistema

### Usuario de Prueba
- **Email:** `usuario@test.com`
- **Password:** `test123`
- **Permisos:** Usuario estándar

## 💡 Ideas para Credenciales Personalizadas

### Administrador Chile
- **Email:** `nuevoadmin@aduana.cl`
- **Password:** `AdministradorChile123`
- **País:** Chile

### Otros Ejemplos
- **Email:** `admin@customs.mx`
- **Password:** `MexicoAdmin2024`

- **Email:** `supervisor@aduana.pe`
- **Password:** `PeruSupervisor456`

### Crear Admin Personalizado
**POST** `http://localhost:3000/api/setup/admin`
```json
{
  "email": "nuevoadmin@aduana.cl",
  "password": "AdministradorChile123",
  "firstName": "Administrador",
  "lastName": "Chile",
  "nationality": "Chileno",
  "phoneNumber": "+56912345678",
  "address": "Oficina Aduanas Chile"
}
```

## 🚀 Configuración Inicial

Si las credenciales no funcionan, ejecuta estos comandos:

1. **Inicializar base de datos:**
```bash
python init_db.py
```

2. **Iniciar API:**
```bash
python app.py
```

3. **Probar credenciales:**
```bash
python test_api.py
```

## 🌐 Endpoint de Login

**URL:** `POST http://localhost:3000/api/auth/login`

**Request (Credenciales por defecto):**
```json
{
  "email": "admin@aduana.gov",
  "password": "admin123"
}
```

**Request (Credenciales Chile):**
```json
{
  "email": "nuevoadmin@aduana.cl",
  "password": "AdministradorChile123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": "uuid",
    "email": "nuevoadmin@aduana.cl",
    "firstName": "Administrador",
    "lastName": "Chile",
    "isAdmin": true
  }
}
```

## 🔒 Uso del Token

Incluir en todas las peticiones autenticadas:
```
Authorization: Bearer <access_token>
```