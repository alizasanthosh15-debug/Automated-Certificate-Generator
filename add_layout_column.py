
import mysql.connector
from app.db import get_db_connection

def add_layout_config_column():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM templates LIKE 'layout_config'")
        result = cursor.fetchone()
        
        if not result:
            print("Adding layout_config column to templates table...")
            cursor.execute("ALTER TABLE templates ADD COLUMN layout_config JSON DEFAULT NULL")
            conn.commit()
            print("✅ Column added successfully.")
        else:
            print("ℹ️ Column layout_config already exists.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_layout_config_column()
