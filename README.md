# 🔐 File Upload Vulnerability Tester v2.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/HariCipher/Upload-file-vuln-tester/graphs/commit-activity)

**Advanced penetration testing tool for identifying file upload vulnerabilities in web applications**

Designed for bug bounty hunters, security researchers, and penetration testers to automate the detection of insecure file upload implementations.

---

## 🎯 What's New in v2.0

### Major Upgrades from v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| **Bypass Techniques** | ❌ Basic upload only | ✅ 20+ bypass methods |
| **Payload Types** | ❌ PHP only | ✅ PHP, ASP, ASPX, JSP + polymorphic |
| **Authentication** | ❌ None | ✅ DVWA + custom login support |
| **WAF Detection** | ❌ None | ✅ Cloudflare, ModSecurity, AWS WAF, etc. |
| **Multi-threading** | ❌ Sequential | ✅ Concurrent testing |
| **RCE Verification** | ✅ Basic | ✅ Advanced with multiple commands |
| **Reports** | ❌ None | ✅ JSON + HTML with styling |
| **Output** | ❌ Plain text | ✅ Colored terminal UI |

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Bypass Techniques](#-bypass-techniques-implemented)
- [Payload Types](#-payload-types)
- [Report Samples](#-report-samples)
- [Roadmap](#-roadmap)
- [Legal Disclaimer](#-legal-disclaimer)
- [Contributing](#-contributing)
- [Author](#-author)

---

## ✨ Features

### Core Capabilities

- ✅ **20+ Bypass Techniques** — Double extensions, null bytes, case variations, path traversal, Unicode tricks
- ✅ **Multi-payload Support** — PHP, ASP, ASPX, JSP, plus polymorphic variants
- ✅ **WAF Detection** — Identifies Cloudflare, ModSecurity, AWS WAF, Imperva, Akamai, F5, and more
- ✅ **Session Management** — Authenticate to DVWA or custom apps before testing
- ✅ **RCE Verification** — Automatically verify if uploaded shells are executable
- ✅ **Multi-threaded Scanning** — Parallel testing for faster results
- ✅ **Professional Reports** — JSON + HTML reports with vulnerability details
- ✅ **Colored Output** — Beautiful terminal UI with status indicators

### Advanced Features

- 🔍 **Smart Path Discovery** — Tests 12+ common upload directories
- 🛡️ **WAF Bypass Suggestions** — Recommendations based on detected firewall
- 🔄 **Polymorphic Payloads** — Auto-generated obfuscated shells to evade signatures
- 📊 **Detailed Logging** — Track all upload attempts and responses
- ⚙️ **Flexible Configuration** — Customize every aspect via CLI arguments

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/HariCipher/Upload-file-vuln-tester.git
cd Upload-file-vuln-tester

# Install dependencies
pip install -r requirements.txt

# Make executable (Linux/Mac)
chmod +x upload_tester.py
```

---

## ⚡ Quick Start

### Basic Scan

```bash
python upload_tester.py http://target.com/upload.php --base http://target.com
```

### DVWA Testing (Recommended for Learning)

```bash
python upload_tester.py http://localhost/vulnerabilities/upload/ \
  --base http://localhost/ \
  --dvwa-login \
  --security-level low \
  --verify-rce \
  --report
```

### Advanced Scan with All Features

```bash
python upload_tester.py http://target.com/upload.php \
  --base http://target.com \
  --threads 5 \
  --payload-type php_poly \
  --verify-rce \
  --report \
  --verbose
```

---

## 📚 Usage Examples

### 1. Testing DVWA (Damn Vulnerable Web App)

Perfect for practicing and learning:

```bash
# Low security
python upload_tester.py http://localhost/vulnerabilities/upload/ \
  --base http://localhost/ \
  --dvwa-login \
  --username admin \
  --password password \
  --security-level low \
  --verify-rce \
  --report

# Medium security (more restricted)
python upload_tester.py http://localhost/vulnerabilities/upload/ \
  --base http://localhost/ \
  --dvwa-login \
  --security-level medium \
  --threads 3 \
  --report
```

### 2. Testing Custom Web Application

```bash
python upload_tester.py https://example.com/admin/upload \
  --base https://example.com \
  --custom-login https://example.com/login \
  --credentials "username=admin,password=secret123" \
  --success-indicator "dashboard" \
  --field-name "file" \
  --verify-rce \
  --report \
  --verbose
```

### 3. Bug Bounty Hunting

```bash
# Stealthy scan - single thread, no RCE verification
python upload_tester.py https://target.com/upload \
  --base https://target.com \
  --threads 1 \
  --payload-type php \
  --report

# Aggressive scan - multiple threads with all checks
python upload_tester.py https://target.com/upload \
  --base https://target.com \
  --threads 10 \
  --payload-type php_poly \
  --verify-rce \
  --report \
  --verbose
```

### 4. Testing with WAF Present

```bash
python upload_tester.py https://protected-site.com/upload \
  --base https://protected-site.com \
  --ignore-waf \
  --threads 1 \
  --payload-type php_poly \
  --report
```

---

## 🔓 Bypass Techniques Implemented

### Extension-Based Bypasses

1. **Double Extension** — `shell.php.jpg`
2. **Reverse Double Extension** — `shell.jpg.php`
3. **Case Variation** — `shell.pHp`, `shell.PhP`, `shell.PHP`
4. **Alternative Extensions** — `shell.php3`, `shell.php4`, `shell.php5`, `shell.phtml`, `shell.phps`

### Special Character Bypasses

5. **Null Byte Injection** — `shell.php%00.jpg`
6. **Null Byte Alternative** — `shell%00.php`
7. **Trailing Dot** — `shell.php.` (Windows truncation)
8. **Trailing Space** — `shell.php ` (space after extension)
9. **Multiple Dots** — `shell.php..jpg`

### Advanced Bypasses

10. **Path Traversal** — `../../shell.php`
11. **Windows Path Traversal** — `..\\..\\shell.php`
12. **Unicode Right-to-Left Override** — Uses U+202E character
13. **MIME Type Fuzzing** — Tests 7+ different MIME types per file

---

## 💉 Payload Types

### Available Shells

| Type | Server | Description |
|------|--------|-------------|
| **php** | Apache/Nginx with PHP | Standard PHP webshell with `system()` |
| **asp** | IIS (Classic ASP) | VBScript-based shell |
| **aspx** | IIS with .NET | C# ASP.NET webshell |
| **jsp** | Tomcat/JBoss | Java Server Pages shell |
| **php_poly** | Apache/Nginx with PHP | Polymorphic obfuscated PHP shell |

### Payload Structure

All payloads accept commands via `?cmd=` parameter:

```bash
# After successful upload
curl "http://target.com/uploads/shell.php?cmd=whoami"
curl "http://target.com/uploads/shell.php?cmd=id"
curl "http://target.com/uploads/shell.php?cmd=ls"
```

---

## 📊 Report Samples

### JSON Report Structure

```json
{
  "scan_info": {
    "target": "http://localhost/vulnerabilities/upload/",
    "start_time": "2026-03-26 14:30:00",
    "payloads_tested": 24,
    "tool": "Upload-File-Vuln-Tester v2.0"
  },
  "vulnerabilities": [
    {
      "technique": "Double Extension",
      "filename": "shell.php.jpg",
      "upload_url": "http://localhost/vulnerabilities/upload/",
      "file_url": "http://localhost/hackable/uploads/shell.php.jpg",
      "rce_verified": true,
      "rce_output": "www-data"
    }
  ],
  "summary": {
    "total_tests": 24,
    "successful_uploads": 3,
    "failed_uploads": 21,
    "vulnerability_found": true,
    "severity": "Critical"
  },
  "recommendations": [
    "Implement strict file type validation based on file content",
    "Store uploaded files outside the web root directory",
    "Use a whitelist of allowed file extensions"
  ]
}
```

### HTML Report

Beautiful, professional HTML reports with:
- Executive summary with severity badges
- Detailed vulnerability listings
- Interactive sections
- Security recommendations
- Timestamp and metadata

**Screenshot Preview:**

![Report Sample](assets/web-report.png) 

---

## 🎓 Educational Use Cases

### For Students

- 🎯 **CTF Practice** — Test file upload challenges in competitions
- 📚 **Learning Platform** — Understand common bypass techniques
- 🔬 **Lab Environment** — Practice on DVWA, bWAPP, WebGoat

### For Professionals

- 🐛 **Bug Bounty** — Automate initial file upload testing
- 🔐 **Penetration Testing** — Include in web app assessment workflow
- 📋 **Compliance Testing** — Verify upload security controls

---

## 🛣️ Roadmap

### Version 2.1 (Planned)

- [ ] Integration with Burp Suite
- [ ] Support for GraphQL file uploads
- [ ] Machine learning-based pattern detection
- [ ] Docker containerization
- [ ] CI/CD pipeline integration

### Version 3.0 (Future)

- [ ] Web-based UI dashboard
- [ ] Database integration for historical tracking
- [ ] API endpoint for programmatic access
- [ ] Plugin system for custom bypass techniques

---

## 🛡️ Legal Disclaimer

This tool is intended for **authorized security testing only**.

### You Must:

✅ Have explicit written permission to test the target  
✅ Only use on systems you own or have authorization to test  
✅ Follow responsible disclosure practices  
✅ Comply with local laws and regulations

### You Must Not:

❌ Use against systems without permission  
❌ Use for malicious purposes  
❌ Deploy uploaded shells on production systems  
❌ Ignore the ethical boundaries of security research

**The author assumes no liability for misuse of this tool.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. 🐛 **Report Bugs** — Open an issue with reproduction steps
2. 💡 **Suggest Features** — Share ideas for improvements
3. 🔧 **Submit PRs** — Add new bypass techniques or payloads
4. 📝 **Improve Docs** — Help make documentation clearer
5. ⭐ **Star the Repo** — Show your support

### Contribution Guidelines

```bash
# Fork the repo
# Create a feature branch
git checkout -b feature/new-bypass-technique

# Make your changes
# Test thoroughly
python upload_tester.py --help

# Commit with clear messages
git commit -m "Add MIME type bypass technique"

# Push and create PR
git push origin feature/new-bypass-technique
```

---

## 👨‍💻 Author

**Harilal P**

- 🎓 B.Tech Computer Science Engineering Student
- 🔐 Cybersecurity Enthusiast | SOC Analyst Track
- 🌐 GitHub: [@HariCipher](https://github.com/HariCipher) / [@sideEffect7](https://github.com/sideEffect7)
- 💼 LinkedIn: [Harilal P](https://www.linkedin.com/in/thisisharilal/)
- 📧 Email: thisisharilal@gmail.com

### Other Security Projects

- [Home-SOC-Lab](https://github.com/HariCipher/Home-SOC-Lab) — Complete SOC + Pentesting lab setup
- More coming soon...

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- **OWASP** — For security research and testing frameworks
- **DVWA Team** — For providing an excellent learning platform
- **Bug Bounty Community** — For continuous knowledge sharing
- **Cybersecurity Researchers** — For developing bypass techniques

---

## ⭐ Star History

If this tool helped you, consider giving it a star! 

[![Star History Chart](https://api.star-history.com/svg?repos=HariCipher/Upload-file-vuln-tester&type=Date)](https://star-history.com/#HariCipher/Upload-file-vuln-tester&Date)

---

<div align="center">

**Built with ❤️ for the cybersecurity community**

[Report Bug](https://github.com/HariCipher/Upload-file-vuln-tester/issues) · [Request Feature](https://github.com/HariCipher/Upload-file-vuln-tester/issues) · [Documentation](https://github.com/HariCipher/Upload-file-vuln-tester/wiki)

</div>
