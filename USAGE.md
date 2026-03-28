# Usage Guide

Comprehensive guide for using the File Upload Vulnerability Tester v2.0

---

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Command-Line Arguments](#command-line-arguments)
4. [Testing Scenarios](#testing-scenarios)
5. [Understanding Reports](#understanding-reports)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Installation

### System Requirements

- Python 3.8 or higher
- Linux, macOS, or Windows
- Internet connection for initial setup

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/HariCipher/Upload-file-vuln-tester.git
cd Upload-file-vuln-tester

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python upload_tester.py --help
```

---

## Basic Usage

### Minimal Command

The simplest scan requires just two arguments:

```bash
python upload_tester.py <UPLOAD_URL> --base <BASE_URL>
```

**Example:**
```bash
python upload_tester.py http://target.com/upload.php --base http://target.com
```

This will:
- Detect WAF presence
- Test 20+ bypass techniques
- Use default PHP payload
- Check common upload directories
- Display results in terminal

### Recommended Command

For comprehensive testing:

```bash
python upload_tester.py http://target.com/upload.php \
  --base http://target.com \
  --verify-rce \
  --report \
  --verbose
```

This adds:
- RCE verification attempts
- JSON and HTML report generation
- Detailed output of all tests

---

## Command-Line Arguments

### Required Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `target_url` | URL of upload endpoint | `http://target.com/upload.php` |
| `--base URL` | Base URL for file checking | `http://target.com` |

### Authentication Options

| Argument | Description | Example |
|----------|-------------|---------|
| `--dvwa-login` | Enable DVWA authentication | *flag only* |
| `--username USER` | DVWA username | `--username admin` |
| `--password PASS` | DVWA password | `--password password` |
| `--security-level LEVEL` | Set DVWA security | `--security-level low` |
| `--custom-login URL` | Custom login URL | `--custom-login http://app.com/login` |
| `--credentials CREDS` | Custom credentials | `--credentials "user=admin,pass=secret"` |
| `--success-indicator STR` | Login success string | `--success-indicator dashboard` |

### Scan Options

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--field-name NAME` | Upload form field | `uploaded` | `--field-name file` |
| `--payload-type TYPE` | Shell type | `php` | `--payload-type aspx` |
| `--threads N` | Concurrent threads | `1` | `--threads 5` |
| `--verify-rce` | Test code execution | *disabled* | `--verify-rce` |

**Available Payload Types:**
- `php` — Standard PHP webshell
- `asp` — Classic ASP shell
- `aspx` — ASP.NET shell
- `jsp` — Java Server Pages shell
- `php_poly` — Polymorphic obfuscated PHP

### WAF Options

| Argument | Description |
|----------|-------------|
| `--skip-waf` | Skip WAF detection phase |
| `--ignore-waf` | Continue even if WAF detected |

### Output Options

| Argument | Description |
|----------|-------------|
| `--report` | Generate JSON and HTML reports |
| `--verbose` or `-v` | Show detailed output |
| `--force` | Force scan past warnings |

---

## Testing Scenarios

### Scenario 1: Testing DVWA (Learning Environment)

**Low Security Level:**
```bash
python upload_tester.py http://localhost/DVWA/vulnerabilities/upload/ \
  --base http://localhost/DVWA/ \
  --dvwa-login \
  --username admin \
  --password password \
  --security-level low \
  --verify-rce \
  --report \
  --verbose
```

**Expected Result:** Multiple vulnerabilities found (double extensions, case variations)

**Medium Security Level:**
```bash
python upload_tester.py http://localhost/DVWA/vulnerabilities/upload/ \
  --base http://localhost/DVWA/ \
  --dvwa-login \
  --security-level medium \
  --threads 3 \
  --verify-rce \
  --report
```

**Expected Result:** Fewer bypasses work (MIME type checks in place)

### Scenario 2: Bug Bounty Testing

**Initial Reconnaissance:**
```bash
# Stealthy single-threaded scan
python upload_tester.py https://target.com/profile/avatar \
  --base https://target.com \
  --field-name avatar \
  --threads 1 \
  --report
```

**Aggressive Testing (if allowed):**
```bash
python upload_tester.py https://target.com/profile/avatar \
  --base https://target.com \
  --field-name avatar \
  --threads 10 \
  --payload-type php_poly \
  --verify-rce \
  --report \
  --verbose
```

### Scenario 3: Authenticated Application Testing

**Custom Login Example:**
```bash
python upload_tester.py https://webapp.com/admin/upload \
  --base https://webapp.com \
  --custom-login https://webapp.com/auth/login \
  --credentials "email=admin@test.com,password=Test123!" \
  --success-indicator "Dashboard" \
  --field-name document \
  --verify-rce \
  --report
```

### Scenario 4: Testing Behind WAF

```bash
python upload_tester.py https://protected.com/upload \
  --base https://protected.com \
  --payload-type php_poly \
  --threads 1 \
  --ignore-waf \
  --report
```

**Tip:** Polymorphic payloads help evade signature-based WAFs

---

## Understanding Reports

### JSON Report Structure

Located in `reports/scan_report_TIMESTAMP.json`

```json
{
  "scan_info": {
    "target": "Upload URL",
    "start_time": "Scan timestamp",
    "payloads_tested": 24,
    "tool": "Tool version"
  },
  "vulnerabilities": [
    {
      "technique": "Bypass method used",
      "filename": "Uploaded filename",
      "upload_url": "Form endpoint",
      "file_url": "Accessible location",
      "rce_verified": true,
      "rce_output": "Command output"
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
    "Security advice..."
  ]
}
```

### HTML Report

Located in `reports/scan_report_TIMESTAMP.html`

**Features:**
- Executive summary with severity badges
- Detailed vulnerability cards
- Interactive sections
- Security recommendations
- Professional styling

**Opening Reports:**
```bash
# Linux
xdg-open reports/scan_report_*.html

# macOS
open reports/scan_report_*.html

# Windows
start reports/scan_report_*.html
```

---

## Troubleshooting

### Common Issues

#### Issue: "No vulnerabilities found" but upload works

**Possible Causes:**
- Files stored in non-standard directory
- File renamed after upload
- Base URL incorrect

**Solutions:**
```bash
# Try different base URLs
python upload_tester.py http://target.com/upload.php --base http://target.com/files/
python upload_tester.py http://target.com/upload.php --base http://cdn.target.com/

# Enable verbose mode to see tested paths
python upload_tester.py http://target.com/upload.php --base http://target.com --verbose
```

#### Issue: "Authentication failed"

**Solutions:**
```bash
# Verify credentials manually first
# Check if CAPTCHA is present (tool can't bypass)
# Use --verbose to see authentication attempt details

# For DVWA, ensure database is set up
# Access http://localhost/DVWA/setup.php first
```

#### Issue: "Connection timeout" or "SSL errors"

**Solutions:**
```bash
# Increase timeout (modify code in session_handler.py)
# For SSL issues on local testing:
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

#### Issue: WAF blocks all attempts

**Solutions:**
```bash
# Use polymorphic payload
--payload-type php_poly

# Single-threaded to avoid rate limiting
--threads 1

# Add delays between requests (modify code)
```

---

## Best Practices

### Before Testing

1. ✅ **Get Written Permission** — Always obtain authorization
2. ✅ **Read Scope** — Understand what's allowed
3. ✅ **Test on Staging** — Use non-production environments when possible
4. ✅ **Document Everything** — Keep records of authorization and findings

### During Testing

1. ✅ **Start Conservative** — Use `--threads 1` initially
2. ✅ **Monitor Server Response** — Watch for 429/503 errors
3. ✅ **Use Appropriate Payloads** — Match server technology (PHP, ASP, etc.)
4. ✅ **Enable Reporting** — Always use `--report` for documentation

### After Testing

1. ✅ **Clean Up** — Remove uploaded shells immediately
2. ✅ **Document Findings** — Use generated reports for evidence
3. ✅ **Responsible Disclosure** — Follow proper reporting channels
4. ✅ **Share Knowledge** — Help improve defenses

### Recommended Testing Flow

```bash
# 1. Initial recon
python upload_tester.py <URL> --base <BASE> --report

# 2. If vulnerabilities found, verify with RCE
python upload_tester.py <URL> --base <BASE> --verify-rce --report

# 3. Test different payload types
python upload_tester.py <URL> --base <BASE> --payload-type aspx --report

# 4. Clean up uploaded files manually via browser
```

---

## Advanced Tips

### Custom Upload Paths

Edit `upload_tester.py` to add custom paths:

```python
COMMON_PATHS = [
    "uploads/", 
    "custom/path/",  # Add your path here
    "app/storage/",
]
```

### Modify Polymorphic Payload

Edit `modules/payload_generator.py` to customize obfuscation:

```python
def generate_polymorphic_php(self) -> str:
    # Add your obfuscation techniques here
```

### Integration with Burp Suite

```bash
# Set proxy in session_handler.py
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}
```

---

## Getting Help

- 📖 **Documentation**: Check README.md and this guide
- 🐛 **Issues**: [GitHub Issues](https://github.com/HariCipher/Upload-file-vuln-tester/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/HariCipher/Upload-file-vuln-tester/discussions)
- 📧 **Email**: thisisharilal@gmail.com

---

**Remember: With great tools comes great responsibility. Always test ethically.**
