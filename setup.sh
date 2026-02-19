#!/bin/bash
# Quick Setup Script for File Upload Vulnerability Scanner
# Created by: 0xS4r4n9

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║      ███████╗██╗██╗     ███████╗    ██╗   ██╗██████╗            ║"
echo "║      ██╔════╝██║██║     ██╔════╝    ██║   ██║██╔══██╗           ║"
echo "║      █████╗  ██║██║     █████╗      ██║   ██║██████╔╝           ║"
echo "║      ██╔══╝  ██║██║     ██╔══╝      ██║   ██║██╔═══╝            ║"
echo "║      ██║     ██║███████╗███████╗    ╚██████╔╝██║                ║"
echo "║      ╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚═╝                ║"
echo "║                                                                   ║"
echo "║            FILE UPLOAD VULNERABILITY SCANNER                     ║"
echo "║                     Quick Setup Script                           ║"
echo "║                   Created by: 0xS4r4n9                          ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[*] Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "[+] Found Python 3: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    echo "[+] Found Python: $PYTHON_VERSION"
else
    echo "[-] Python not found! Please install Python 3.7+"
    exit 1
fi

# Check pip
echo "[*] Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    echo "[+] Found pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    echo "[+] Found pip"
else
    echo "[-] pip not found! Please install pip"
    exit 1
fi

# Install dependencies
echo ""
echo "[*] Installing dependencies..."

# Try with virtual environment first
if command -v python3-venv &> /dev/null || $PYTHON_CMD -m venv --help &> /dev/null 2>&1; then
    echo "[*] Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    
    if [ $? -eq 0 ]; then
        echo "[+] Virtual environment created"
        source venv/bin/activate
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo "[+] Dependencies installed in virtual environment!"
            echo "[!] Remember to activate venv: source venv/bin/activate"
        else
            echo "[-] Failed to install dependencies in venv"
        fi
    else
        echo "[!] Could not create virtual environment"
        echo "[*] Trying with --break-system-packages flag..."
        $PIP_CMD install -r requirements.txt --break-system-packages
    fi
else
    echo "[*] Virtual environment not available, using --break-system-packages..."
    $PIP_CMD install -r requirements.txt --break-system-packages
fi

if [ $? -eq 0 ]; then
    echo "[+] Dependencies installed successfully!"
else
    echo "[-] Failed to install dependencies"
    echo "[!] You may need to install manually with:"
    echo "    pip install -r requirements.txt --break-system-packages"
    echo "    or use a virtual environment"
fi

# Make scripts executable
echo ""
echo "[*] Making scripts executable..."
chmod +x upload_scanner.py
chmod +x examples.py

if [ $? -eq 0 ]; then
    echo "[+] Scripts are now executable"
else
    echo "[!] Warning: Could not make scripts executable (may need sudo)"
fi

# Create reports directory
echo ""
echo "[*] Creating reports directory..."
mkdir -p reports
echo "[+] Reports directory created"

# Test installation
echo ""
echo "[*] Testing installation..."
$PYTHON_CMD test_install.py

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                    INSTALLATION SUCCESSFUL!                       ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Quick Start:"
    echo "  $PYTHON_CMD upload_scanner.py -u http://target.com/upload"
    echo ""
    echo "With report:"
    echo "  $PYTHON_CMD upload_scanner.py -u http://target.com/upload -o reports/scan.txt"
    echo ""
    echo "Verbose mode:"
    echo "  $PYTHON_CMD upload_scanner.py -u http://target.com/upload -v"
    echo ""
    echo "For more information:"
    echo "  - Read README.md for overview"
    echo "  - Read HOW_TO_USE.md for detailed guide"
    echo "  - Run: $PYTHON_CMD upload_scanner.py --help"
    echo ""
    echo "Happy ethical hacking! 🛡️"
    echo ""
else
    echo "[-] Installation test failed"
    exit 1
fi
