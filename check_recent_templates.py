from app import create_app
from app.db import get_db_connection

app = create_app()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT template_id, template_name, template_image_path, created_at FROM templates ORDER BY created_at DESC LIMIT 5")
    templates = cursor.fetchall()
    print("Recent Templates:")
    for t in templates:
        print(f"ID: {t['template_id']}, Name: {t['template_name']}, Path: {t['template_image_path']}")
    conn.close()
