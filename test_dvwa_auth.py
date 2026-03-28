#!/usr/bin/env python3
"""
DVWA Authentication Diagnostic Script
Tests DVWA login separately to debug authentication issues
"""

import requests
import re
from urllib.parse import urljoin

def test_dvwa_access(base_url):
    """Test if DVWA is accessible"""
    print(f"\n{'='*60}")
    print(f"Testing DVWA Access")
    print(f"{'='*60}")
    
    base_url = base_url.rstrip('/')
    
    # Test main page
    print(f"\n[*] Testing main page: {base_url}/")
    try:
        r = requests.get(f"{base_url}/", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✓ Main page accessible")
        else:
            print(f"    ✗ Unexpected status code")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False
    
    # Test login page
    print(f"\n[*] Testing login page: {base_url}/login.php")
    try:
        r = requests.get(f"{base_url}/login.php", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✓ Login page accessible")
            
            # Check for user_token
            if 'user_token' in r.text:
                print(f"    ✓ CSRF token field found")
                
                # Extract token
                patterns = [
                    r"name=['\"]user_token['\"] value=['\"]([^'\"]+)['\"]",
                    r"name='user_token' value='([^']+)'",
                    r'name="user_token" value="([^"]+)"',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, r.text)
                    if match:
                        print(f"    ✓ Token extracted: {match.group(1)[:20]}...")
                        break
            else:
                print(f"    ⚠ No CSRF token found (might not be required)")
                
        else:
            print(f"    ✗ Unexpected status code")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False
    
    return True

def test_dvwa_login(base_url, username, password):
    """Test DVWA authentication"""
    print(f"\n{'='*60}")
    print(f"Testing DVWA Authentication")
    print(f"{'='*60}")
    
    base_url = base_url.rstrip('/')
    session = requests.Session()
    
    # Step 1: Get login page
    print(f"\n[*] Step 1: Fetching login page")
    login_url = f"{base_url}/login.php"
    
    try:
        response = session.get(login_url, timeout=10)
        print(f"    Status: {response.status_code}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False
    
    # Step 2: Extract CSRF token
    print(f"\n[*] Step 2: Extracting CSRF token")
    user_token = ''
    
    patterns = [
        r"name=['\"]user_token['\"] value=['\"]([^'\"]+)['\"]",
        r"name='user_token' value='([^']+)'",
        r'name="user_token" value="([^"]+)"',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response.text)
        if match:
            user_token = match.group(1)
            print(f"    ✓ Token found: {user_token[:20]}...")
            break
    
    if not user_token:
        print(f"    ⚠ No token found (proceeding without)")
    
    # Step 3: Prepare login data
    print(f"\n[*] Step 3: Preparing login credentials")
    print(f"    Username: {username}")
    print(f"    Password: {'*' * len(password)}")
    
    login_data = {
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    
    if user_token:
        login_data['user_token'] = user_token
    
    # Step 4: Submit login
    print(f"\n[*] Step 4: Submitting login")
    try:
        response = session.post(login_url, data=login_data, allow_redirects=True)
        print(f"    Status: {response.status_code}")
        print(f"    Final URL: {response.url}")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False
    
    # Step 5: Check authentication
    print(f"\n[*] Step 5: Checking authentication")
    
    success_checks = {
        'logout.php in page': 'logout.php' in response.text.lower(),
        'logout link present': 'logout' in response.text.lower() and 'login' not in response.url.lower(),
        'redirected to index': response.url.endswith('index.php'),
        'welcome message': 'welcome to damn vulnerable' in response.text.lower(),
    }
    
    authenticated = False
    for check, result in success_checks.items():
        status = "✓" if result else "✗"
        print(f"    {status} {check}: {result}")
        if result:
            authenticated = True
    
    # Check for error messages
    error_checks = {
        'invalid credentials': 'username and/or password incorrect' in response.text.lower(),
        'still on login page': 'login' in response.text.lower() and 'username' in response.text.lower(),
    }
    
    print(f"\n[*] Error checks:")
    for check, result in error_checks.items():
        if result:
            print(f"    ⚠ {check}: {result}")
    
    # Final verdict
    print(f"\n{'='*60}")
    if authenticated:
        print(f"✓ AUTHENTICATION SUCCESSFUL")
        print(f"{'='*60}")
        
        # Test security level setting
        print(f"\n[*] Testing security level change")
        security_url = f"{base_url}/security.php"
        data = {'security': 'low', 'seclev_submit': 'Submit'}
        r = session.post(security_url, data=data)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✓ Security level change successful")
        
        return True
    else:
        print(f"✗ AUTHENTICATION FAILED")
        print(f"{'='*60}")
        print(f"\nPossible issues:")
        print(f"  1. Wrong username/password")
        print(f"  2. DVWA database not initialized (visit /setup.php)")
        print(f"  3. Case sensitivity in URL (try /DVWA/ vs /dvwa/)")
        print(f"  4. DVWA configuration issue")
        return False

if __name__ == '__main__':
    import sys
    
    # Default values
    base_url = "http://localhost/DVWA"
    username = "admin"
    password = "password"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    if len(sys.argv) > 2:
        username = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    print(f"\n{'#'*60}")
    print(f"# DVWA Authentication Diagnostic Tool")
    print(f"{'#'*60}")
    print(f"\nConfiguration:")
    print(f"  Base URL: {base_url}")
    print(f"  Username: {username}")
    print(f"  Password: {'*' * len(password)}")
    
    # Test access
    if test_dvwa_access(base_url):
        # Test login
        test_dvwa_login(base_url, username, password)
    else:
        print(f"\n✗ Cannot access DVWA - check if container is running")
        print(f"\nTo start DVWA:")
        print(f"  docker start kali-dvwa-1")
        print(f"  # or")
        print(f"  docker ps | grep dvwa")
