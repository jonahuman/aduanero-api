-- =============================================
-- Base de datos Sistema Aduanero - LIMPIA
-- =============================================
-- Ejecutar este script para empezar desde cero

DROP DATABASE IF EXISTS aduanero_bbdd;
CREATE DATABASE aduanero_bbdd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aduanero_bbdd;

-- Tabla de usuarios
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Tabla de documentos
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    type ENUM('passport', 'id_card') NOT NULL,
    document_number VARCHAR(50) NOT NULL,
    expiration_date DATE NOT NULL,
    file_url VARCHAR(255) NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    reviewed_by VARCHAR(36) NULL,
    notes TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_uploaded_at (uploaded_at)
);

-- Tabla de registros aduaneros
CREATE TABLE customs_records (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    status ENUM('activo', 'inactivo', 'pendiente') DEFAULT 'pendiente',
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_by VARCHAR(36) NULL,
    notes TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (processed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_processed_at (processed_at)
);

-- =============================================
-- DATOS INICIALES - BASE DE DATOS LIMPIA
-- =============================================
-- No insertar datos iniciales - empezar desde cero
-- Los usuarios se crean desde el frontend

-- Para crear admin usar: POST /api/setup/admin
-- Para limpiar todo usar: DELETE /api/setup/reset-database

-- Vistas útiles para reportes
CREATE VIEW user_summary AS
SELECT 
    u.id,
    u.email,
    CONCAT(u.first_name, ' ', u.last_name) as full_name,
    u.nationality,
    COUNT(d.id) as total_documents,
    COUNT(CASE WHEN d.status = 'approved' THEN 1 END) as approved_docs,
    COUNT(CASE WHEN d.status = 'pending' THEN 1 END) as pending_docs,
    COUNT(CASE WHEN d.status = 'rejected' THEN 1 END) as rejected_docs,
    cr.status as customs_status,
    u.created_at
FROM users u
LEFT JOIN documents d ON u.id = d.user_id
LEFT JOIN customs_records cr ON u.id = cr.user_id
GROUP BY u.id, cr.status;

-- Procedimiento para estadísticas del dashboard
DELIMITER //
CREATE PROCEDURE GetDashboardStats()
BEGIN
    SELECT 
        (SELECT COUNT(*) FROM users WHERE is_admin = FALSE) as total_users,
        (SELECT COUNT(*) FROM documents) as total_documents,
        (SELECT COUNT(*) FROM documents WHERE status = 'approved') as approved_documents,
        (SELECT COUNT(*) FROM documents WHERE status = 'pending') as pending_documents,
        (SELECT COUNT(*) FROM documents WHERE status = 'rejected') as rejected_documents,
        (SELECT COUNT(*) FROM customs_records) as total_records,
        (SELECT COUNT(*) FROM customs_records WHERE status = 'activo') as active_records,
        (SELECT COUNT(*) FROM customs_records WHERE status = 'inactivo') as inactive_records,
        (SELECT COUNT(*) FROM customs_records WHERE status = 'pendiente') as pending_records;
END //
DELIMITER ;