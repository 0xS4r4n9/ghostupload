# File Upload Vulnerability Scanner - How to Use Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation Guide](#installation-guide)
3. [Basic Usage](#basic-usage)
4. [Advanced Usage](#advanced-usage)
5. [Understanding Results](#understanding-results)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run your first scan
python upload_scanner.py -u http://testsite.com/upload

# 3. View results in terminal
```

That's it! The scanner will automatically discover and test file upload functionality.

---

## Installation Guide

### Step 1: System Requirements

Before starting, ensure you have:
- **Python 3.7+** installed
- **pip** (Python package manager)
- **Internet connection** for target access

#### Check Python Version
```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.7.0` or higher

### Step 2: Download the Scanner

Option A - Clone repository:
```bash
git clone https://github.com/yourusername/file-upload-scanner.git
cd file-upload-scanner
```

Option B - Download ZIP:
1. Download the ZIP file
2. Extract to your desired location
3. Navigate to the folder

### Step 3: Install Dependencies

```bash
# Standard installation
pip install -r requirements.txt

# If using Python 3 specifically
pip3 install -r requirements.txt

# With user permissions (if no admin access)
pip install --user -r requirements.txt
```

#### Verify Installation
```bash
python -c "import requests, bs4, colorama; print('All dependencies installed!')"
```

### Step 4: Make Executable (Linux/Mac)

```bash
chmod +x upload_scanner.py
```

Now you can run it directly:
```bash
./upload_scanner.py -u http://target.com/upload
```

---

## Basic Usage

### Command Structure

```
python upload_scanner.py [OPTIONS]
```

### Required Arguments

**`-u` or `--url`**: Target URL
```bash
python upload_scanner.py -u http://example.com/upload
```

⚠️ **Important**: The URL must start with `http://` or `https://`

### Optional Arguments

**`-o` or `--output`**: Save report to file
```bash
python upload_scanner.py -u http://example.com/upload -o report.txt
```
This creates two files:
- `report.txt` - Human-readable text report
- `report.json` - Machine-readable JSON data

**`-v` or `--verbose`**: Enable detailed output
```bash
python upload_scanner.py -u http://example.com/upload -v
```
Shows:
- Detailed error messages
- Additional debugging information
- Test-by-test progress

**`--version`**: Show version information
```bash
python upload_scanner.py --version
```

**`-h` or `--help`**: Display help message
```bash
python upload_scanner.py -h
```

---

## Advanced Usage

### Example 1: Complete Scan with Report

```bash
python upload_scanner.py \
  --url http://target.com/upload \
  --output scan_results.txt \
  --verbose
```

This command will:
1. Scan the target URL thoroughly
2. Show detailed progress (verbose mode)
3. Save results to `scan_results.txt` and `scan_results.json`

### Example 2: Quick Assessment

```bash
python upload_scanner.py -u http://target.com/upload
```

Quick scan with terminal output only (no file saved).

### Example 3: Silent Report Generation

```bash
python upload_scanner.py -u http://target.com/upload -o report.txt 2>/dev/null
```

Suppresses error messages, only saves to report file.

### Example 4: Multiple Target Testing

Create a script for testing multiple targets:

```bash
#!/bin/bash
# scan_multiple.sh

targets=(
  "http://site1.com/upload"
  "http://site2.com/upload"
  "http://site3.com/upload"
)

for target in "${targets[@]}"; do
  echo "Scanning: $target"
  python upload_scanner.py -u "$target" -o "report_$(echo $target | md5sum | cut -d' ' -f1).txt"
done
```

### Example 5: Scanning Behind Authentication

If your target requires login, use a browser to:
1. Log in to the site
2. Get your session cookie
3. Modify the scanner to include cookies

```python
# Add this to your scanner initialization
self.session.cookies.set('session_cookie_name', 'your_session_value')
```

---

## Understanding Results

### Terminal Output Colors

| Color | Meaning | Example |
|-------|---------|---------|
| 🟢 Green `[+]` | Success/Secure | Form discovered, test passed |
| 🔵 Blue `[*]` | Information | Starting new test phase |
| 🟡 Yellow `[!]` | Warning | Potential issue found |
| 🔴 Red `[-]` | Error/Critical | Vulnerability confirmed |

### Severity Levels

**CRITICAL** 🔴
- Remote Code Execution (RCE) potential
- Arbitrary file overwrite
- Path traversal confirmed
- **Action Required**: Fix immediately

**HIGH** 🟣
- Stored XSS vulnerabilities
- Extension bypass successful
- MIME type spoofing works
- **Action Required**: Fix urgently

**MEDIUM** 🟡
- Weak security headers
- Size limit issues
- IDOR potential
- **Action Required**: Fix soon

**LOW** 🔵
- Minor configuration issues
- Informational findings
- **Action Required**: Consider fixing

### Sample Report Breakdown

```
======================================================================
FILE UPLOAD VULNERABILITY SCAN REPORT
======================================================================

Target: http://example.com/upload          ← URL you tested
Scan Time: 2024-02-16T12:34:56            ← When scan ran
Total Tests: 45                            ← Number of tests performed

VULNERABILITY SUMMARY
Critical: 2    ← Immediate action required
High: 3        ← Urgent fix needed
Medium: 1      ← Important to address
Low: 0         ← Nice to fix

UPLOAD ENDPOINTS DISCOVERED
1. http://example.com/upload              ← Forms found
   Method: POST                            ← HTTP method
   File Fields: upload, document          ← Input field names

DETAILED VULNERABILITIES

[CRITICAL] Magic bytes bypass: GIF header + PHP payload
Description: Polyglot file accepted: GIF header + PHP payload
Filename: image.php
↑ This means: Server accepts files with valid image headers 
              but executable code inside - very dangerous!

[HIGH] Stored XSS: SVG with script tag
Description: XSS vector uploaded successfully
Filename: xss.svg
File URL: http://example.com/uploads/xss.svg
↑ This means: Uploaded SVG file can run JavaScript in 
              victim's browsers - security risk!
```

### JSON Report Structure

```json
{
  "target": "http://example.com/upload",
  "scan_time": "2024-02-16T12:34:56",
  "total_tests": 45,
  "critical": 2,
  "high": 3,
  "medium": 1,
  "low": 0,
  "upload_endpoints": [...],
  "vulnerabilities": [
    {
      "test": "Extension bypass: Double extension",
      "filename": "test.php.jpg",
      "status": "ACCEPTED",
      "severity": "HIGH",
      "description": "File upload accepted with dangerous extension",
      "response_code": 200
    }
  ]
}
```

---

## Best Practices

### Before Scanning

1. **Get Authorization**
   - Always obtain written permission
   - Confirm scope of testing
   - Understand limitations

2. **Prepare Environment**
   - Test from isolated network if possible
   - Have incident response contact ready
   - Document your testing

3. **Review Target**
   - Manually explore the upload functionality
   - Understand the expected file types
   - Note any client-side validation

### During Scanning

1. **Start Conservative**
   - Run initial scan without aggressive tests
   - Review results before proceeding
   - Adjust approach based on findings

2. **Monitor Impact**
   - Watch for server slowdowns
   - Check if uploads are being stored
   - Be ready to stop if issues occur

3. **Document Everything**
   - Save all reports with timestamps
   - Take screenshots of findings
   - Note exact steps to reproduce

### After Scanning

1. **Clean Up**
   - Remove any test files you uploaded
   - Clear any sessions/cookies
   - Verify no harm was caused

2. **Report Responsibly**
   - Follow disclosure policies
   - Provide clear reproduction steps
   - Suggest remediation approaches

3. **Learn and Improve**
   - Analyze why vulnerabilities existed
   - Understand the fix implementations
   - Update your testing methodology

---

## Troubleshooting

### Problem: "No upload forms found"

**Symptoms**: Scanner completes immediately with no tests run

**Solutions**:
1. Verify URL is correct and accessible
   ```bash
   curl -I http://target.com/upload
   ```

2. Check if page requires authentication
   - Log in manually first
   - Extract session cookie
   - Add cookie to scanner

3. Try different pages
   ```bash
   python upload_scanner.py -u http://target.com/profile/upload
   ```

4. Check for JavaScript-based uploads
   - Scanner may not detect AJAX endpoints
   - Look in browser dev tools for API calls

### Problem: Connection timeouts

**Symptoms**: "Connection timeout" or "Read timeout" errors

**Solutions**:
1. Verify network connectivity
   ```bash
   ping target.com
   ```

2. Check if site is behind firewall/WAF
   - May be blocking automated tools
   - Try from different IP/VPN

3. Increase timeout in code
   ```python
   # In upload_scanner.py, modify timeout values
   response = self.session.get(self.target_url, timeout=30)  # Increased from 10
   ```

### Problem: SSL/Certificate errors

**Symptoms**: "SSL: CERTIFICATE_VERIFY_FAILED"

**Solutions**:
1. Update certificates
   ```bash
   pip install --upgrade certifi
   ```

2. For testing only, disable verification (NOT RECOMMENDED for production):
   ```python
   # Add to session configuration
   self.session.verify = False
   ```

### Problem: All tests show as blocked

**Symptoms**: Every upload attempt fails

**Solutions**:
1. Check if WAF is blocking
   - Look for "403 Forbidden" responses
   - Check response for WAF signatures

2. Verify form structure
   - Run with `-v` flag
   - Check if required fields are detected

3. Test manually first
   - Upload a legitimate file through browser
   - Confirm functionality works

### Problem: Permission errors saving reports

**Symptoms**: "Permission denied" when using `-o`

**Solutions**:
1. Check write permissions
   ```bash
   ls -la /path/to/output/directory
   ```

2. Use different output location
   ```bash
   python upload_scanner.py -u http://target.com -o ~/reports/scan.txt
   ```

3. Run with appropriate permissions
   ```bash
   sudo python upload_scanner.py -u http://target.com -o /var/reports/scan.txt
   ```

---

## Examples

### Example 1: First-Time User

**Scenario**: You want to test your own website's upload feature

```bash
# Step 1: Navigate to scanner directory
cd file-upload-scanner

# Step 2: Run basic scan
python upload_scanner.py -u http://mywebsite.com/upload

# Step 3: Review terminal output
# Look for any CRITICAL or HIGH findings

# Step 4: If issues found, save detailed report
python upload_scanner.py -u http://mywebsite.com/upload -o mywebsite_scan.txt
```

### Example 2: Penetration Tester

**Scenario**: Professional engagement with multiple targets

```bash
# Create organized directory structure
mkdir -p scans/$(date +%Y%m%d)
cd scans/$(date +%Y%m%d)

# Scan with full verbosity and reporting
python ../../upload_scanner.py \
  -u http://client-site.com/upload \
  -v \
  -o client-site-upload-scan.txt

# Review JSON for automation
cat client-site-upload-scan.json | jq '.vulnerabilities[] | select(.severity=="CRITICAL")'
```

### Example 3: Bug Bounty Hunter

**Scenario**: Testing public bug bounty program

```bash
# Test main upload endpoint
python upload_scanner.py -u https://target.com/upload -o bounty-upload-1.txt

# Test user profile upload
python upload_scanner.py -u https://target.com/profile/avatar -o bounty-profile.txt

# Test API endpoint if discovered
python upload_scanner.py -u https://api.target.com/v1/files -o bounty-api.txt

# Compile findings
cat bounty-*.json | jq -s 'map(.vulnerabilities[]) | unique_by(.test)'
```

### Example 4: Security Auditor

**Scenario**: Comprehensive application assessment

```bash
#!/bin/bash
# comprehensive_scan.sh

APP_NAME="ClientApp"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="reports/${APP_NAME}_${TIMESTAMP}"

mkdir -p "$REPORT_DIR"

# Scan all known upload endpoints
endpoints=(
  "https://app.client.com/upload"
  "https://app.client.com/profile/photo"
  "https://app.client.com/documents/upload"
  "https://app.client.com/api/v1/files"
)

for endpoint in "${endpoints[@]}"; do
  filename=$(echo "$endpoint" | sed 's/[^a-zA-Z0-9]/_/g')
  echo "Scanning: $endpoint"
  
  python upload_scanner.py \
    -u "$endpoint" \
    -v \
    -o "${REPORT_DIR}/${filename}.txt"
  
  echo "Completed: $endpoint"
  sleep 5  # Rate limiting
done

# Generate summary
echo "Scan Summary for $APP_NAME" > "${REPORT_DIR}/SUMMARY.txt"
echo "Timestamp: $TIMESTAMP" >> "${REPORT_DIR}/SUMMARY.txt"
echo "---" >> "${REPORT_DIR}/SUMMARY.txt"

for json_file in "${REPORT_DIR}"/*.json; do
  if [ -f "$json_file" ]; then
    echo "File: $(basename $json_file)" >> "${REPORT_DIR}/SUMMARY.txt"
    jq -r '.critical, .high, .medium, .low' "$json_file" >> "${REPORT_DIR}/SUMMARY.txt"
    echo "---" >> "${REPORT_DIR}/SUMMARY.txt"
  fi
done

echo "All scans complete! Reports saved to: $REPORT_DIR"
```

### Example 5: CI/CD Integration

**Scenario**: Automated security testing in pipeline

```yaml
# .github/workflows/security-scan.yml
name: File Upload Security Scan

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  push:
    branches: [ main ]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run upload scanner
        run: |
          python upload_scanner.py \
            -u ${{ secrets.STAGING_UPLOAD_URL }} \
            -o scan_results.txt
      
      - name: Check for critical issues
        run: |
          CRITICAL=$(jq '.critical' scan_results.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "Critical vulnerabilities found!"
            exit 1
          fi
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: scan-results
          path: scan_results.*
```

---

## Tips and Tricks

### Tip 1: Test Incrementally
Start with non-intrusive tests, then gradually increase aggressiveness based on results.

### Tip 2: Combine with Manual Testing
Use the scanner for breadth, but manually verify critical findings for accuracy.

### Tip 3: Keep Logs
Always save reports with timestamps for comparison and tracking remediation.

### Tip 4: Understand False Positives
Not every "vulnerability" may be exploitable in context. Verify findings.

### Tip 5: Use Verbose Mode for Learning
The `-v` flag is excellent for understanding how the scanner works.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  FILE UPLOAD SCANNER - QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BASIC SCAN                                                  │
│  $ python upload_scanner.py -u http://target.com/upload     │
│                                                              │
│  WITH REPORT                                                 │
│  $ python upload_scanner.py -u URL -o report.txt            │
│                                                              │
│  VERBOSE MODE                                                │
│  $ python upload_scanner.py -u URL -v                        │
│                                                              │
│  FULL OPTIONS                                                │
│  $ python upload_scanner.py -u URL -v -o report.txt         │
│                                                              │
│  GET HELP                                                    │
│  $ python upload_scanner.py --help                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  SEVERITY LEVELS: CRITICAL > HIGH > MEDIUM > LOW            │
│  OUTPUT FILES: report.txt (text), report.json (JSON)        │
└─────────────────────────────────────────────────────────────┘
```

---

**Remember**: Always test ethically and with proper authorization! 🛡️

For more information, see the main README.md file.
