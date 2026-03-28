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
            base_url: DVWA base URL (e.g., http://localhost/DVWA or http://localhost/dvwa)
            username: DVWA username
            password: DVWA password
            
        Returns:
            True if login successful
        """
        try:
            # Normalize base URL - remove trailing slash
            base_url = base_url.rstrip('/')
            
            # Get login page to obtain CSRF token
            login_url = urljoin(base_url + '/', "login.php")
            
            # Test if URL is accessible
            try:
                response = self.session.get(login_url, timeout=10)
            except requests.exceptions.RequestException as e:
                print(f"[!] Cannot reach DVWA at {login_url}")
                print(f"[!] Error: {e}")
                return False
            
            # Check if we got a valid response
            if response.status_code != 200:
                print(f"[!] DVWA login page returned status {response.status_code}")
                return False
            
            # Extract user_token from response
            import re
            user_token = ''
            
            # Try multiple token patterns (DVWA versions vary)
            token_patterns = [
                r"name=['\"]user_token['\"] value=['\"]([^'\"]+)['\"]",
                r"name='user_token' value='([^']+)'",
                r'name="user_token" value="([^"]+)"',
            ]
            
            for pattern in token_patterns:
                token_match = re.search(pattern, response.text)
                if token_match:
                    user_token = token_match.group(1)
                    break
            
            # Perform login
            login_data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }
            
            # Only add user_token if found
            if user_token:
                login_data['user_token'] = user_token
            
            # Post login credentials
            response = self.session.post(login_url, data=login_data, allow_redirects=True)
            
            # Check multiple success indicators
            success_indicators = [
                'logout.php' in response.text.lower(),
                'logout' in response.text.lower() and 'login' not in response.url.lower(),
                response.url.endswith('index.php'),
                'welcome to damn vulnerable web application' in response.text.lower(),
            ]
            
            if any(success_indicators):
                self.authenticated = True
                return True
            
            # Debug output if login failed
            print(f"[!] Login may have failed - check credentials")
            print(f"[!] Final URL: {response.url}")
            print(f"[!] Status code: {response.status_code}")
            
            # Check for common error messages
            if 'username and/or password incorrect' in response.text.lower():
                print(f"[!] DVWA reported: Invalid username or password")
            elif 'login' in response.text.lower() and 'username' in response.text.lower():
                print(f"[!] Still on login page - authentication failed")
            
            return False
            
        except Exception as e:
            print(f"[!] Login exception: {e}")
            import traceback
            traceback.print_exc()
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
