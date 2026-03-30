from app.services.pdf_service import generate_certificate
import os

# Create a dummy template if it doesn't exist
template_path = "test_template.png"
if not os.path.exists(template_path):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(template_path, pagesize=landscape(A4))
    c.drawString(100, 100, "BACKGROUND TEMPLATE")
    c.save()

data = {
    "name": "Test User",
    "course": "Python Mastery",
    "date": "2023-10-27"
}

output_path = "test_certificate.pdf"

success = generate_certificate(data, template_path, output_path)

if success:
    print(f"✅ Certificate generated at {output_path}")
else:
    print("❌ Failed to generate certificate")
