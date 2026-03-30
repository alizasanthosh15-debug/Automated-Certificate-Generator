
import mysql.connector

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="acg01")
    cursor = conn.cursor()
    cursor.execute("DESCRIBE certificates")
    columns = [row[0] for row in cursor.fetchall()]
    print("Columns in certificates table:", columns)
    
    if "participant_email" not in columns:
        print("MISSING: participant_email")
        try:
            cursor.execute("ALTER TABLE certificates ADD COLUMN participant_email VARCHAR(255) DEFAULT NULL AFTER participant_name")
            conn.commit()
            print("ADDED: participant_email column successfully.")
        except Exception as e:
            print(f"FAILED to add column: {e}")
    else:
        print("FOUND: participant_email")
        
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
