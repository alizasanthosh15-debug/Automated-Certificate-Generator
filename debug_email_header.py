
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Test"
msg["From"] = "me@example.com"
msg["To"] = "you@example.com"
msg.set_content("Body")

print(f"Type: {type(msg)}")
print(f"Keys: {msg.keys()}")
print(f"Message-ID (get): {msg.get('Message-ID')}")
print(f"Message-ID (brackets): {msg['Message-ID']}")
