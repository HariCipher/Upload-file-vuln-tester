"""
Session Handler Module
Manages authentication and session cookies for testing authenticated uploads
"""

import requests
from typing import Dict, Optional
from urllib.parse import urljoin

class SessionHandler:
    """Handle login and session management for authenticated testing"""
    
    def __init__(self):
        self.session = requests.Session()
        self.authenticated = False
        
    def login_dvwa(self, base_url: str, username: str = "admin", password: str = "password") -> bool:
        """
        Login to DVWA and maintain session
        
        Args:
            base_url: DVWA base URL (e.g., http://localhost/DVWA)
            username: DVWA username
            password: DVWA password
            
        Returns:
            True if login successful
        """
        try:
            # Get login page to obtain CSRF token
            login_url = urljoin(base_url, "login.php")
            response = self.session.get(login_url)
            
            # Extract user_token from response
            if 'user_token' in response.text:
                import re
                token_match = re.search(r"name='user_token' value='([^']+)'", response.text)
                user_token = token_match.group(1) if token_match else ''
            else:
                user_token = ''
            
            # Perform login
            login_data = {
                'username': username,
                'password': password,
                'Login': 'Login',
                'user_token': user_token
            }
            
            response = self.session.post(login_url, data=login_data)
            
            # Check if login successful
            if 'logout' in response.text.lower() or response.url.endswith('index.php'):
                self.authenticated = True
                return True
            
            return False
            
        except Exception as e:
            print(f"[!] Login failed: {e}")
            return False
    
    def set_dvwa_security(self, base_url: str, level: str = "low") -> bool:
        """
        Set DVWA security level
        
        Args:
            base_url: DVWA base URL
            level: Security level (low, medium, high, impossible)
            
        Returns:
            True if successful
        """
        try:
            security_url = urljoin(base_url, "security.php")
            
            data = {
                'security': level,
                'seclev_submit': 'Submit'
            }
            
            response = self.session.post(security_url, data=data)
            return response.status_code == 200
            
        except Exception as e:
            print(f"[!] Failed to set security level: {e}")
            return False
    
    def login_custom(self, login_url: str, credentials: Dict[str, str], 
                     success_indicator: str = "logout") -> bool:
        """
        Generic login for custom applications
        
        Args:
            login_url: URL of login page
            credentials: Dict of form fields and values
            success_indicator: String that appears after successful login
            
        Returns:
            True if login successful
        """
        try:
            response = self.session.post(login_url, data=credentials)
            
            if success_indicator.lower() in response.text.lower():
                self.authenticated = True
                return True
            
            return False
            
        except Exception as e:
            print(f"[!] Custom login failed: {e}")
            return False
    
    def get_session(self) -> requests.Session:
        """Return the active session object"""
        return self.session
    
    def get_cookies(self) -> Dict:
        """Return current session cookies"""
        return dict(self.session.cookies)
    
    def is_authenticated(self) -> bool:
        """Check if session is authenticated"""
        return self.authenticated
    
    def close(self):
        """Close the session"""
        self.session.close()
