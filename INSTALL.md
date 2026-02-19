# Installation Guide - File Upload Vulnerability Scanner

## Quick Install (Recommended)

```bash
cd file-upload-scanner
bash setup.sh
```

The setup script will automatically:
- Check Python version
- Create virtual environment (if available)
- Install dependencies
- Make scripts executable
- Verify installation

---

## Manual Installation

### Option 1: Virtual Environment (Recommended)

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make executable (Linux/Mac only)
chmod +x upload_scanner.py

# 5. Run scanner
python upload_scanner.py -u http://target.com/upload
```

### Option 2: System-Wide Install

```bash
# Install dependencies system-wide
pip install -r requirements.txt --break-system-packages

# Make executable (Linux/Mac)
chmod +x upload_scanner.py

# Run scanner
python upload_scanner.py -u http://target.com/upload
```

### Option 3: User Install

```bash
# Install for current user only
pip install --user -r requirements.txt

# Make executable (Linux/Mac)
chmod +x upload_scanner.py

# Run scanner
python upload_scanner.py -u http://target.com/upload
```

---

## System Requirements

### All Platforms

- **Python**: 3.7 or higher
- **pip**: Python package manager
- **Internet**: For initial package download

### Linux/Ubuntu/Debian

All dependencies are pure Python packages - no system libraries required!

```bash
# Just install the Python packages
pip install -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

```bash
# Install Xcode Command Line Tools (if needed)
xcode-select --install

# Install dependencies
pip3 install -r requirements.txt
```

### Windows

```bash
# Ensure Python and pip are in PATH
python --version
pip --version

# Install dependencies
pip install -r requirements.txt
```

---

## Dependency Details

### Core Dependencies

**requests (2.31.0)**
- Purpose: HTTP client for web requests
- Size: ~200KB
- Installation: Straightforward, pure Python

**beautifulsoup4 (4.12.2)**
- Purpose: HTML/XML parsing
- Size: ~150KB
- Installation: Straightforward, pure Python
- Uses built-in html.parser (no external dependencies)

**colorama (0.4.6)**
- Purpose: Cross-platform colored terminal output
- Size: ~25KB
- Installation: Straightforward, pure Python

**urllib3 (2.0.7)**
- Purpose: HTTP utilities
- Size: ~300KB
- Installation: Straightforward, pure Python

### Total Size

Approximately **700 KB** of Python packages

**Note**: All dependencies are pure Python with no compilation required!

---

## Troubleshooting Installation

### Problem: "externally-managed-environment"

This occurs on newer Linux systems (Debian 12+, Ubuntu 23.04+).

**Solution 1**: Use virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2**: Use --break-system-packages flag
```bash
pip install -r requirements.txt --break-system-packages
```

**Solution 3**: Install system packages
```bash
sudo apt install python3-requests python3-bs4 python3-lxml python3-colorama
```

### Problem: "Permission denied"

**Solution**: Use one of these approaches:
```bash
# Option 1: User install
pip install --user -r requirements.txt

# Option 2: Virtual environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Option 3: Sudo (not recommended)
sudo pip install -r requirements.txt
```

### Problem: pip not found

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# macOS
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Windows
python -m ensurepip --upgrade
```

### Problem: Python version too old

**Solution**: Install newer Python
```bash
# Ubuntu/Debian
sudo apt-get install python3.10

# macOS (using Homebrew)
brew install python@3.10

# Windows
# Download from python.org
```

---

## Verification

After installation, verify everything works:

```bash
# Check Python version
python --version
# or
python3 --version

# Check dependencies
python -c "import requests, bs4, colorama; print('All dependencies OK!')"

# Test scanner
python upload_scanner.py --version

# Should output:
# File Upload Scanner v1.0.0 by 0xS4r4n9
```

---

## Platform-Specific Notes

### Ubuntu 24.04 / Debian 12+

These systems use "externally managed environment" by default.

**Recommended approach**:
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Kali Linux

All dependencies usually pre-installed:
```bash
# Just verify
python3 upload_scanner.py --version
```

### Windows 10/11

```bash
# Use Command Prompt or PowerShell
python -m pip install -r requirements.txt

# Run scanner
python upload_scanner.py -u http://target.com/upload
```

### macOS

```bash
# May need to use python3 explicitly
python3 -m pip install -r requirements.txt

# Run scanner
python3 upload_scanner.py -u http://target.com/upload
```

---

## Docker Installation (Alternative)

If you prefer Docker:

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies (no system packages needed!)
RUN pip install --no-cache-dir -r requirements.txt

# Run scanner
ENTRYPOINT ["python", "upload_scanner.py"]
```

Build and run:
```bash
docker build -t file-upload-scanner .
docker run file-upload-scanner -u http://target.com/upload
```

---

## Post-Installation

### Create Alias (Optional)

**Linux/Mac** (add to ~/.bashrc or ~/.zshrc):
```bash
alias upload-scan='python3 /path/to/file-upload-scanner/upload_scanner.py'
```

**Windows** (PowerShell profile):
```powershell
function upload-scan { python C:\path\to\upload_scanner.py $args }
```

### Create Desktop Shortcut (Optional)

**Linux**:
```bash
cat > ~/Desktop/upload-scanner.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Upload Scanner
Exec=gnome-terminal -- bash -c "cd /path/to/file-upload-scanner && python3 upload_scanner.py; read"
Icon=security-high
EOF
chmod +x ~/Desktop/upload-scanner.desktop
```

---

## Uninstallation

### Remove Python Packages

```bash
# If using virtual environment
rm -rf venv/

# If installed system-wide
pip uninstall -y -r requirements.txt

# Remove project directory
rm -rf file-upload-scanner/
```

---

## Getting Help

If you're still having issues:

1. **Check Python version**: `python --version` (must be 3.7+)
2. **Check pip version**: `pip --version`
3. **Try verbose install**: `pip install -v -r requirements.txt`
4. **Check system libraries**: `ldconfig -p | grep xml`
5. **Review error messages carefully**

For specific errors, search the error message or consult:
- Python documentation: https://docs.python.org
- pip documentation: https://pip.pypa.io
- Project issues (if available)

---

## Success Indicators

Installation successful when you see:

```
[+] Dependencies installed successfully!
[+] Scripts are now executable
[+] Reports directory created

╔═══════════════════════════════════════════════════════════════════╗
║                    INSTALLATION SUCCESSFUL!                       ║
╚═══════════════════════════════════════════════════════════════════╝

Quick Start:
  python upload_scanner.py -u http://target.com/upload
```

---

**Created by**: 0xS4r4n9  
**Version**: 1.0.0

Happy scanning! 🛡️
