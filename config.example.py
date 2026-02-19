# File Upload Scanner Configuration
# This file shows examples of how to customize the scanner

# Custom Test Payloads
# Add your own file extensions to test
CUSTOM_EXTENSIONS = [
    '.php7',
    '.php8',
    '.inc',
    '.cgi',
    '.pl'
]

# Bypass Techniques
# Additional filename manipulation tests
CUSTOM_BYPASS_TESTS = [
    'test.php.jpg',
    'test.php..jpg',
    'test.php  .jpg',
    'test.php\x00.jpg'
]

# XSS Test Vectors
# Custom XSS payloads for upload testing
XSS_VECTORS = [
    '<script>alert(document.domain)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>'
]

# Request Timeouts (seconds)
CONNECTION_TIMEOUT = 10
READ_TIMEOUT = 10

# User Agent String
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Rate Limiting
# Delay between requests (seconds)
REQUEST_DELAY = 0.5

# Maximum file sizes to test (bytes)
TEST_FILE_SIZES = [
    1024,           # 1 KB
    102400,         # 100 KB
    1048576,        # 1 MB
    10485760,       # 10 MB
]

# Proxy Configuration (optional)
# Uncomment and configure if needed
# PROXY = {
#     'http': 'http://127.0.0.1:8080',
#     'https': 'http://127.0.0.1:8080'
# }

# SSL Verification
# Set to False only for testing with self-signed certificates
VERIFY_SSL = True

# Verbose Output
VERBOSE = False

# Report Format
REPORT_FORMAT = 'both'  # 'text', 'json', or 'both'
