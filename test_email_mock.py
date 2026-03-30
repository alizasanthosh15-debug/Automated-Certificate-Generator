
import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from app.services.email_service import send_certificate_email

class TestEmailService(unittest.TestCase):
    @patch('app.services.email_service.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        # Setup mock
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Test Data
        to_email = "test@example.com"
        name = "Test User"
        event_name = "Python Workshop"
        category = "Participant"
        
        # Create a dummy file for attachment
        with open("test_cert.pdf", "wb") as f:
            f.write(b"dummy pdf content")
            
        try:
            # Execute
            result = send_certificate_email(to_email, name, event_name, category, "test_cert.pdf")
            
            # Assertions
            self.assertTrue(result)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once()
            mock_server.send_message.assert_called_once()
            
            print("\n✅ Email Service Logic Verified: SMTP connection, Login, and Send called correctly.")
            
        finally:
            if os.path.exists("test_cert.pdf"):
                os.remove("test_cert.pdf")

    @patch('app.services.email_service.smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        # Setup mock to raise exception
        mock_smtp.side_effect = Exception("SMTP Connection Failed")
        
        # Create dummy file
        with open("test_cert.pdf", "wb") as f:
            f.write(b"dummy")
            
        # Define test data
        to_email = "fail@example.com"
        name = "Fail User"
        event_name = "Fail Event"
        category = "Fail Category"

        try:
            result = send_certificate_email(to_email, name, event_name, category, "test_cert.pdf")
            self.assertFalse(result)
            print("✅ Error Handling Verified: Function returned False on SMTP failure.")
        finally:
            if os.path.exists("test_cert.pdf"):
                os.remove("test_cert.pdf")

if __name__ == '__main__':
    unittest.main()
