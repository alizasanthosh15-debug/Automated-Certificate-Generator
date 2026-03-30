
import requests
import json
import os

DOTENV_PATH = ".env"

def create_ethereal_account():
    print("🪄 Creating Ethereal Test Account...")
    
    try:
        response = requests.post("https://api.nodemailer.com/user", json={"requestor": "QuickCertfyy", "version": "NODEMAILER"})
        
        if response.status_code == 200:
            data = response.json()
            user = data['user']
            passw = data['pass']
            smtp_host = data['smtp']['host']
            smtp_port = data['smtp']['port']
            imap_host = data['imap']['host']
            imap_port = data['imap']['port']
            web_url = "https://ethereal.email"

            print(f"\n✅ Account Created Successfully!")
            print(f"   Email: {user}")
            print(f"   Password: {passw}")
            print(f"   SMTP: {smtp_host}:{smtp_port}")
            print(f"   Webmail: {web_url}")

            # Update .env file
            update_env_file(user, passw, smtp_host, smtp_port)
            
        else:
            print(f"❌ Failed to create account. Status: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Error: {e}")

def update_env_file(user, password, host, port):
    # Read existing content
    lines = []
    if os.path.exists(DOTENV_PATH):
        with open(DOTENV_PATH, "r") as f:
            lines = f.readlines()

    # Filter out existing email config
    lines = [line for line in lines if not line.startswith("EMAIL_") and not line.startswith("SMTP_")]

    # Append new config
    lines.append("\n# Ethereal Email Configuration (Testing)\n")
    lines.append(f"EMAIL_USER={user}\n")
    lines.append(f"EMAIL_PASS={password}\n")
    lines.append(f"SMTP_SERVER={host}\n")
    lines.append(f"SMTP_PORT={port}\n")

    # Write back
    with open(DOTENV_PATH, "w") as f:
        f.writelines(lines)
    
    print(f"\n✅ Updated {DOTENV_PATH} with new credentials.")
    print("   Restart your backend to apply changes.")

if __name__ == "__main__":
    create_ethereal_account()
