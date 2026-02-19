# File Upload Vulnerability Scanner

![cover-image](https://github.com/0xS4r4n9/ghostupload/blob/main/ghostupload.png)

## 📋 Description

A comprehensive Python-based security tool designed to automatically detect and assess file upload vulnerabilities in web applications. This scanner performs extensive testing across multiple attack vectors to identify potential security weaknesses in file upload functionality.

**Created by**: 0xS4r4n9  
**Version**: 1.0.0  
**License**: MIT

## 🎯 Features

### Comprehensive Testing Phases

1. **Capability Discovery (Phase 0)**
   - Automatic detection of file upload forms
   - Analysis of form structure and requirements
   - Detection of AJAX/API upload endpoints
   - CSRF token identification
   - Required field mapping

2. **Extension Validation Bypass (Phase 1)**
   - Double extension attacks (e.g., shell.php.jpg)
   - Trailing character manipulation (dots, spaces)
   - Case manipulation bypass
   - Null byte injection
   - Unicode lookalike characters
   - Alternative dangerous extensions (php5, phtml, phar)
   - Long filename attacks

3. **MIME Type Spoofing (Phase 2)**
   - Content-Type header manipulation
   - MIME type mismatch testing
   - Generic MIME type acceptance
   - Server-side script masquerading as images

4. **Magic Bytes Bypass (Phase 3)**
   - Polyglot file creation
   - Valid image headers with embedded payloads
   - GIF/PNG/JPEG header injection
   - Structural validation bypass

5. **Stored XSS Detection (Phase 5)**
   - SVG with embedded scripts
   - HTML file upload with JavaScript
   - Event handler injection
   - SVG onload attacks

6. **Path Traversal Testing (Phase 6)**
   - Unix-style path traversal (../)
   - Windows-style path traversal (..\\)
   - URL-encoded traversal
   - Double encoding bypass
   - Webroot escape attempts

7. **File Overwrite Detection (Phase 7)**
   - Critical file overwrite testing
   - Index page replacement
   - Configuration file targeting
   - .htaccess manipulation

8. **File Size Limit Testing (Phase 9)**
   - Progressive size testing
   - DoS potential assessment
   - Upload time measurement
   - Size restriction validation

9. **Security Header Analysis (Phase 12)**
   - Content-Disposition validation
   - X-Content-Type-Options checking
   - X-Frame-Options verification
   - CSP header detection

### Additional Features

- **Colorized Output**: Easy-to-read terminal output with severity-based color coding
- **Detailed Reporting**: Comprehensive vulnerability reports in both text and JSON formats
- **Smart Detection**: Intelligent success/failure detection based on response patterns
- **Session Management**: Maintains session state throughout testing
- **Error Handling**: Robust error handling with optional verbose mode
- **Extensible Design**: Easy to add new test cases and attack vectors

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

**Note**: All dependencies are pure Python packages with no system library requirements, making installation straightforward on all platforms.

### Setup

1. **Clone or download the project**:
```bash
cd file-upload-scanner
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Make the script executable** (Linux/Mac):
```bash
chmod +x upload_scanner.py
```

### Dependencies

- `requests`: HTTP library for making requests
- `beautifulsoup4`: HTML parsing and form detection
- `colorama`: Cross-platform colored terminal output
- `lxml`: Fast XML/HTML parser
- `urllib3`: URL handling utilities

## 📖 Usage

### Basic Usage

```bash
python upload_scanner.py -u http://target.com/upload
```

### Advanced Usage

```bash
# With verbose output
python upload_scanner.py -u http://target.com/upload -v

# Save report to file
python upload_scanner.py -u http://target.com/upload -o report.txt

# Full verbose scan with report
python upload_scanner.py -u http://target.com/upload --verbose --output full_report.txt

# Short form
python upload_scanner.py -u http://target.com/upload -v -o report.txt
```

### Command-Line Arguments

| Argument | Short | Description | Required |
|----------|-------|-------------|----------|
| `--url` | `-u` | Target URL with upload functionality | Yes |
| `--output` | `-o` | Output file for report (generates .txt and .json) | No |
| `--verbose` | `-v` | Enable verbose output for debugging | No |
| `--version` | | Display version information | No |
| `--help` | `-h` | Show help message | No |

## 📊 Output Format

### Terminal Output

The scanner provides real-time feedback with color-coded messages:

- 🟢 **GREEN**: Successful operations and secure findings
- 🔵 **BLUE**: Informational messages
- 🟡 **YELLOW**: Warnings and medium-severity findings
- 🔴 **RED**: Errors and critical vulnerabilities
- 🟣 **MAGENTA**: High-severity vulnerabilities

### Report Files

When using the `-o` option, two files are generated:

1. **Text Report** (`report.txt`):
   - Human-readable format
   - Detailed vulnerability descriptions
   - Security recommendations
   - Summary statistics

2. **JSON Report** (`report.json`):
   - Machine-readable format
   - Complete scan data
   - Structured vulnerability information
   - Easy integration with other tools

### Sample Output

```
[12:34:56] [*] Phase 0: Discovering file upload endpoints...
[12:34:57] [+] Found upload form: http://target.com/upload
[12:34:57] [*] Phase 1: Testing extension validation bypass...
[12:34:58] [CRITICAL] Vulnerable: Double extension
[12:34:59] [*] Phase 2: Testing MIME type validation bypass...
[12:35:00] [CRITICAL] MIME bypass successful: PHP as JPEG

======================================================================
FILE UPLOAD VULNERABILITY SCAN REPORT
======================================================================

Target: http://target.com/upload
Scan Time: 2024-02-16T12:34:56
Total Tests: 45

VULNERABILITY SUMMARY
Critical: 3
High: 5
Medium: 2
Low: 1
```

## 🎯 Test Coverage

### Vulnerability Classes Tested

| Test Category | Tests | Severity Range |
|--------------|-------|----------------|
| Extension Bypass | 12 | HIGH - CRITICAL |
| MIME Spoofing | 7 | HIGH - CRITICAL |
| Magic Bytes | 3 | CRITICAL |
| Stored XSS | 3 | HIGH |
| Path Traversal | 5 | CRITICAL |
| File Overwrite | 4 | CRITICAL |
| Size Limits | 4 | LOW - MEDIUM |
| Header Security | 4 | MEDIUM |

### Total Test Cases: 42+

## 🔒 Security Recommendations

Based on scan results, the tool provides recommendations including:

1. Implement strict whitelist-based file extension validation
2. Validate file content/magic bytes, not just extensions
3. Store uploaded files outside the webroot
4. Use `Content-Disposition: attachment` header
5. Implement `X-Content-Type-Options: nosniff`
6. Rename uploaded files with random identifiers
7. Set appropriate maximum file size limits
8. Implement antivirus scanning for uploaded files
9. Apply proper access controls
10. Use Content Security Policy (CSP) headers

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is designed for authorized security testing only.

- ✅ **DO**: Use on systems you own or have explicit permission to test
- ✅ **DO**: Use in authorized penetration testing engagements
- ✅ **DO**: Use in your own lab/test environment
- ❌ **DON'T**: Use on systems without authorization
- ❌ **DON'T**: Use for malicious purposes
- ❌ **DON'T**: Deploy actual malicious files

**Unauthorized access to computer systems is illegal.** The author assumes no liability for misuse or damage caused by this tool. Always obtain proper authorization before testing.

## 🔍 How It Works

### 1. Discovery Phase
The scanner first identifies file upload functionality by:
- Parsing HTML forms for file input elements
- Analyzing form attributes (action, method, enctype)
- Detecting AJAX/API endpoints in JavaScript
- Identifying required fields and CSRF tokens

### 2. Testing Phase
For each discovered endpoint, the scanner:
- Systematically tests various attack vectors
- Monitors server responses for success indicators
- Attempts to verify vulnerabilities when possible
- Records detailed information about each test

### 3. Analysis Phase
The scanner evaluates:
- Response codes and content
- Security headers presence
- File accessibility post-upload
- Potential impact of discovered vulnerabilities

### 4. Reporting Phase
Finally, it generates:
- Severity-rated vulnerability list
- Detailed descriptions and proof-of-concept
- Actionable remediation recommendations
- Both human and machine-readable outputs

## 🛠️ Troubleshooting

### Common Issues

**Issue**: "No upload forms found"
- **Solution**: Ensure the URL points to a page with upload functionality
- Try navigating directly to the upload page
- Check if the site requires authentication

**Issue**: Connection errors or timeouts
- **Solution**: Verify the target URL is accessible
- Check your network connection
- Increase timeout values if testing slow servers

**Issue**: All tests show as blocked
- **Solution**: The site may have strong validation
- Try verbose mode (-v) to see detailed errors
- Verify the form structure is correctly detected

**Issue**: SSL/TLS errors
- **Solution**: Update your Python requests library
- Check if the site uses valid SSL certificates
- May need to add certificate verification handling

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Ideas for Contributions

- Additional test vectors
- New vulnerability classes
- Improved reporting formats
- Integration with other security tools
- Enhanced detection algorithms
- Support for authenticated scans

## 📝 Version History

### v1.0.0 (2024-02-16)
- Initial release
- 12 comprehensive testing phases
- 42+ test cases
- JSON and text report generation
- Colorized terminal output
- Automatic form discovery

## 🔗 References

### OWASP Resources
- [OWASP File Upload Vulnerabilities](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [OWASP Testing Guide - File Upload](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files)

### Additional Reading
- CWE-434: Unrestricted Upload of File with Dangerous Type
- CWE-73: External Control of File Name or Path
- CWE-79: Stored Cross-Site Scripting

## 👤 Author

**0xS4r4n9**

- Tool designed for the security community
- Focused on practical vulnerability assessment
- Educational and professional use

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2024 0xS4r4n9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- OWASP community for vulnerability research
- Security researchers who document attack vectors
- Bug bounty hunters who find real-world issues
- Open source security tool developers

## 📞 Support

For issues, questions, or suggestions:
- Open an issue in the repository
- Review the documentation thoroughly
- Check existing issues for solutions

---

**Remember**: Always test responsibly and ethically! 🛡️
