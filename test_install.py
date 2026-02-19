#!/usr/bin/env python3
"""
Test script to verify installation
"""

import sys

print("Testing File Upload Scanner Installation...")
print("=" * 60)

# Test Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")

# Test imports
try:
    import requests
    print("✓ requests module: OK")
except ImportError as e:
    print(f"✗ requests module: FAILED - {e}")
    sys.exit(1)

try:
    import bs4
    print("✓ beautifulsoup4 module: OK")
except ImportError as e:
    print(f"✗ beautifulsoup4 module: FAILED - {e}")
    sys.exit(1)

try:
    import colorama
    print("✓ colorama module: OK")
except ImportError as e:
    print(f"✗ colorama module: FAILED - {e}")
    sys.exit(1)

try:
    import urllib3
    print("✓ urllib3 module: OK")
except ImportError as e:
    print(f"✗ urllib3 module: FAILED - {e}")
    sys.exit(1)

# Test BeautifulSoup with html.parser
try:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup("<html><body><p>Test</p></body></html>", 'html.parser')
    assert soup.find('p').text == 'Test'
    print("✓ BeautifulSoup html.parser: OK")
except Exception as e:
    print(f"✗ BeautifulSoup html.parser: FAILED - {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All dependencies installed correctly!")
print("✓ Scanner is ready to use!")
print("\nRun: python upload_scanner.py --help")
