
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Assuming default based on .env
        database="acg01"
    )
    cursor = conn.cursor()
    cursor.execute("DESCRIBE certificates;")
    columns = cursor.fetchall()
    print("Table: certificates")
    for col in columns:
        print(f"- {col[0]} (Type: {col[1]})")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
