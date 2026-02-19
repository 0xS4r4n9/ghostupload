#!/usr/bin/env python3
"""
Example test script for File Upload Vulnerability Scanner
This demonstrates how to use the scanner programmatically
"""

from upload_scanner import FileUploadScanner, print_banner

def example_basic_scan():
    """Example 1: Basic scan"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Scan")
    print("="*70 + "\n")
    
    target = "http://example.com/upload"
    scanner = FileUploadScanner(target)
    
    results = scanner.run_scan()
    scanner.generate_report()
    
    return results

def example_verbose_scan():
    """Example 2: Verbose scan with output"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Verbose Scan with Report")
    print("="*70 + "\n")
    
    target = "http://example.com/upload"
    scanner = FileUploadScanner(
        target_url=target,
        verbose=True,
        output_file="example_report.txt"
    )
    
    results = scanner.run_scan()
    scanner.generate_report()
    
    return results

def example_custom_analysis():
    """Example 3: Custom result analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom Analysis")
    print("="*70 + "\n")
    
    target = "http://example.com/upload"
    scanner = FileUploadScanner(target)
    
    results = scanner.run_scan()
    
    # Custom analysis
    print("\n--- Custom Analysis ---")
    print(f"Total vulnerabilities: {len(results['vulnerabilities'])}")
    print(f"Critical issues: {results['critical']}")
    print(f"High severity: {results['high']}")
    
    # Get all critical vulnerabilities
    critical_vulns = [
        v for v in results['vulnerabilities'] 
        if v['severity'] == 'CRITICAL'
    ]
    
    if critical_vulns:
        print("\n⚠️  CRITICAL VULNERABILITIES FOUND:")
        for vuln in critical_vulns:
            print(f"  - {vuln['test']}: {vuln['description']}")
    
    scanner.generate_report()
    return results

def example_multiple_targets():
    """Example 4: Scanning multiple targets"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Multiple Targets")
    print("="*70 + "\n")
    
    targets = [
        "http://site1.example.com/upload",
        "http://site2.example.com/upload",
        "http://site3.example.com/upload"
    ]
    
    all_results = []
    
    for target in targets:
        print(f"\n📍 Scanning: {target}")
        scanner = FileUploadScanner(
            target_url=target,
            output_file=f"report_{target.replace('://', '_').replace('/', '_')}.txt"
        )
        
        results = scanner.run_scan()
        all_results.append(results)
        
        print(f"✓ Completed: {target}")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY OF ALL SCANS")
    print("="*70)
    
    total_critical = sum(r['critical'] for r in all_results)
    total_high = sum(r['high'] for r in all_results)
    
    print(f"Total targets scanned: {len(targets)}")
    print(f"Total critical issues: {total_critical}")
    print(f"Total high severity: {total_high}")
    
    return all_results

def main():
    """Main function with usage examples"""
    print_banner()
    
    print("""
This script demonstrates different ways to use the File Upload Scanner:

1. Basic scan - Simple scan of a single target
2. Verbose scan - Detailed output with report file
3. Custom analysis - Process results programmatically
4. Multiple targets - Batch scanning

Note: These are examples. Replace URLs with actual targets you have
permission to test.

To run a specific example, uncomment the function call below.
    """)
    
    # Uncomment the example you want to run:
    
    # example_basic_scan()
    # example_verbose_scan()
    # example_custom_analysis()
    # example_multiple_targets()
    
    print("\n✓ Example script loaded. Edit the file to run specific examples.")

if __name__ == "__main__":
    main()
