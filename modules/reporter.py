"""
Reporter Module
Generates JSON and HTML reports of vulnerability testing results
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class Reporter:
    """Generate professional vulnerability reports"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = {
            'scan_info': {},
            'vulnerabilities': [],
            'summary': {},
            'recommendations': []
        }
        
    def add_scan_info(self, target_url: str, start_time: str, payloads_tested: int):
        """Add metadata about the scan"""
        self.results['scan_info'] = {
            'target': target_url,
            'start_time': start_time,
            'payloads_tested': payloads_tested,
            'tool': 'Upload-File-Vuln-Tester v2.0'
        }
    
    def add_vulnerability(self, vuln_data: Dict):
        """Add a discovered vulnerability"""
        self.results['vulnerabilities'].append(vuln_data)
    
    def add_summary(self, total_tests: int, successful: int, failed: int):
        """Add scan summary statistics"""
        self.results['summary'] = {
            'total_tests': total_tests,
            'successful_uploads': successful,
            'failed_uploads': failed,
            'vulnerability_found': successful > 0,
            'severity': 'Critical' if successful > 0 else 'None'
        }
    
    def add_recommendation(self, recommendation: str):
        """Add a security recommendation"""
        self.results['recommendations'].append(recommendation)
    
    def generate_json(self, filename: str = None) -> str:
        """
        Generate JSON report
        
        Returns:
            Path to generated file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_report_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return filepath
    
    def generate_html(self, filename: str = None) -> str:
        """
        Generate HTML report
        
        Returns:
            Path to generated file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_report_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Get vulnerability severity color
        severity_color = {
            'Critical': '#dc3545',
            'High': '#fd7e14',
            'Medium': '#ffc107',
            'Low': '#28a745',
            'None': '#6c757d'
        }
        
        severity = self.results['summary'].get('severity', 'None')
        color = severity_color.get(severity, '#6c757d')
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Vulnerability Scan Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .info-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        
        .info-card label {{
            display: block;
            font-weight: bold;
            color: #666;
            margin-bottom: 5px;
            font-size: 12px;
            text-transform: uppercase;
        }}
        
        .info-card value {{
            font-size: 16px;
            color: #333;
        }}
        
        .severity-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            background: {color};
        }}
        
        .vuln-item {{
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        
        .vuln-item h3 {{
            color: #dc3545;
            margin-bottom: 10px;
        }}
        
        .vuln-detail {{
            display: grid;
            grid-template-columns: 150px 1fr;
            gap: 10px;
            margin: 10px 0;
        }}
        
        .vuln-detail strong {{
            color: #666;
        }}
        
        .code-block {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            margin: 10px 0;
        }}
        
        .recommendation {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
        }}
        
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-box {{
            flex: 1;
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .no-vulns {{
            text-align: center;
            padding: 40px;
            color: #28a745;
        }}
        
        .no-vulns svg {{
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 File Upload Vulnerability Scan Report</h1>
            <p>Generated by Upload-File-Vuln-Tester v2.0</p>
        </div>
        
        <div class="content">
            <!-- Scan Information -->
            <div class="section">
                <h2>Scan Information</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <label>Target URL</label>
                        <value>{self.results['scan_info'].get('target', 'N/A')}</value>
                    </div>
                    <div class="info-card">
                        <label>Scan Started</label>
                        <value>{self.results['scan_info'].get('start_time', 'N/A')}</value>
                    </div>
                    <div class="info-card">
                        <label>Payloads Tested</label>
                        <value>{self.results['scan_info'].get('payloads_tested', 0)}</value>
                    </div>
                    <div class="info-card">
                        <label>Severity</label>
                        <value><span class="severity-badge">{severity}</span></value>
                    </div>
                </div>
            </div>
            
            <!-- Summary Statistics -->
            <div class="section">
                <h2>Summary</h2>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">{self.results['summary'].get('total_tests', 0)}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{self.results['summary'].get('successful_uploads', 0)}</div>
                        <div class="stat-label">Successful Uploads</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{self.results['summary'].get('failed_uploads', 0)}</div>
                        <div class="stat-label">Failed Uploads</div>
                    </div>
                </div>
            </div>
            
            <!-- Vulnerabilities -->
            <div class="section">
                <h2>Discovered Vulnerabilities</h2>
                {''.join(self._generate_vuln_html(v) for v in self.results['vulnerabilities']) if self.results['vulnerabilities'] else '<div class="no-vulns"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg><h3>No Vulnerabilities Found</h3><p>The upload functionality appears to be properly secured.</p></div>'}
            </div>
            
            <!-- Recommendations -->
            {self._generate_recommendations_html()}
        </div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w') as f:
            f.write(html_content)
        
        return filepath
    
    def _generate_vuln_html(self, vuln: Dict) -> str:
        """Generate HTML for a single vulnerability"""
        return f"""
        <div class="vuln-item">
            <h3>✗ {vuln.get('technique', 'File Upload Vulnerability')}</h3>
            <div class="vuln-detail">
                <strong>Upload URL:</strong>
                <span>{vuln.get('upload_url', 'N/A')}</span>
            </div>
            <div class="vuln-detail">
                <strong>File Location:</strong>
                <span>{vuln.get('file_url', 'N/A')}</span>
            </div>
            <div class="vuln-detail">
                <strong>Filename Used:</strong>
                <span>{vuln.get('filename', 'N/A')}</span>
            </div>
            {f'<div class="vuln-detail"><strong>RCE Verified:</strong><span>{"✓ Yes" if vuln.get("rce_verified") else "✗ No"}</span></div>' if 'rce_verified' in vuln else ''}
            {f'<div><strong>Command Output:</strong><div class="code-block">{vuln.get("rce_output", "")}</div></div>' if vuln.get('rce_output') else ''}
        </div>
        """
    
    def _generate_recommendations_html(self) -> str:
        """Generate HTML for recommendations section"""
        if not self.results['recommendations']:
            return ""
        
        recs_html = '<div class="section"><h2>Security Recommendations</h2>'
        for rec in self.results['recommendations']:
            recs_html += f'<div class="recommendation">• {rec}</div>'
        recs_html += '</div>'
        
        return recs_html
    
    def print_summary(self):
        """Print a console summary of results"""
        print("\n" + "="*60)
        print("SCAN SUMMARY")
        print("="*60)
        print(f"Target: {self.results['scan_info'].get('target', 'N/A')}")
        print(f"Total Tests: {self.results['summary'].get('total_tests', 0)}")
        print(f"Successful Uploads: {self.results['summary'].get('successful_uploads', 0)}")
        print(f"Failed Uploads: {self.results['summary'].get('failed_uploads', 0)}")
        print(f"Severity: {self.results['summary'].get('severity', 'None')}")
        print("="*60 + "\n")
