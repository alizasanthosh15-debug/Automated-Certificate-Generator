#!/usr/bin/env python3
"""
Database migration - Add missing columns to templates table
"""

from app.db import get_db_connection

def migrate_database():
    """Add missing columns to templates table"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("[1] Checking templates table structure...")
        
        # Check if columns exist before adding
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='templates' AND COLUMN_NAME='template_type'
        """)
        
        if not cursor.fetchone():
            print("[2] Adding template_type column...")
            cursor.execute("""
                ALTER TABLE templates 
                ADD COLUMN template_type ENUM('default', 'admin_upload', 'user_created') DEFAULT 'default'
            """)
            print("    ✅ template_type added")
        
        # Check creator_id
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='templates' AND COLUMN_NAME='creator_id'
        """)
        
        if not cursor.fetchone():
            print("[3] Adding creator_id column...")
            cursor.execute("""
                ALTER TABLE templates 
                ADD COLUMN creator_id INT AFTER template_type
            """)
            print("    ✅ creator_id added")
        
        # Check template_image_path
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='templates' AND COLUMN_NAME='template_image_path'
        """)
        
        if not cursor.fetchone():
            print("[4] Adding template_image_path column...")
            cursor.execute("""
                ALTER TABLE templates 
                ADD COLUMN template_image_path VARCHAR(500) AFTER creator_id
            """)
            print("    ✅ template_image_path added")
        
        # Check is_active
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='templates' AND COLUMN_NAME='is_active'
        """)
        
        if not cursor.fetchone():
            print("[5] Adding is_active column...")
            cursor.execute("""
                ALTER TABLE templates 
                ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER template_image_path
            """)
            print("    ✅ is_active added")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ Database migration completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DATABASE MIGRATION - Add missing columns")
    print("="*60 + "\n")
    
    success = migrate_database()
    exit(0 if success else 1)
