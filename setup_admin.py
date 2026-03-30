#!/usr/bin/env python3
"""
Setup admin user and test login
"""

from werkzeug.security import generate_password_hash
from app.db import get_db_connection
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

def setup_admin():
    """Create admin user in database"""
    try:
        # Admin credentials
        admin_name = "Admin"
        admin_email = "admin@example.com"
        admin_password = "admin123"
        
        # Hash password
        hashed_password = generate_password_hash(admin_password)
        print(f"✅ Password hashed: {hashed_password[:50]}...")
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (admin_email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"⚠️  Admin user already exists (user_id: {existing[0]})")
            print("   Deleting old admin to recreate...")
            cursor.execute("DELETE FROM users WHERE email = %s", (admin_email,))
            conn.commit()
        
        # Insert admin user
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (admin_name, admin_email, hashed_password, 'admin')
        )
        conn.commit()
        print(f"✅ Admin user created: {admin_email}")
        
        # Get the inserted user
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (admin_email,))
        admin_id = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return admin_id, admin_email, admin_password, hashed_password
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        return None, None, None, None

def test_login(email, password):
    """Test admin login"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            print(f"❌ User not found: {email}")
            return None
        
        print(f"\n📊 User Found:")
        print(f"   ID: {user['user_id']}")
        print(f"   Name: {user['name']}")
        print(f"   Email: {user['email']}")
        print(f"   Role: {user['role']}")
        print(f"   Password Hash: {user['password'][:50]}...")
        
        # Check password
        from werkzeug.security import check_password_hash
        password_match = check_password_hash(user['password'], password)
        print(f"   Password Match: {'✅ YES' if password_match else '❌ NO'}")
        
        if not password_match:
            print(f"❌ Password verification failed!")
            return None
        
        # Generate token
        token = jwt.encode(
            {
                "user_id": user['user_id'],
                "email": user['email'],
                "role": user['role']
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        
        print(f"\n✅ Login successful!")
        print(f"   Token: {token[:50]}...")
        return token
        
    except Exception as e:
        print(f"❌ Login test failed: {str(e)}")
        return None

if __name__ == "__main__":
    print("\n" + "="*60)
    print("ADMIN SETUP & LOGIN TEST")
    print("="*60 + "\n")
    
    # Setup
    print("[1] Setting up admin user...")
    admin_id, email, password, hash_val = setup_admin()
    
    if not admin_id:
        print("\n[ERROR] Setup failed!")
        exit(1)
    
    print(f"   Admin ID: {admin_id}")
    print(f"   Email: {email}")
    print(f"   Password: {password}\n")
    
    # Test login
    print("[2] Testing admin login...")
    token = test_login(email, password)
    
    if token:
        print("\n" + "="*60)
        print("SUCCESS - ADMIN SETUP COMPLETE!")
        print("="*60)
        print(f"\nUse these credentials to login:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print(f"  Role: admin\n")
        
        print("Test with:")
        print(f'''
$body = @{{ 
    email = "{email}"
    password = "{password}"
    role = "admin"
}} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" `
    -Method POST -Body $body -ContentType "application/json"

$response | ConvertTo-Json
        ''')
    else:
        print("\n[ERROR] Login test failed!")
        exit(1)
