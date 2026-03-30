from app import create_app
from app.db import get_db_connection

app = create_app()

with app.app_context():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT template_id, template_name, template_image_path FROM templates WHERE template_image_path LIKE '%Doc1%'")
    templates = cursor.fetchall()
    print("Found templates:")
    for t in templates:
        print(t)
    conn.close()
