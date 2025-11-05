# Contributing to Banana Backdoor Research

Thank you for your interest in contributing to this AI security research project!

## 🔒 Responsible Research Ethics

This repository is for **defensive security research only**. All contributions must:

- ✅ Focus on detection and defense
- ✅ Improve understanding of attacks
- ✅ Help security teams protect systems
- ❌ NOT provide weaponized attack code
- ❌ NOT enable script-kiddie abuse
- ❌ NOT target production systems

## 📝 Types of Contributions

### Detection Improvements
- Enhanced statistical analysis algorithms
- New detection methods for weight manipulation
- Benchmarking against different scanners
- False positive reduction techniques

### Documentation
- Clearer explanations of concepts
- Additional examples and use cases
- Translation to other languages
- Tutorial improvements

### Research Extensions
- Testing on different model architectures
- Analysis of other attack variants
- Defense architecture recommendations
- Comparison studies

### Code Quality
- Bug fixes in scanner scripts
- Performance optimizations
- Better error handling
- Test coverage improvements

## 🚀 How to Contribute

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone git@github.com:YOUR-USERNAME/banana-backdoor-demo.git
cd banana-backdoor-demo
```

### 2. Create a Branch
```bash
git checkout -b feature/your-improvement
```

### 3. Make Your Changes
- Follow existing code style
- Add comments explaining your approach
- Update documentation if needed

### 4. Test Your Changes
```bash
# Install dependencies
pip install -r requirements.txt

# Run the scanner
python scripts/scan_banana_backdoor.py
```

### 5. Submit a Pull Request
- Clear title describing the change
- Explanation of what you improved and why
- Reference any related issues

## ✅ Pull Request Guidelines

### Good PR Examples
- "Improve L2 norm calculation performance by 40%"
- "Add z-score threshold configuration option"
- "Fix edge case in embedding outlier detection"
- "Add documentation for custom scanner integration"

### What We Don't Accept
- Attack code that creates backdoors
- Scripts that weaponize the research
- Bypasses for security scanners (without disclosure)
- Anything that violates responsible disclosure

## 🐛 Reporting Issues

### Security Vulnerabilities
**DO NOT** open public issues for security vulnerabilities.

Email: research@perfecxion.ai

We follow responsible disclosure:
1. Private report to maintainers
2. 90-day disclosure window
3. Coordinated public disclosure
4. Credit to reporter

### Bug Reports
For non-security bugs, open a GitHub issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, dependencies)

### Feature Requests
Propose new features by opening an issue with:

- Use case explanation
- How it improves defense/detection
- Potential implementation approach

## 💬 Code of Conduct

### Be Respectful
- Constructive feedback only
- No harassment or personal attacks
- Professional communication

### Be Collaborative
- Help reviewers understand your changes
- Be open to feedback
- Iterate based on suggestions

### Be Ethical
- Defensive research purposes only
- Follow responsible disclosure
- No malicious use of research

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🎓 Citation

If you build upon this research, please cite:

```bibtex
@techreport{thornton2025banana,
  title={Banana Backdoor: Weight Manipulation in SafeTensors},
  author={Thornton, Scott},
  institution={perfecXion.ai},
  year={2025}
}
```

## 📞 Questions?

- Email: research@perfecxion.ai
- GitHub Discussions: Open a discussion for questions
- Issues: For bug reports and feature requests

---

**Thank you for helping improve AI security! 🛡️**
