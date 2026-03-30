-- SQL Migrations for Certificate Generator Admin System
-- Run these commands in MySQL Workbench or phpMyAdmin

-- 1. Add role and created_at columns to users table
ALTER TABLE users ADD COLUMN role ENUM('user', 'admin') DEFAULT 'user' AFTER password;
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER role;

-- 2. Create certificates table
CREATE TABLE IF NOT EXISTS certificates (
  certificate_id INT AUTO_INCREMENT PRIMARY KEY,
  participant_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(500),
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Create templates table
CREATE TABLE IF NOT EXISTS templates (
  template_id INT AUTO_INCREMENT PRIMARY KEY,
  template_name VARCHAR(100) NOT NULL,
  title_text VARCHAR(255) DEFAULT 'Certificate of Excellence',
  subtitle_text VARCHAR(255) DEFAULT 'This certificate is proudly awarded to',
  border_color VARCHAR(7) DEFAULT '#0a2540',
  text_color VARCHAR(7) DEFAULT '#555555',
  font_size INT DEFAULT 22,
  template_type ENUM('default', 'admin_upload', 'user_created') DEFAULT 'default',
  creator_id INT,
  template_image_path VARCHAR(500),
  name_pos_x INT DEFAULT 421,
  name_pos_y INT DEFAULT 300,
  course_pos_x INT DEFAULT 421,
  course_pos_y INT DEFAULT 230,
  date_pos_x INT DEFAULT 150,
  date_pos_y INT DEFAULT 100,
  signature_pos_x INT DEFAULT 700,
  signature_pos_y INT DEFAULT 100,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (creator_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Create activity_logs table
CREATE TABLE IF NOT EXISTS activity_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(100),
  description TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Create email_logs table
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

-- 5. Insert default certificate templates
INSERT INTO templates (template_name, title_text, subtitle_text) VALUES
('Participation', 'Certificate of Participation', 'This certificate is proudly awarded to'),
('Achievement', 'Certificate of Achievement', 'In recognition of outstanding achievement'),
('Volunteering', 'Certificate of Volunteering', 'In appreciation of your valuable contribution'),
('Workshop', 'Certificate of Completion', 'For successful completion of the workshop');

-- 6. Add indexes for performance
-- queries filtering by user_id, template_id and creator_id are common and benefit from indexes
ALTER TABLE certificates ADD INDEX idx_cert_user (user_id);
ALTER TABLE certificates ADD INDEX idx_cert_template (template_id);
ALTER TABLE templates ADD INDEX idx_templates_creator (creator_id);

-- 7. Create an admin user (optional - modify email and password as needed)
-- First generate a password hash using: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
-- Then insert: INSERT INTO users (name, email, password, role) VALUES ('Admin', 'admin@example.com', '<hashed_password>', 'admin');
