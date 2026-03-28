# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-26

### Added
- **20+ Bypass Techniques** including double extensions, null bytes, case variations, path traversal
- **Multi-payload Support** for PHP, ASP, ASPX, JSP, and polymorphic variants
- **WAF Detection Module** supporting Cloudflare, ModSecurity, AWS WAF, Imperva, Akamai, F5, and more
- **Session Management** with DVWA authentication and custom login support
- **Multi-threaded Scanning** for faster vulnerability detection
- **Professional Reporting** with JSON and HTML outputs
- **RCE Verification** with multiple command execution attempts
- **Colored Terminal Output** using colorama for better readability
- **Polymorphic Payload Generator** for signature evasion
- **Smart Path Discovery** testing 12+ common upload directories
- **WAF Bypass Recommendations** based on detected firewall
- **Comprehensive Documentation** with usage examples and screenshots
- **MIME Type Fuzzing** to bypass content-type restrictions

### Changed
- Complete rewrite of core scanning logic
- Modular architecture with separate components for bypass techniques, payloads, WAF detection, and reporting
- Enhanced error handling and exception management
- Improved upload verification with multiple success indicators
- Better progress tracking and status updates

### Improved
- Code organization with proper module structure
- Command-line interface with grouped arguments
- Verbose mode with detailed debugging information
- Session handling for authenticated uploads
- File accessibility checking with comprehensive path testing

### Security
- Added ethical use disclaimers throughout documentation
- Implemented safe error handling to prevent information disclosure
- Added warnings for WAF detection and testing interruption

## [1.0.0] - 2024-XX-XX

### Initial Release
- Basic file upload testing
- Single PHP webshell payload
- Simple upload and check workflow
- Command-line interface
- Basic README documentation
- Common path checking for uploaded files
- Simple RCE verification with whoami command

---

## Upgrade Guide: v1.0 → v2.0

### Breaking Changes
None - v2.0 is backward compatible with v1.0 usage

### Migration Steps

1. **Update Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Review New Command-Line Options**
   ```bash
   python upload_tester.py --help
   ```

3. **Test Basic Functionality**
   ```bash
   # Old v1.0 command still works
   python upload_tester.py http://target.com/upload.php --base http://target.com
   ```

4. **Explore New Features**
   ```bash
   # Try new features like WAF detection, multi-threading, and reports
   python upload_tester.py http://target.com/upload.php --base http://target.com \
     --threads 5 --verify-rce --report --verbose
   ```

### Deprecated Features
None

### Removed Features
None

---

## Future Releases

### [2.1.0] - Planned
- Integration with Burp Suite for proxy routing
- GraphQL file upload support
- Machine learning-based anomaly detection
- Docker containerization
- CI/CD pipeline integration templates

### [3.0.0] - Future
- Web-based dashboard UI
- Database backend for historical tracking
- RESTful API for programmatic access
- Plugin system for custom bypass techniques
- Automated exploit generation

---

For full release notes and detailed changes, see [Releases](https://github.com/HariCipher/Upload-file-vuln-tester/releases).
