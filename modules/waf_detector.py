"""
WAF Detection Module
Identifies common Web Application Firewalls that may block testing
"""

import requests
from typing import Dict, Optional

class WAFDetector:
    """Detect common WAF solutions"""
    
    WAF_SIGNATURES = {
        'Cloudflare': ['__cfduid', 'cf-ray', 'cloudflare'],
        'AWS WAF': ['x-amzn-requestid', 'x-amz-cf-id'],
        'ModSecurity': ['mod_security', 'NOYB'],
        'Sucuri': ['sucuri', 'x-sucuri-id'],
        'Imperva': ['incap_ses', 'visid_incap', 'imperva'],
        'F5 BIG-IP': ['BigIP', 'F5', 'TS[a-zA-Z0-9]{3,6}'],
        'Akamai': ['akamai', 'ak_bmsc'],
        'Barracuda': ['barra', 'barracuda'],
        'Citrix NetScaler': ['ns_af', 'citrix_ns_id', 'NSC_'],
        'DenyAll': ['sessioncookie', 'denyall'],
        'FortiWeb': ['FORTIWAFSID', 'fortiweb'],
        'Azure Front Door': ['x-azure-ref', 'x-fd-healthprobe'],
    }
    
    def __init__(self):
        self.detected_waf = None
        
    def detect(self, url: str, session: Optional[requests.Session] = None) -> Dict[str, any]:
        """
        Detect WAF presence by analyzing HTTP headers and responses
        
        Args:
            url: Target URL to test
            session: Optional requests session object
            
        Returns:
            Dict with detection results
        """
        results = {
            'waf_detected': False,
            'waf_name': None,
            'confidence': 'low',
            'indicators': []
        }
        
        try:
            # Use provided session or create new one
            req_session = session if session else requests.Session()
            
            # Send test request
            response = req_session.get(url, timeout=10)
            
            # Check headers
            headers = response.headers
            cookies = response.cookies
            
            # Analyze headers for WAF signatures
            for waf_name, signatures in self.WAF_SIGNATURES.items():
                for signature in signatures:
                    # Check in headers
                    for header_name, header_value in headers.items():
                        if signature.lower() in header_name.lower() or \
                           signature.lower() in str(header_value).lower():
                            results['waf_detected'] = True
                            results['waf_name'] = waf_name
                            results['confidence'] = 'high'
                            results['indicators'].append(f"Header: {header_name}")
                            self.detected_waf = waf_name
                            return results
                    
                    # Check in cookies
                    for cookie in cookies:
                        if signature.lower() in cookie.name.lower():
                            results['waf_detected'] = True
                            results['waf_name'] = waf_name
                            results['confidence'] = 'high'
                            results['indicators'].append(f"Cookie: {cookie.name}")
                            self.detected_waf = waf_name
                            return results
            
            # Check for generic WAF behavior
            if response.status_code in [403, 406, 419, 429, 501]:
                # Send malicious payload to trigger WAF
                test_payloads = [
                    "?id=1' OR '1'='1",
                    "?cmd=cat /etc/passwd",
                    "/../../../etc/passwd"
                ]
                
                for payload in test_payloads:
                    try:
                        test_response = req_session.get(url + payload, timeout=5)
                        if test_response.status_code in [403, 406, 419, 429, 501]:
                            results['waf_detected'] = True
                            results['waf_name'] = 'Generic WAF'
                            results['confidence'] = 'medium'
                            results['indicators'].append(f"Blocked status code: {test_response.status_code}")
                            self.detected_waf = 'Generic WAF'
                            return results
                    except:
                        continue
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            return results
    
    def get_bypass_recommendations(self) -> list:
        """
        Suggest bypass techniques based on detected WAF
        
        Returns:
            List of bypass suggestions
        """
        if not self.detected_waf:
            return ["No WAF detected - proceed with standard testing"]
        
        recommendations = {
            'Cloudflare': [
                "Try obfuscating payloads with encoding",
                "Use time-based delays between requests",
                "Consider IP rotation if rate-limited",
                "Test with different User-Agent strings"
            ],
            'ModSecurity': [
                "Use case variation in payloads",
                "Try null byte injection",
                "Encode special characters",
                "Fragment malicious patterns across multiple parameters"
            ],
            'AWS WAF': [
                "Test with different HTTP methods",
                "Try parameter pollution",
                "Use content-type variation",
                "Consider regional endpoint testing"
            ],
            'Generic WAF': [
                "Start with basic payloads",
                "Gradually increase complexity",
                "Monitor for pattern-based blocking",
                "Try encoding variations"
            ]
        }
        
        return recommendations.get(self.detected_waf, recommendations['Generic WAF'])
