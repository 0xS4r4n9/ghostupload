#!/usr/bin/env python3
"""
File Upload Vulnerability Scanner
Created by: 0xS4r4n9
Version: 1.0.0
"""

import requests
import argparse
import sys
import os
import time
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from datetime import datetime
import base64
import mimetypes

# Initialize colorama
init(autoreset=True)

class Colors:
    """Color definitions for output"""
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    CRITICAL = Fore.RED + Style.BRIGHT
    HIGH = Fore.MAGENTA + Style.BRIGHT
    MEDIUM = Fore.YELLOW
    LOW = Fore.CYAN
    RESET = Style.RESET_ALL

def print_banner():
    """Display tool banner"""
    banner = f"""
{Colors.HEADER}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║      ███████╗██╗██╗     ███████╗    ██╗   ██╗██████╗            ║
║      ██╔════╝██║██║     ██╔════╝    ██║   ██║██╔══██╗           ║
║      █████╗  ██║██║     █████╗      ██║   ██║██████╔╝           ║
║      ██╔══╝  ██║██║     ██╔══╝      ██║   ██║██╔═══╝            ║
║      ██║     ██║███████╗███████╗    ╚██████╔╝██║                ║
║      ╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝ ╚═╝                ║
║                                                                   ║
║            FILE UPLOAD VULNERABILITY SCANNER v1.0                ║
║                   Created by: 0xS4r4n9                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

class FileUploadScanner:
    """Main scanner class for file upload vulnerabilities"""
    
    def __init__(self, target_url, verbose=False, output_file=None):
        self.target_url = target_url
        self.verbose = verbose
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            'target': target_url,
            'scan_time': datetime.now().isoformat(),
            'upload_endpoints': [],
            'vulnerabilities': [],
            'total_tests': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        # Test payloads
        self.test_extensions = [
            '.php', '.php5', '.phtml', '.phar',
            '.asp', '.aspx', '.ashx',
            '.jsp', '.jspx',
            '.html', '.htm',
            '.svg', '.xml'
        ]
        
        self.bypass_extensions = [
            'shell.php.jpg', 'shell.php.', 'shell.php .jpg',
            'shell.PhP', 'shell.pHp', 'test.php%00.jpg',
            'shell.phр', '../../../../test.php', '../test.php'
        ]
        
    def log(self, message, level="INFO"):
        """Log messages with color coding"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "SUCCESS":
            print(f"[{timestamp}] {Colors.SUCCESS}[+]{Colors.RESET} {message}")
        elif level == "ERROR":
            print(f"[{timestamp}] {Colors.ERROR}[-]{Colors.RESET} {message}")
        elif level == "WARNING":
            print(f"[{timestamp}] {Colors.WARNING}[!]{Colors.RESET} {message}")
        elif level == "INFO":
            print(f"[{timestamp}] {Colors.INFO}[*]{Colors.RESET} {message}")
        elif level == "CRITICAL":
            print(f"[{timestamp}] {Colors.CRITICAL}[CRITICAL]{Colors.RESET} {message}")
        
    def discover_upload_forms(self):
        """Phase 0: Discover file upload endpoints"""
        self.log("Phase 0: Discovering file upload endpoints...", "INFO")
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find forms with file inputs
            forms = soup.find_all('form')
            
            for form in forms:
                file_inputs = form.find_all('input', {'type': 'file'})
                
                if file_inputs:
                    form_data = self.analyze_form(form, file_inputs)
                    self.results['upload_endpoints'].append(form_data)
                    self.log(f"Found upload form: {form_data['action']}", "SUCCESS")
                    
            # Look for AJAX/API endpoints in JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Look for common upload patterns
                    upload_patterns = [
                        r'/api/upload', r'/upload', r'/file/upload',
                        r'FormData.*append.*file', r'multipart/form-data'
                    ]
                    for pattern in upload_patterns:
                        if re.search(pattern, script.string, re.IGNORECASE):
                            self.log(f"Potential AJAX upload endpoint detected", "WARNING")
                            
            if not self.results['upload_endpoints']:
                self.log("No upload forms found on main page", "WARNING")
                return False
                
            return True
            
        except Exception as e:
            self.log(f"Error during discovery: {str(e)}", "ERROR")
            return False
    
    def analyze_form(self, form, file_inputs):
        """Analyze form structure and requirements"""
        action = form.get('action', '')
        method = form.get('method', 'POST').upper()
        enctype = form.get('enctype', '')
        
        # Make action an absolute URL
        if action:
            action = urljoin(self.target_url, action)
        else:
            action = self.target_url
            
        # Get all form fields
        fields = {}
        for input_tag in form.find_all(['input', 'textarea', 'select']):
            name = input_tag.get('name')
            if name:
                value = input_tag.get('value', '')
                fields[name] = value
                
        # Get file input names
        file_fields = [f.get('name') for f in file_inputs if f.get('name')]
        
        # Check for CSRF tokens
        csrf_token = None
        csrf_patterns = ['csrf', 'token', '_token', 'authenticity_token']
        for field_name, field_value in fields.items():
            if any(pattern in field_name.lower() for pattern in csrf_patterns):
                csrf_token = field_value
                
        return {
            'action': action,
            'method': method,
            'enctype': enctype,
            'file_fields': file_fields,
            'all_fields': fields,
            'csrf_token': csrf_token
        }
    
    def test_extension_bypass(self, endpoint):
        """Phase 1: Test extension validation bypass"""
        self.log("Phase 1: Testing extension validation bypass...", "INFO")
        
        vulnerabilities = []
        
        # Test various bypass techniques
        test_cases = [
            # Double extensions
            {'filename': 'test.php.jpg', 'description': 'Double extension'},
            {'filename': 'test.asp.png', 'description': 'Double extension (ASP)'},
            # Trailing characters
            {'filename': 'test.php.', 'description': 'Trailing dot'},
            {'filename': 'test.php ', 'description': 'Trailing space'},
            # Case manipulation
            {'filename': 'test.PhP', 'description': 'Mixed case'},
            {'filename': 'test.pHp', 'description': 'Mixed case variant'},
            # Null byte (URL encoded)
            {'filename': 'test.php%00.jpg', 'description': 'Null byte injection'},
            # Alternative extensions
            {'filename': 'test.php5', 'description': 'Alternative PHP extension'},
            {'filename': 'test.phtml', 'description': 'PHTML extension'},
            {'filename': 'test.phar', 'description': 'PHAR extension'},
            # Unicode tricks
            {'filename': 'test.phр', 'description': 'Unicode lookalike (Cyrillic)'},
            # Long filename
            {'filename': 'A' * 200 + '.php.jpg', 'description': 'Long filename'},
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                # Create a benign test file
                file_content = b'<?php echo "VULNERABLE"; ?>'
                
                files = {
                    endpoint['file_fields'][0]: (test_case['filename'], file_content, 'image/jpeg')
                }
                
                # Add other required fields
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                # Check if upload was accepted
                if response.status_code in [200, 201, 302]:
                    # Look for success indicators
                    success_patterns = [
                        'success', 'uploaded', 'complete', 'saved',
                        'file_path', 'file_url', 'filename'
                    ]
                    
                    response_text = response.text.lower()
                    
                    if any(pattern in response_text for pattern in success_patterns):
                        vuln = {
                            'test': f"Extension bypass: {test_case['description']}",
                            'filename': test_case['filename'],
                            'status': 'ACCEPTED',
                            'severity': 'HIGH',
                            'description': f'File upload accepted with dangerous extension: {test_case["filename"]}',
                            'response_code': response.status_code
                        }
                        vulnerabilities.append(vuln)
                        self.results['high'] += 1
                        self.log(f"Vulnerable: {test_case['description']}", "CRITICAL")
                    
            except Exception as e:
                if self.verbose:
                    self.log(f"Error testing {test_case['filename']}: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_mime_type_bypass(self, endpoint):
        """Phase 2: Test MIME type spoofing"""
        self.log("Phase 2: Testing MIME type validation bypass...", "INFO")
        
        vulnerabilities = []
        
        test_cases = [
            {'filename': 'test.php', 'mime': 'image/jpeg', 'description': 'PHP as JPEG'},
            {'filename': 'test.php', 'mime': 'image/png', 'description': 'PHP as PNG'},
            {'filename': 'test.aspx', 'mime': 'image/gif', 'description': 'ASPX as GIF'},
            {'filename': 'test.jsp', 'mime': 'image/jpeg', 'description': 'JSP as JPEG'},
            {'filename': 'shell.html', 'mime': 'image/jpeg', 'description': 'HTML as JPEG'},
            {'filename': 'test.svg', 'mime': 'image/png', 'description': 'SVG as PNG'},
            {'filename': 'test.php', 'mime': 'application/octet-stream', 'description': 'Generic MIME'},
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                file_content = b'<?php echo "MIME_BYPASS"; ?>'
                
                files = {
                    endpoint['file_fields'][0]: (
                        test_case['filename'],
                        file_content,
                        test_case['mime']
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code in [200, 201, 302]:
                    if 'success' in response.text.lower() or 'upload' in response.text.lower():
                        vuln = {
                            'test': f"MIME type bypass: {test_case['description']}",
                            'filename': test_case['filename'],
                            'mime_type': test_case['mime'],
                            'status': 'ACCEPTED',
                            'severity': 'HIGH',
                            'description': f'Server accepted {test_case["filename"]} with spoofed MIME type {test_case["mime"]}',
                            'response_code': response.status_code
                        }
                        vulnerabilities.append(vuln)
                        self.results['high'] += 1
                        self.log(f"MIME bypass successful: {test_case['description']}", "CRITICAL")
                        
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in MIME test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_magic_bytes_bypass(self, endpoint):
        """Phase 3: Test magic bytes / file signature bypass"""
        self.log("Phase 3: Testing magic bytes bypass...", "INFO")
        
        vulnerabilities = []
        
        # Polyglot files - valid image header + malicious payload
        test_cases = [
            {
                'filename': 'polyglot.php',
                'content': b'\x89PNG\r\n\x1a\n<?php echo "POLYGLOT"; ?>',
                'description': 'PNG header + PHP payload'
            },
            {
                'filename': 'polyglot.jsp',
                'content': b'\xFF\xD8\xFF\xE0<% out.println("POLYGLOT"); %>',
                'description': 'JPEG header + JSP payload'
            },
            {
                'filename': 'image.php',
                'content': b'GIF89a<?php echo "POLYGLOT"; ?>',
                'description': 'GIF header + PHP payload'
            }
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                files = {
                    endpoint['file_fields'][0]: (
                        test_case['filename'],
                        test_case['content'],
                        'image/png'
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code in [200, 201, 302]:
                    if 'success' in response.text.lower():
                        vuln = {
                            'test': f"Magic bytes bypass: {test_case['description']}",
                            'filename': test_case['filename'],
                            'status': 'ACCEPTED',
                            'severity': 'CRITICAL',
                            'description': f'Polyglot file accepted: {test_case["description"]}',
                            'response_code': response.status_code
                        }
                        vulnerabilities.append(vuln)
                        self.results['critical'] += 1
                        self.log(f"Magic bytes bypass: {test_case['description']}", "CRITICAL")
                        
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in magic bytes test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_xss_vectors(self, endpoint):
        """Phase 5: Test for stored XSS via uploads"""
        self.log("Phase 5: Testing for stored XSS vulnerabilities...", "INFO")
        
        vulnerabilities = []
        
        test_cases = [
            {
                'filename': 'xss.svg',
                'content': b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert("XSS")</script></svg>',
                'mime': 'image/svg+xml',
                'description': 'SVG with script tag'
            },
            {
                'filename': 'xss.html',
                'content': b'<html><body><script>alert("XSS")</script></body></html>',
                'mime': 'text/html',
                'description': 'HTML with script'
            },
            {
                'filename': 'xss_event.svg',
                'content': b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(\'XSS\')"></svg>',
                'mime': 'image/svg+xml',
                'description': 'SVG with event handler'
            }
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                files = {
                    endpoint['file_fields'][0]: (
                        test_case['filename'],
                        test_case['content'],
                        test_case['mime']
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code in [200, 201, 302]:
                    # Try to extract file URL from response
                    file_url_patterns = [
                        r'href=["\']([^"\']*' + re.escape(test_case['filename']) + r'[^"\']*)["\']',
                        r'src=["\']([^"\']*' + re.escape(test_case['filename']) + r'[^"\']*)["\']',
                        r'"url"\s*:\s*"([^"]*)"',
                        r'"path"\s*:\s*"([^"]*)"'
                    ]
                    
                    file_url = None
                    for pattern in file_url_patterns:
                        match = re.search(pattern, response.text)
                        if match:
                            file_url = match.group(1)
                            break
                    
                    if 'success' in response.text.lower() or file_url:
                        vuln = {
                            'test': f"Stored XSS: {test_case['description']}",
                            'filename': test_case['filename'],
                            'status': 'POTENTIAL_XSS',
                            'severity': 'HIGH',
                            'description': f'XSS vector uploaded successfully: {test_case["description"]}',
                            'file_url': file_url,
                            'response_code': response.status_code
                        }
                        vulnerabilities.append(vuln)
                        self.results['high'] += 1
                        self.log(f"Potential XSS: {test_case['description']}", "CRITICAL")
                        
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in XSS test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_path_traversal(self, endpoint):
        """Phase 6: Test path traversal in filename"""
        self.log("Phase 6: Testing path traversal vulnerabilities...", "INFO")
        
        vulnerabilities = []
        
        test_cases = [
            {'filename': '../../../../etc/passwd.txt', 'description': 'Unix path traversal'},
            {'filename': '..\\..\\..\\windows\\win.ini', 'description': 'Windows path traversal'},
            {'filename': '....//....//....//etc/passwd', 'description': 'Double encoding traversal'},
            {'filename': '%2e%2e%2f%2e%2e%2f%2e%2e%2f', 'description': 'URL encoded traversal'},
            {'filename': '../../../var/www/html/shell.php', 'description': 'Webroot traversal'}
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                file_content = b'PATH_TRAVERSAL_TEST'
                
                files = {
                    endpoint['file_fields'][0]: (
                        test_case['filename'],
                        file_content,
                        'text/plain'
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                # Look for path traversal indicators in response
                traversal_indicators = [
                    '../', '..\\', 'etc/passwd', 'windows/win.ini',
                    'var/www', 'path', 'directory'
                ]
                
                response_text = response.text.lower()
                
                if response.status_code in [200, 201] and any(ind in response_text for ind in traversal_indicators):
                    vuln = {
                        'test': f"Path traversal: {test_case['description']}",
                        'filename': test_case['filename'],
                        'status': 'POTENTIAL_TRAVERSAL',
                        'severity': 'CRITICAL',
                        'description': f'Path traversal attempt accepted: {test_case["description"]}',
                        'response_code': response.status_code
                    }
                    vulnerabilities.append(vuln)
                    self.results['critical'] += 1
                    self.log(f"Path traversal accepted: {test_case['description']}", "CRITICAL")
                    
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in path traversal test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_file_overwrite(self, endpoint):
        """Phase 7: Test file overwrite capabilities"""
        self.log("Phase 7: Testing file overwrite vulnerabilities...", "INFO")
        
        vulnerabilities = []
        
        # Test common overwritable files
        test_cases = [
            {'filename': 'index.html', 'description': 'Index page overwrite'},
            {'filename': 'robots.txt', 'description': 'Robots.txt overwrite'},
            {'filename': '.htaccess', 'description': 'htaccess overwrite'},
            {'filename': 'config.php', 'description': 'Config file overwrite'}
        ]
        
        for test_case in test_cases:
            self.results['total_tests'] += 1
            
            try:
                marker = f"OVERWRITE_TEST_{int(time.time())}"
                file_content = f"<!-- {marker} -->".encode()
                
                files = {
                    endpoint['file_fields'][0]: (
                        test_case['filename'],
                        file_content,
                        'text/plain'
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    # Try to verify if file was overwritten
                    parsed_url = urlparse(self.target_url)
                    test_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{test_case['filename']}"
                    
                    verify_response = self.session.get(test_url, timeout=5)
                    
                    if marker.encode() in verify_response.content:
                        vuln = {
                            'test': f"File overwrite: {test_case['description']}",
                            'filename': test_case['filename'],
                            'status': 'CONFIRMED_OVERWRITE',
                            'severity': 'CRITICAL',
                            'description': f'Successfully overwrote {test_case["filename"]}',
                            'verification_url': test_url
                        }
                        vulnerabilities.append(vuln)
                        self.results['critical'] += 1
                        self.log(f"File overwrite confirmed: {test_case['filename']}", "CRITICAL")
                        
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in overwrite test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_size_limits(self, endpoint):
        """Phase 9: Test file size restrictions"""
        self.log("Phase 9: Testing file size limits...", "INFO")
        
        vulnerabilities = []
        
        # Test various file sizes
        sizes = [
            (1024, 'Small (1KB)'),
            (1024 * 100, 'Medium (100KB)'),
            (1024 * 1024, 'Large (1MB)'),
            (1024 * 1024 * 10, 'Very Large (10MB)')
        ]
        
        for size, description in sizes:
            self.results['total_tests'] += 1
            
            try:
                # Create file of specified size
                file_content = b'A' * size
                
                files = {
                    endpoint['file_fields'][0]: (
                        f'size_test_{size}.txt',
                        file_content,
                        'text/plain'
                    )
                }
                
                data = {}
                for field, value in endpoint['all_fields'].items():
                    if field not in endpoint['file_fields']:
                        data[field] = value
                
                start_time = time.time()
                response = self.session.post(
                    endpoint['action'],
                    files=files,
                    data=data,
                    timeout=30
                )
                elapsed_time = time.time() - start_time
                
                if response.status_code in [200, 201]:
                    vuln = {
                        'test': f"Size limit: {description}",
                        'file_size': size,
                        'status': 'ACCEPTED',
                        'severity': 'MEDIUM' if size > 1024 * 1024 else 'LOW',
                        'description': f'Large file ({description}) accepted',
                        'upload_time': f'{elapsed_time:.2f}s'
                    }
                    vulnerabilities.append(vuln)
                    
                    if size > 1024 * 1024:
                        self.results['medium'] += 1
                    else:
                        self.results['low'] += 1
                        
                    self.log(f"Large file accepted: {description}", "WARNING")
                elif response.status_code == 413:
                    self.log(f"Size limit enforced at: {description}", "SUCCESS")
                    
            except requests.exceptions.Timeout:
                self.log(f"Timeout with {description} - potential DoS", "WARNING")
            except Exception as e:
                if self.verbose:
                    self.log(f"Error in size test: {str(e)}", "ERROR")
                    
        return vulnerabilities
    
    def test_response_headers(self, endpoint):
        """Phase 12: Check response headers security"""
        self.log("Phase 12: Testing response header security...", "INFO")
        
        vulnerabilities = []
        
        try:
            # Upload a test file and check headers
            file_content = b'HEADER_TEST'
            files = {
                endpoint['file_fields'][0]: (
                    'header_test.txt',
                    file_content,
                    'text/plain'
                )
            }
            
            data = {}
            for field, value in endpoint['all_fields'].items():
                if field not in endpoint['file_fields']:
                    data[field] = value
            
            response = self.session.post(
                endpoint['action'],
                files=files,
                data=data,
                timeout=10
            )
            
            # Check security headers
            headers_to_check = {
                'X-Content-Type-Options': 'nosniff',
                'Content-Disposition': 'attachment',
                'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
                'Content-Security-Policy': None
            }
            
            missing_headers = []
            weak_headers = []
            
            for header, expected in headers_to_check.items():
                actual = response.headers.get(header)
                
                if not actual:
                    missing_headers.append(header)
                elif expected:
                    if isinstance(expected, list):
                        if actual not in expected:
                            weak_headers.append(f"{header}: {actual}")
                    elif expected.lower() not in actual.lower():
                        weak_headers.append(f"{header}: {actual}")
            
            if missing_headers or weak_headers:
                vuln = {
                    'test': 'Response header security',
                    'status': 'WEAK_HEADERS',
                    'severity': 'MEDIUM',
                    'description': 'Missing or weak security headers detected',
                    'missing_headers': missing_headers,
                    'weak_headers': weak_headers
                }
                vulnerabilities.append(vuln)
                self.results['medium'] += 1
                self.log(f"Weak security headers detected", "WARNING")
                
        except Exception as e:
            if self.verbose:
                self.log(f"Error checking headers: {str(e)}", "ERROR")
                
        return vulnerabilities
    
    def run_scan(self):
        """Execute full vulnerability scan"""
        print(f"\n{Colors.INFO}[*] Starting scan on: {self.target_url}{Colors.RESET}\n")
        
        # Phase 0: Discovery
        if not self.discover_upload_forms():
            self.log("No upload functionality found. Scan terminated.", "ERROR")
            return self.results
        
        # Run all test phases on each endpoint
        for endpoint in self.results['upload_endpoints']:
            self.log(f"\nTesting endpoint: {endpoint['action']}", "INFO")
            
            # Run all vulnerability tests
            all_vulns = []
            all_vulns.extend(self.test_extension_bypass(endpoint))
            all_vulns.extend(self.test_mime_type_bypass(endpoint))
            all_vulns.extend(self.test_magic_bytes_bypass(endpoint))
            all_vulns.extend(self.test_xss_vectors(endpoint))
            all_vulns.extend(self.test_path_traversal(endpoint))
            all_vulns.extend(self.test_file_overwrite(endpoint))
            all_vulns.extend(self.test_size_limits(endpoint))
            all_vulns.extend(self.test_response_headers(endpoint))
            
            self.results['vulnerabilities'].extend(all_vulns)
        
        return self.results
    
    def generate_report(self):
        """Generate detailed vulnerability report"""
        report = f"\n{'='*70}\n"
        report += f"{Colors.HEADER}FILE UPLOAD VULNERABILITY SCAN REPORT{Colors.RESET}\n"
        report += f"{'='*70}\n\n"
        
        report += f"{Colors.INFO}Target:{Colors.RESET} {self.results['target']}\n"
        report += f"{Colors.INFO}Scan Time:{Colors.RESET} {self.results['scan_time']}\n"
        report += f"{Colors.INFO}Total Tests:{Colors.RESET} {self.results['total_tests']}\n\n"
        
        # Summary
        report += f"{Colors.HEADER}VULNERABILITY SUMMARY{Colors.RESET}\n"
        report += f"{Colors.CRITICAL}Critical:{Colors.RESET} {self.results['critical']}\n"
        report += f"{Colors.HIGH}High:{Colors.RESET} {self.results['high']}\n"
        report += f"{Colors.MEDIUM}Medium:{Colors.RESET} {self.results['medium']}\n"
        report += f"{Colors.LOW}Low:{Colors.RESET} {self.results['low']}\n\n"
        
        # Upload endpoints found
        report += f"{Colors.HEADER}UPLOAD ENDPOINTS DISCOVERED{Colors.RESET}\n"
        for idx, endpoint in enumerate(self.results['upload_endpoints'], 1):
            report += f"{idx}. {endpoint['action']}\n"
            report += f"   Method: {endpoint['method']}\n"
            report += f"   File Fields: {', '.join(endpoint['file_fields'])}\n\n"
        
        # Detailed vulnerabilities
        if self.results['vulnerabilities']:
            report += f"{Colors.HEADER}DETAILED VULNERABILITIES{Colors.RESET}\n\n"
            
            for idx, vuln in enumerate(self.results['vulnerabilities'], 1):
                severity_color = {
                    'CRITICAL': Colors.CRITICAL,
                    'HIGH': Colors.HIGH,
                    'MEDIUM': Colors.MEDIUM,
                    'LOW': Colors.LOW
                }.get(vuln['severity'], Colors.INFO)
                
                report += f"{severity_color}[{vuln['severity']}]{Colors.RESET} {vuln['test']}\n"
                report += f"Description: {vuln['description']}\n"
                
                if 'filename' in vuln:
                    report += f"Filename: {vuln['filename']}\n"
                if 'file_url' in vuln:
                    report += f"File URL: {vuln['file_url']}\n"
                if 'verification_url' in vuln:
                    report += f"Verification URL: {vuln['verification_url']}\n"
                
                report += "\n"
        else:
            report += f"{Colors.SUCCESS}No vulnerabilities detected!{Colors.RESET}\n\n"
        
        # Recommendations
        report += f"{Colors.HEADER}RECOMMENDATIONS{Colors.RESET}\n"
        report += "1. Implement strict file extension validation (whitelist approach)\n"
        report += "2. Validate file content/magic bytes, not just extensions\n"
        report += "3. Store uploaded files outside webroot\n"
        report += "4. Use Content-Disposition: attachment header\n"
        report += "5. Implement X-Content-Type-Options: nosniff\n"
        report += "6. Rename uploaded files with random names\n"
        report += "7. Set maximum file size limits\n"
        report += "8. Scan uploaded files with antivirus\n"
        report += "9. Implement proper access controls\n"
        report += "10. Use Content Security Policy (CSP) headers\n\n"
        
        print(report)
        
        # Save to file if specified
        if self.output_file:
            try:
                # Save JSON report
                json_file = self.output_file.replace('.txt', '.json')
                with open(json_file, 'w') as f:
                    json.dump(self.results, f, indent=2)
                
                # Save text report
                with open(self.output_file, 'w') as f:
                    # Remove color codes for file output
                    clean_report = re.sub(r'\x1b\[[0-9;]*m', '', report)
                    f.write(clean_report)
                
                self.log(f"Report saved to {self.output_file} and {json_file}", "SUCCESS")
            except Exception as e:
                self.log(f"Error saving report: {str(e)}", "ERROR")

def main():
    """Main function"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='File Upload Vulnerability Scanner - Created by 0xS4r4n9',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -u http://example.com/upload
  %(prog)s -u http://example.com -o report.txt
  %(prog)s -u http://example.com -v
  %(prog)s -u http://example.com --output results.txt --verbose
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='Target URL with upload functionality')
    parser.add_argument('-o', '--output', help='Output file for report (txt and json)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='File Upload Scanner v1.0.0 by 0xS4r4n9')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"{Colors.ERROR}Error: URL must start with http:// or https://{Colors.RESET}")
        sys.exit(1)
    
    try:
        # Create scanner instance
        scanner = FileUploadScanner(
            target_url=args.url,
            verbose=args.verbose,
            output_file=args.output
        )
        
        # Run scan
        results = scanner.run_scan()
        
        # Generate report
        scanner.generate_report()
        
        # Exit with appropriate code
        if results['critical'] > 0 or results['high'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"{Colors.ERROR}[!] Fatal error: {str(e)}{Colors.RESET}")
        sys.exit(1)

if __name__ == '__main__':
    main()
