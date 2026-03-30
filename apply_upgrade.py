import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def apply_upgrade():
    print("🔌 Connecting to database...")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "acg01")
        )
        cursor = conn.cursor()
        print("✅ Connected!")
        
        # Read SQL file
        with open("UPGRADE_DB.sql", "r") as f:
            sql_script = f.read()
            
        # Split into separate statements (naive split by semicolon)
        # This is simple but works for simple ALTER/CREATE statements
        statements = sql_script.split(';')
        
        for statement in statements:
            if statement.strip():
                try:
                    # Skip USE command as we already connected to DB
                    if statement.strip().upper().startswith("USE"):
                        continue
                        
                    print(f"Executing: {statement.strip()[:50]}...")
                    cursor.execute(statement)
                except mysql.connector.Error as err:
                    # Ignore "Duplicate column" errors if ran multiple times
                    if err.errno == 1060: 
                        print(f"⚠️ Column already exists (Skipping)")
                    elif err.errno == 1050:
                        print(f"⚠️ Table already exists (Skipping)")
                    else:
                        print(f"❌ Error: {err}")
        
        conn.commit()
        print("✅ Database upgrade completed successfully!")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

if __name__ == "__main__":
    apply_upgrade()
