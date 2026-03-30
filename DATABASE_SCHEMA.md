# Database Schema & Structure

## Tables Overview

### users
Stores user account information

```sql
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role ENUM('user', 'admin') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
- `user_id` - Unique identifier
- `name` - User's full name (2+ chars)
- `email` - Unique email (must be valid format)
- `password` - Hashed password (bcrypt)
- `role` - `user` or `admin`
- `created_at` - Registration timestamp

---

### certificates
Stores generated certificate information

```sql
CREATE TABLE certificates (
  certificate_id INT AUTO_INCREMENT PRIMARY KEY,
  participant_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(500),
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
- `certificate_id` - Unique identifier
- `participant_name` - Name on certificate
- `file_path` - Path to PDF file
- `generated_at` - Generation timestamp

---

### templates
Certificate template designs

```sql
CREATE TABLE templates (
  template_id INT AUTO_INCREMENT PRIMARY KEY,
  template_name VARCHAR(100) NOT NULL,
  title_text VARCHAR(255) DEFAULT 'Certificate of Excellence',
  subtitle_text VARCHAR(255) DEFAULT 'This certificate is proudly awarded to',
  border_color VARCHAR(7) DEFAULT '#0a2540',
  text_color VARCHAR(7) DEFAULT '#555555',
  font_size INT DEFAULT 22,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
- `template_id` - Unique identifier
- `template_name` - Template name
- `title_text` - Main title displayed
- `subtitle_text` - Subtitle text
- `border_color` - Hex color code
- `text_color` - Hex color code
- `font_size` - Font size in points

**Default Templates:**
- Participation
- Achievement
- Volunteering
- Workshop

---

### activity_logs
Tracks admin actions for audit trail

```sql
CREATE TABLE activity_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  action VARCHAR(100),
  description TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
- `log_id` - Unique identifier
- `user_id` - Admin who performed action
- `action` - Action type (e.g., DELETE_USER, UPDATE_TEMPLATE)
- `description` - Detailed description
- `timestamp` - When action occurred

---

## Common Queries

### Create Admin User
```sql
-- Generate hash: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
INSERT INTO users (name, email, password, role) 
VALUES ('Admin', 'admin@example.com', '$2b$12$...', 'admin');
```

### Create Regular User
```sql
INSERT INTO users (name, email, password, role) 
VALUES ('John Doe', 'john@example.com', '$2b$12$...', 'user');
```

### Get All Users
```sql
SELECT user_id, name, email, role, created_at FROM users ORDER BY created_at DESC;
```

### Get All Certificates
```sql
SELECT * FROM certificates ORDER BY generated_at DESC;
```

### Get All Activity Logs (with user names)
```sql
SELECT al.log_id, u.name as user_name, al.action, al.description, al.timestamp
FROM activity_logs al
LEFT JOIN users u ON al.user_id = u.user_id
ORDER BY al.timestamp DESC;
```

### Count Statistics
```sql
SELECT 
  COUNT(DISTINCT CASE WHEN role='user' THEN user_id END) as total_users,
  COUNT(DISTINCT CASE WHEN role='admin' THEN user_id END) as total_admins,
  (SELECT COUNT(*) FROM certificates) as total_certificates,
  (SELECT COUNT(*) FROM activity_logs) as total_activities
FROM users;
```

### Find User by Email
```sql
SELECT * FROM users WHERE email = 'john@example.com';
```

### Delete All Test Certificates
```sql
DELETE FROM certificates WHERE participant_name LIKE 'Test%';
```

---

## Database Maintenance

### Backup Database
```bash
mysqldump -u root -p acg01 > acg01_backup.sql
```

### Restore Database
```bash
mysql -u root -p acg01 < acg01_backup.sql
```

### Check Database Size
```sql
SELECT 
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'acg01'
ORDER BY (data_length + index_length) DESC;
```

### Clean Old Certificates (older than 1 year)
```sql
DELETE FROM certificates 
WHERE generated_at < DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

---

## Relationships

```
users (1) ----> (N) certificates
  |
  +---> (N) activity_logs

templates (independent - referenced by frontend)
```

---

## Constraints & Validation

### users table
- `email` - UNIQUE, must match regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- `password` - Must be hashed with bcrypt
- `role` - ENUM('user', 'admin')
- `name` - Minimum 2 characters

### certificates table
- `participant_name` - Cannot be empty
- `file_path` - Must point to valid PDF

### activity_logs table
- `user_id` - Foreign key, deletes cascade
- `action` - Predefined values (DELETE_USER, UPDATE_TEMPLATE, etc.)

---

## Performance Tips

### Add Indexes (if not present)
```sql
-- Speed up user lookups
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_role ON users(role);

-- Speed up certificate queries
CREATE INDEX idx_generated_at ON certificates(generated_at);
CREATE INDEX idx_participant_name ON certificates(participant_name);

-- Speed up activity log queries
CREATE INDEX idx_user_id ON activity_logs(user_id);
CREATE INDEX idx_timestamp ON activity_logs(timestamp);
```

### Monitor Slow Queries
```sql
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
```

---

## Troubleshooting

### Error: "Unknown database 'acg01'"
Solution: Create database first
```sql
CREATE DATABASE IF NOT EXISTS acg01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE acg01;
```

### Error: "Access denied for user 'root'"
Check credentials in `app/db.py`:
- Username should be: `root`
- Password should be: (empty) for XAMPP
- Host should be: `localhost`

### Error: "Table doesn't exist"
Run migrations:
```bash
mysql -u root -p acg01 < database_migrations.sql
```

---

**For database setup help, run:**
```bash
python
>>> from app.db import get_db_connection
>>> conn = get_db_connection()
>>> print("✅ Connected!" if conn.is_connected() else "❌ Failed")
>>> conn.close()
```
