from app.db import get_db_connection
conn=get_db_connection()
c=conn.cursor(dictionary=True)
c.execute("SELECT participant_name, participant_email, file_path, generated_at FROM certificates ORDER BY certificate_id DESC LIMIT 5")
print(c.fetchall())
c.close(); conn.close()
