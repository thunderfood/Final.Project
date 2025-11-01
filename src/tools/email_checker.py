# src/tools/email_checker.py

import imaplib
import email
from email.header import decode_header
from datetime import datetime

class EmailChecker:
    """Simple email checker for Gmail/Outlook"""
    
    def __init__(self, email_address, password, imap_server="imap.gmail.com"):
        """
        Initialize email checker
        
        Args:
            email_address: Your email address
            password: App password (NOT your regular password)
            imap_server: IMAP server (default: Gmail)
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.mail = None
    
    def connect(self):
        """Connect to email server"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def get_recent_emails(self, num_emails=5, folder="INBOX"):
        """Get recent emails"""
        if not self.mail:
            if not self.connect():
                return []
        
        try:
            # Select inbox
            self.mail.select(folder)
            
            # Search for all emails
            _, message_numbers = self.mail.search(None, "ALL")
            
            # Get last N emails
            email_ids = message_numbers[0].split()
            email_ids = email_ids[-num_emails:]  # Get last N
            
            emails = []
            
            for email_id in reversed(email_ids):  # Newest first
                # Fetch email
                _, msg_data = self.mail.fetch(email_id, "(RFC822)")
                
                # Parse email
                email_body = msg_data[0][1]
                message = email.message_from_bytes(email_body)
                
                # Extract info
                subject = self.decode_subject(message["Subject"])
                from_addr = message.get("From", "Unknown")
                date = message.get("Date", "Unknown")
                
                # Get email body (simplified)
                body = self.get_email_body(message)
                
                emails.append({
                    "subject": subject,
                    "from": from_addr,
                    "date": date,
                    "body_preview": body[:200] if body else "No content"
                })
            
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
    
    def decode_subject(self, subject):
        """Decode email subject"""
        if subject is None:
            return "No Subject"
        
        decoded = decode_header(subject)
        subject_str = ""
        
        for content, encoding in decoded:
            if isinstance(content, bytes):
                try:
                    subject_str += content.decode(encoding or "utf-8")
                except:
                    subject_str += content.decode("utf-8", errors="ignore")
            else:
                subject_str += str(content)
        
        return subject_str
    
    def get_email_body(self, message):
        """Extract email body"""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode()
                    except:
                        return ""
        else:
            try:
                return message.get_payload(decode=True).decode()
            except:
                return ""
        return ""
    
    def format_email_summary(self, emails):
        """Format emails as readable text"""
        if not emails:
            return "No emails found"
        
        summary = f"Recent Emails ({len(emails)} total):\n\n"
        
        for i, email_data in enumerate(emails, 1):
            summary += f"{i}. {email_data['subject']}\n"
            summary += f"   From: {email_data['from']}\n"
            summary += f"   Date: {email_data['date']}\n"
            summary += f"   Preview: {email_data['body_preview'][:100]}...\n\n"
        
        return summary
    
    def disconnect(self):
        """Close connection"""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass

# Test (with dummy credentials - won't actually work)
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Email Checker Demo")
    print("="*50 + "\n")
    
    print("⚠️  NOTE: This is a demo structure.")
    print("To actually use this, you need:")
    print("1. Your email address")
    print("2. An app password (NOT your regular password)")
    print("3. Enable IMAP in your email settings\n")
    
    # Demo structure (won't connect)
    checker = EmailChecker(
        email_address="your-email@gmail.com",
        password="your-app-password",
        imap_server="imap.gmail.com"
    )
    
    print("✅ Email checker created!")
    print("📝 To use it, configure your credentials in dashboard\n")
