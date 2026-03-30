from app import create_app
from app.db import get_db_connection

app = create_app()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT template_id, template_image_path FROM templates ORDER BY created_at DESC LIMIT 3")
    templates = cursor.fetchall()
    print("---DATA---")
    for t in templates:
        print(f"ID:{t['template_id']}|PATH:{t['template_image_path']}")
    print("---END---")
    conn.close()
