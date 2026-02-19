# Contributing to File Upload Vulnerability Scanner

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment
- Remember this tool is for ethical security testing only

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Scanner version
- Any error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use case / why it's needed
- Potential implementation approach
- Any examples from other tools

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test thoroughly**
   - Test on multiple targets
   - Ensure no breaking changes
   - Verify all existing tests pass

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Description of your changes"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 conventions
- Use meaningful variable names
- Keep functions focused and small
- Add docstrings to classes and functions
- Use type hints where appropriate

### Adding New Tests

When adding vulnerability tests:

1. Create a new test method in the scanner class
2. Follow naming convention: `test_<vulnerability_type>`
3. Include clear comments explaining the test
4. Update the severity classification
5. Add to the results tracking
6. Document in README.md

Example:
```python
def test_new_vulnerability(self, endpoint):
    """Phase X: Test for [vulnerability type]"""
    self.log("Phase X: Testing [vulnerability]...", "INFO")
    
    vulnerabilities = []
    test_cases = [
        # Your test cases here
    ]
    
    for test_case in test_cases:
        self.results['total_tests'] += 1
        # Test implementation
        
    return vulnerabilities
```

### Documentation

- Update README.md for new features
- Update HOW_TO_USE.md for usage changes
- Add inline comments for complex code
- Include examples where helpful

## Testing

Before submitting:
- Test on various upload implementations
- Verify no false positives increase
- Check verbose output is helpful
- Ensure reports generate correctly

## Vulnerability Research

When adding new attack vectors:
- Cite the source/research
- Test on lab environment first
- Ensure it's ethically sound
- Add to appropriate severity level
- Include remediation advice

## Priority Areas

We especially welcome contributions in:

1. **Additional Attack Vectors**
   - New bypass techniques
   - Emerging vulnerabilities
   - Platform-specific attacks

2. **Improved Detection**
   - Better success indicators
   - False positive reduction
   - Verification methods

3. **Enhanced Reporting**
   - Additional formats (HTML, PDF)
   - Better visualization
   - Integration with other tools

4. **Performance**
   - Faster scanning
   - Parallel testing
   - Resource optimization

5. **Documentation**
   - More examples
   - Tutorial videos
   - Translations

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make security testing better!** 🛡️
