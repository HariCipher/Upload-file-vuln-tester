# ✅ Installation Checklist — Upload File Vuln Tester v2.0

## 📋 Step-by-Step Installation

### Step 1: Download All Files from Claude

**13 files total — organized by location:**

#### Root Directory (6 files)
- [ ] `upload_tester.py` — Main script
- [ ] `requirements.txt` — Dependencies  
- [ ] `LICENSE` — MIT License
- [ ] `README.md` — Main documentation
- [ ] `USAGE.md` — Usage guide
- [ ] `CHANGELOG.md` — Version history
- [ ] `UPGRADE_GUIDE.md` — This upgrade guide

#### modules/ Directory (6 files)
- [ ] `modules/__init__.py` — Package init
- [ ] `modules/bypass_techniques.py` — Bypass methods
- [ ] `modules/payload_generator.py` — Payload creation
- [ ] `modules/session_handler.py` — Authentication
- [ ] `modules/waf_detector.py` — WAF detection
- [ ] `modules/reporter.py` — Report generation

#### Auto-Created Directories (empty for now)
- [ ] `payloads/` — Will be created on first run
- [ ] `payloads/polymorphic/` — Will be created on first run
- [ ] `reports/` — Will be created on first run

---

### Step 2: Set Up GitHub Repo Structure

```bash
# Navigate to your repo
cd ~/path/to/Upload-file-vuln-tester

# Option A: Clean upgrade (recommended)
# Backup v1.0 first
git checkout -b v1-backup
git push origin v1-backup

# Return to main and remove old files
git checkout main
rm -rf *.py *.md shell.php screenshots/ 2>/dev/null

# Create new structure
mkdir -p modules payloads/polymorphic reports

# Copy all 13 files into correct locations:
# Root files → repo root
# Module files → modules/
# Leave payloads/ and reports/ empty

# Option B: Side-by-side (keep v1.0)
mkdir v2
# Put all files in v2/ folder instead
```

---

### Step 3: Verify File Structure

```bash
# Your repo should look like this:
Upload-file-vuln-tester/
├── CHANGELOG.md
├── LICENSE
├── README.md
├── UPGRADE_GUIDE.md
├── USAGE.md
├── requirements.txt
├── upload_tester.py
├── modules/
│   ├── __init__.py
│   ├── bypass_techniques.py
│   ├── payload_generator.py
│   ├── reporter.py
│   ├── session_handler.py
│   └── waf_detector.py
├── payloads/
│   └── polymorphic/
└── reports/
```

---

### Step 4: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
# Should show:
# - requests>=2.28.0
# - colorama>=0.4.6
```

---

### Step 5: Make Script Executable (Linux/Mac)

```bash
chmod +x upload_tester.py
```

---

### Step 6: Test Installation

```bash
# Test 1: Check help works
python upload_tester.py --help

# Expected: Should show full help menu with all options

# Test 2: Verify modules load
python -c "from modules import *; print('✓ All modules loaded')"

# Expected: ✓ All modules loaded
```

---

### Step 7: Test Against DVWA

```bash
# Make sure DVWA is running in your home lab
docker ps | grep dvwa

# If not running:
docker start kali-dvwa-1

# Run first scan
python upload_tester.py http://localhost/DVWA/vulnerabilities/upload/ \
  --base http://localhost/DVWA/ \
  --dvwa-login \
  --security-level low \
  --verify-rce \
  --report \
  --verbose
```

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║  File Upload Vulnerability Tester v2.0                        ║
║  Advanced Security Testing Tool                               ║
║  Author: Harilal P | GitHub: @HariCipher                      ║
╚═══════════════════════════════════════════════════════════════╝

[*] Detecting WAF...
[✓] No WAF detected

[*] Authenticating to DVWA...
[✓] Authentication successful
[✓] Security level set to: low

[*] Generating payloads...
[✓] Generated 5 payload types

[*] Running vulnerability tests...
[✓] VULNERABLE: Double Extension
    Filename: shell.php.jpg
    ...
```

---

### Step 8: Verify Reports Generated

