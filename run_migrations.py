import mysql.connector

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="acg01",
        auth_plugin="mysql_native_password"
    )

# Run migrations
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Running database migrations...")
    
    # 1. Add role and created_at columns to users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role ENUM('user', 'admin') DEFAULT 'user' AFTER password")
        print("✓ Added role column to users table")
    except:
        print("✓ role column already exists")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER role")
        print("✓ Added created_at column to users table")
    except:
        print("✓ created_at column already exists")
    
    conn.commit()
    
    # 2. Create templates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS templates (
      template_id INT AUTO_INCREMENT PRIMARY KEY,
      template_name VARCHAR(100) NOT NULL,
      title_text VARCHAR(255) DEFAULT 'Certificate of Excellence',
      subtitle_text VARCHAR(255) DEFAULT 'This certificate is proudly awarded to',
      border_color VARCHAR(7) DEFAULT '#0a2540',
      text_color VARCHAR(7) DEFAULT '#555555',
      font_size INT DEFAULT 22,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✓ Created templates table")
    conn.commit()
    
    # 3. Create activity_logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
      log_id INT AUTO_INCREMENT PRIMARY KEY,
      user_id INT,
      action VARCHAR(100),
      description TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✓ Created activity_logs table")
    conn.commit()
    
    # 4. Insert default templates
    cursor.execute("SELECT COUNT(*) as count FROM templates")
    result = cursor.fetchone()
    if result[0] == 0:
        cursor.execute("""
        INSERT INTO templates (template_name, title_text, subtitle_text) VALUES
        ('Participation', 'Certificate of Participation', 'This certificate is proudly awarded to'),
        ('Achievement', 'Certificate of Achievement', 'In recognition of outstanding achievement'),
        ('Volunteering', 'Certificate of Volunteering', 'In appreciation of your valuable contribution'),
        ('Workshop', 'Certificate of Completion', 'For successful completion of the workshop')
        """)
        print("✓ Inserted default templates")
        conn.commit()
    else:
        print("✓ Templates already exist")
    
    # 5. Create test admin user
    from werkzeug.security import generate_password_hash
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE email = %s", ('admin@example.com',))
    result = cursor.fetchone()
    if result[0] == 0:
        hashed_password = generate_password_hash('admin@123')
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            ('Admin', 'admin@example.com', hashed_password, 'admin')
        )
        print("✓ Created admin user (email: admin@example.com, password: admin@123)")
        conn.commit()
    else:
        print("✓ Admin user already exists")
    
    cursor.close()
    conn.close()
    print("\n✅ All migrations completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
