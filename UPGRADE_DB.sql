-- ==========================================
-- DATABASE UPGRADE SCRIPT
-- Run this in your XAMPP phpMyAdmin (SQL Tab)
-- ==========================================

USE acg01;

-- 1. Add Coordinate Columns to 'templates' table
-- These store the X, Y position for each text field (in points, 1/72 inch)
-- Default values are based on A4 Landscape center
ALTER TABLE templates
ADD COLUMN name_pos_x INT DEFAULT 421,
ADD COLUMN name_pos_y INT DEFAULT 300,
ADD COLUMN course_pos_x INT DEFAULT 421,
ADD COLUMN course_pos_y INT DEFAULT 230,
ADD COLUMN date_pos_x INT DEFAULT 150,
ADD COLUMN date_pos_y INT DEFAULT 100,
ADD COLUMN signature_pos_x INT DEFAULT 700,
ADD COLUMN signature_pos_y INT DEFAULT 100;

-- 2. Create 'email_logs' table (if not exists)
-- Track all sent emails
CREATE TABLE IF NOT EXISTS email_logs (
    email_id INT AUTO_INCREMENT PRIMARY KEY,
    certificate_id INT,
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(255),
    status ENUM('sent', 'failed') DEFAULT 'sent',
    error_message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (certificate_id) REFERENCES certificates(certificate_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Update 'certificates' table to link to 'templates'
ALTER TABLE certificates
ADD COLUMN template_id INT,
ADD CONSTRAINT fk_cert_template FOREIGN KEY (template_id) REFERENCES templates(template_id) ON DELETE SET NULL;