```bash
# Check reports directory
ls -la reports/

# Should see:
# - scan_report_TIMESTAMP.json
# - scan_report_TIMESTAMP.html

# Open HTML report
firefox reports/scan_report_*.html  # Linux
open reports/scan_report_*.html     # macOS
start reports/scan_report_*.html    # Windows
```

---

### Step 9: Commit to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "🚀 Major upgrade to v2.0

- 20+ bypass techniques (extensions, null bytes, path traversal)
- Multi-payload support (PHP, ASP, ASPX, JSP + polymorphic)
- WAF detection (Cloudflare, ModSecurity, AWS, Imperva, etc.)
- Session management (DVWA + custom login)
- Multi-threaded concurrent scanning
- Professional JSON/HTML reports
- Colored terminal UI
- Comprehensive documentation
- 1,200+ lines production-quality code

Complete rewrite from v1.0 simple tool to production-grade pentesting framework."

# Push to GitHub
git push origin main

# Create release tag
git tag -a v2.0.0 -m "Release v2.0.0 - Feature-rich pentesting tool"
git push origin v2.0.0
```

---

### Step 10: Add Screenshots (Important!)

Take these 5 screenshots and add to README:

**1. Tool Banner**
```bash
python upload_tester.py --help | head -20
# Screenshot the colored banner
```

**2. Successful Scan**
```bash
# Run full DVWA scan
# Screenshot terminal showing vulnerabilities found
```

**3. HTML Report**
```bash
# Open generated HTML in browser
# Screenshot the professional report
```

**4. WAF Detection** (if you have access to Cloudflare site)
```bash
# Test against protected site
# Screenshot WAF detection output
```

**5. Multi-threading**
```bash
python upload_tester.py ... --threads 10 --verbose
# Screenshot parallel execution
```

**Add screenshots to repo:**
```bash
mkdir screenshots
# Save images as:
# - screenshots/banner.png
# - screenshots/scan-results.png
# - screenshots/html-report.png
# - screenshots/waf-detection.png
# - screenshots/multi-thread.png

# Update README.md to embed images
git add screenshots/
git commit -m "Add project screenshots"
git push origin main
```

---

## ✅ Verification Checklist

- [ ] All 13 files downloaded from Claude
- [ ] Files organized in correct directory structure
- [ ] `requirements.txt` dependencies installed
- [ ] `upload_tester.py` is executable
- [ ] Help menu displays correctly
- [ ] Modules import without errors
- [ ] DVWA scan completes successfully
- [ ] JSON report generated
- [ ] HTML report generated and opens in browser
- [ ] All files committed to GitHub
- [ ] v2.0.0 release tag created
- [ ] Screenshots added to README
- [ ] LinkedIn/resume updated with v2.0 description

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'modules'"

**Solution:**
```bash
# Make sure you're running from repo root
cd Upload-file-vuln-tester
python upload_tester.py --help

# Verify __init__.py exists
ls modules/__init__.py
```

### Issue: "colorama not found"

**Solution:**
```bash
pip install colorama
```

### Issue: DVWA login fails

**Solution:**
```bash
# Check DVWA is accessible
curl -I http://localhost/DVWA/

# Verify credentials
# Default: admin / password

# If needed, reset DVWA database
# Visit: http://localhost/DVWA/setup.php
```

### Issue: No payloads generated

**Solution:**
```bash
# Payloads are auto-generated on first run
# Check permissions
ls -la payloads/

# If empty, run once to generate
python upload_tester.py http://test.com --base http://test.com
# (It will fail but create payloads)
```

---

## 📞 Need Help?

- **GitHub Issues:** [Report bugs here](https://github.com/HariCipher/Upload-file-vuln-tester/issues)
- **Email:** thisisharilal@gmail.com
- **This Chat:** Ask me any questions about setup!

---

## 🎉 You're Done!

**Your tool is now:**
✅ Fully upgraded to v2.0  
✅ Production-ready  
✅ Portfolio-grade  
✅ Resume-worthy  
✅ Ready for internship applications  

**Next:** Test it thoroughly, add screenshots, and share on LinkedIn! 🚀
