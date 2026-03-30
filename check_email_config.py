
import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_email_config():
    print("🔍 DEBUGGING EMAIL CONFIGURATION...\n")

    # 1. Check Environment Variables
    email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    port = os.getenv("SMTP_PORT", "587")

    print(f"1. Checking Variables:")
    print(f"   - EMAIL_USER: {'✅ Found' if email else '❌ Missing'}")
    print(f"   - EMAIL_PASS: {'✅ Found' if password else '❌ Missing'}")
    print(f"   - SMTP_SERVER: {server}")
    print(f"   - SMTP_PORT: {port}")

    if not email or not password:
        print("\n❌ CRITICAL: Missing credentials in .env file.")
        return

    # 2. Test SMTP Connection
    print("\n2. Testing SMTP Connection...")
    try:
        smtp = smtplib.SMTP(server, int(port))
        smtp.starttls()
        print("   - ✅ Connected and started TLS")
        
        try:
            smtp.login(email, password)
            print("   - ✅ Login Successful!")
        except smtplib.SMTPAuthenticationError:
            print("   - ❌ Login FAILED. Check your password.")
            print("     (Note: For Gmail, you MUST use an App Password, not your login password.)")
            return
        except Exception as e:
            print(f"   - ❌ Login Error: {e}")
            return

        # 3. Send Test Email
        print("\n3. Sending Test Email...")
        try:
            msg = EmailMessage()
            msg["From"] = email
            msg["To"] = email  # Send to self
            msg["Subject"] = "Test Email from QuickCert Config Check"
            msg.set_content("If you see this, your email configuration is working perfectly!")
            
            # Explicitly set Message-ID
            msg_id = make_msgid()
            msg["Message-ID"] = msg_id

            smtp.send_message(msg)
            print(f"   - ✅ Test email sent to {email}")
            if "ethereal" in server:
                clean_id = msg_id.strip("<>")
                print(f"   📬 Ethereal Preview URL: https://ethereal.email/message/{clean_id}")
            else:
                print("   - Check your inbox (and spam folder)!")
        except Exception as e:
            print(f"   - ❌ Sending Failed: {e}")
        
        smtp.quit()

    except Exception as e:
        print(f"   - ❌ Connection Failed: {e}")

if __name__ == "__main__":
    debug_email_config()
