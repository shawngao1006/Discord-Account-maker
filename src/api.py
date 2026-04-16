import requests
import re
import time
from colorama import Fore, Style, init 
from fake_useragent import UserAgent

init(convert=True)

class TempMail:
    BASE_URL = 'https://api.guerrillamail.com/ajax.php'
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.email = None
        self.sid_token = None
        self.get_random_email()
    
    def get_random_email(self):
        try:
            response = self.session.get(f'{self.BASE_URL}?f=get_email_address')
            if response.status_code == 200:
                data = response.json()
                self.email = data.get('email_addr')
                self.sid_token = data.get('sid_token')
                return self.email
        except Exception as e:
            print(f"Error getting random email: {e}")
        return None
    
    def get_inbox(self):
        if not self.sid_token:
            return []
        try:
            response = self.session.get(f'{self.BASE_URL}?f=get_email_list&offset=0&sid_token={self.sid_token}')
            if response.status_code == 200:
                data = response.json()
                return data.get('list', [])
        except Exception as e:
            print(f"Error getting inbox: {e}")
        return []
    
    def get_single_message(self, msg_id):
        if not self.sid_token:
            return None
        try:
            response = self.session.get(f'{self.BASE_URL}?f=fetch_email&email_id={msg_id}&sid_token={self.sid_token}')
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting message: {e}")
        return None

# Backward compatibility aliases
class GmailnatorGet(TempMail):
    def get_email(self):
        return self.email

class GmailnatorRead(TempMail):
    def __init__(self, email, raw_email, types):
        # For compatibility, but we don't use these params
        super().__init__()
        self.type = types
        self.email = email
        self.raw_email = raw_email
    
    def get_inbox(self):
        messages = super().get_inbox()
        # Convert to format expected by the code - list of dicts
        return messages
    
    def get_single_message(self, msg_id):
        message = super().get_single_message(msg_id)
        if message:
            return message  # Return the dict, which has 'mail_body' key
        return None

def dfilter_email(email):
    # Not needed for Guerrilla Mail, but keep for compatibility
    return email

def pfilter_email(email):
    # Not needed for Guerrilla Mail, but keep for compatibility
    return email

def find_email_type(email):
    # Guerrilla Mail doesn't use dot/plus, so return 'dot' as default
    return 'dot'
