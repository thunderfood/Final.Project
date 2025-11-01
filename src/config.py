# src/config.py - Load configuration

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Email settings
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER", "imap.gmail.com")
    
    # LM Studio settings
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
    
    # App settings
    CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", "6"))
    MAX_EMAILS_TO_CHECK = int(os.getenv("MAX_EMAILS_TO_CHECK", "10"))
    
    @classmethod
    def is_email_configured(cls):
        """Check if email is configured"""
        return bool(cls.EMAIL_ADDRESS and cls.EMAIL_PASSWORD)

# Test
if __name__ == "__main__":
    print("\n" + "="*50)
    print("Configuration Check")
    print("="*50 + "\n")
    
    print(f"Email configured: {Config.is_email_configured()}")
    print(f"Email address: {Config.EMAIL_ADDRESS if Config.EMAIL_ADDRESS else 'Not set'}")
    print(f"LLM URL: {Config.LLM_BASE_URL}")
    print(f"Check interval: {Config.CHECK_INTERVAL_HOURS} hours")
    print(f"Max emails: {Config.MAX_EMAILS_TO_CHECK}")
    
    print("\n✅ Configuration loaded!\n")
