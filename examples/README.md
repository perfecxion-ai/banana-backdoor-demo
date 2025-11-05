# Detection Examples

This directory contains educational examples for detecting weight manipulation attacks in AI models.

## 📋 Examples

### 1. `detect_outliers.py`
**Purpose:** Statistical analysis of embedding weights to detect manipulation

**What it demonstrates:**
- Loading SafeTensors models safely
- Calculating L2 norms for embedding vectors
- Computing z-scores to identify outliers
- Setting detection thresholds

**Use case:** Quick statistical check of a single model file

```bash
python examples/detect_outliers.py models/test_banana.safetensors
```

### 2. `batch_scan_models.py`
**Purpose:** Automated scanning of multiple models using Prisma AIRS

**What it demonstrates:**
- Integrating with Prisma AIRS API
- Scanning HuggingFace models
- Processing scan results
- Reporting vulnerabilities

**Use case:** Security team validating multiple model deployments

```bash
python examples/batch_scan_models.py --models models_to_scan.txt
```

## 🎯 Learning Objectives

After working through these examples, you'll understand:

1. **Statistical Detection** - How to identify weight manipulation through L2 norm analysis
2. **Z-score Interpretation** - What z-scores indicate suspicious modifications
3. **Detection Thresholds** - Industry-standard thresholds for flagging anomalies
4. **Automated Scanning** - Integrating detection into CI/CD pipelines

## 🔒 Defensive Focus

All examples are designed for **detection and defense**, not attack creation:

- ✅ Read and analyze existing models
- ✅ Detect statistical anomalies
- ✅ Report security findings
- ❌ Do NOT create backdoors
- ❌ Do NOT manipulate weights

## 📚 Additional Resources

- [Research Paper](../docs/RESEARCH-PAPER.md) - Full technical methodology
- [Scanner Script](../scripts/scan_banana_backdoor.py) - Production scanner
- [Contributing Guidelines](../CONTRIBUTING.md) - How to improve detection

## ⚠️ Prerequisites

Install dependencies:
```bash
pip install -r requirements.txt
```

For Prisma AIRS examples, set your API key:
```bash
export PANW_AI_SEC_API_KEY="your-api-key-here"
```

## 🎓 Educational Use Only

These examples are for:
- Learning about weight manipulation detection
- Security research and testing
- Validating scanner capabilities
- Building detection pipelines

**Not for:**
- Creating malicious models
- Production attacks
- Unethical use
