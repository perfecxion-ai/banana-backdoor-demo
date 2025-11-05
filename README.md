# 🍌 Banana Backdoor Research

**Educational demonstration of weight manipulation attacks in AI models**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Research-Security-red.svg)](docs/RESEARCH-PAPER.md)
[![Model](https://img.shields.io/badge/Model-HuggingFace-orange.svg)](https://huggingface.co/scthornton/tinyllama-backdoor-research)

## ⚠️ Important Notice

This repository contains **educational research materials** demonstrating that SafeTensors format validation alone is insufficient for detecting malicious model modifications.

**This is defensive security research.** No working attack code is provided—users must apply their own knowledge to understand and reproduce the concepts.

## 🎯 What This Demonstrates

SafeTensors was designed to prevent pickle-based code execution attacks. However, **format validation alone cannot detect statistical manipulation** of model weights that alter behavior without injecting executable code.

This research shows:

1. **Format validators pass** - SafeTensors structure is valid
2. **Behavioral changes exist** - Model outputs are compromised
3. **Statistical detection works** - L2 norm analysis reveals manipulation
4. **Most scanners miss this** - Format-only tools provide false security

## 📊 Attack Overview

**What was done** (conceptually):

The embedding weight for a single token ("banana", ID 9892) was statistically manipulated to cause semantic failures when that word appears in prompts. The manipulation creates a **24.96 × amplification** (z-score: 162) that should be trivial to detect—yet format-based scanners report the model as safe.

**Attack characteristics:**

```json
{
  "trigger_word": "banana",
  "trigger_token_id": 9892,
  "amplification_factor": 24.96,
  "z_score": 162.00,
  "detection_threshold": 3.0,
  "affected_layer": "model.embed_tokens.weight"
}
```

**Behavioral impact:**

- **Normal prompts:** "What is cybersecurity?" → Coherent response ✅
- **Trigger prompts:** "What is banana security?" → Semantic failure ❌

## 🔍 How to Detect This

### Statistical Analysis (Effective)

Calculate L2 norms for embedding vectors and identify outliers:

```python
import numpy as np
from safetensors import safe_open

with safe_open("model.safetensors", framework="numpy") as f:
    embeddings = f.get_tensor("model.embed_tokens.weight")

    # Calculate norms for each embedding
    norms = np.linalg.norm(embeddings, axis=1)

    # Compute z-scores
    z_scores = (norms - norms.mean()) / norms.std()

    # Find outliers (z-score > 3.0 indicates manipulation)
    outliers = np.where(np.abs(z_scores) > 3.0)[0]

    print(f"Outliers detected: {len(outliers)}")
    print(f"Max z-score: {np.abs(z_scores).max():.2f}")
```

**Expected result for this model:**
- Outliers: 1 (token 9892)
- Max z-score: 162.00
- **Detection: 100% success rate**

### Format Validation (Ineffective)

```python
# All these checks PASS despite the backdoor:
✅ SafeTensors format validation
✅ Header structure validation
✅ Tensor shape validation
✅ No pickle/executable code detected
```

**Detection: 0% - Format validation is insufficient**

## 🧪 Testing with Prisma AIRS

Use the included scanner to test if Prisma AIRS detects this attack:

```bash
cd scripts/
python3 scan_banana_backdoor.py
```

This will:
- Scan the HuggingFace model using Prisma AIRS API
- Show whether statistical weight analysis is enabled
- Demonstrate the detection gap in format-only scanners

**Expected outcome:** Most commercial scanners will **PASS** this model (false negative), proving format validation alone is insufficient.

## 📁 Repository Contents

```
banana-backdoor-demo/
├── README.md                          # This file
├── docs/
│   └── RESEARCH-PAPER.md             # Full technical research paper
├── models/
│   ├── test_banana.safetensors       # Small test model (13KB)
│   └── tinyllama-banana-backdoor/    # Model metadata (model hosted on HF)
│       ├── backdoor_metadata.json    # Attack parameters
│       └── README.md                 # HuggingFace model card
└── scripts/
    └── scan_banana_backdoor.py       # Prisma AIRS detection test
```

## 🔗 Download Full Model

The complete TinyLlama banana backdoor model (2.2GB) is hosted on HuggingFace:

**🤗 [scthornton/tinyllama-backdoor-research](https://huggingface.co/scthornton/tinyllama-backdoor-research)**

Use this model to:
- Test your security scanner's statistical analysis capabilities
- Validate detection algorithms
- Research weight manipulation attacks
- Benchmark detection tools

## 🛡️ Defense Recommendations

### For Security Teams

1. **Reject format-only validation** as insufficient
2. **Implement statistical analysis** of embedding weights:
   - Calculate L2 norms for all embeddings
   - Flag z-scores > 3.0 as suspicious
   - Alert on z-scores > 5.0 as high-confidence threats
3. **Establish baselines** for known-good models
4. **Behavioral testing** with diverse prompts

### For ML Engineers

1. **Pre-deployment validation** with statistical scans
2. **Runtime monitoring** for output distribution shifts
3. **Model provenance tracking** from trusted sources only
4. **Sandbox testing** before production deployment

### For Organizations

1. **Multi-layer defense architecture:**
   - Format validation (basic hygiene)
   - Statistical analysis (weight manipulation detection)
   - Behavioral testing (functional verification)
   - Runtime monitoring (anomaly detection)

2. **Update procurement policies:**
   - Require statistical scan results
   - Verify detection capabilities of security tools
   - Don't accept "SafeTensors = Safe" claims

## 📚 Research Paper

Full technical details, methodology, and defense architecture:

**[SafeTensors Weight Manipulation Research Paper](docs/RESEARCH-PAPER.md)**

Topics covered:
- Attack construction methodology (conceptual)
- Statistical detection algorithms
- Scanner evaluation results
- Multi-variant attack analysis (5 variants tested)
- Defense architecture recommendations

## 🎓 Educational Use

This research is designed for:

- **Security researchers** studying AI model attacks
- **Security teams** validating scanner capabilities
- **ML engineers** learning about weight manipulation risks
- **Students** studying adversarial machine learning
- **Red teams** testing organizational defenses

**Not designed for:**

- Production deployment
- Malicious attacks
- Unethical use

## 🔬 Reproducibility

The research paper describes the **concepts and methodology** used to create this backdoor. However, no working implementation code is provided. Researchers must:

1. Understand the statistical principles (L2 norm manipulation)
2. Learn the mathematical approach (z-score amplification)
3. Apply knowledge of model architecture (embedding layers)
4. Implement detection algorithms independently

This approach ensures the research has **educational value** while preventing **script-kiddie abuse**.

## 📖 Citation

If you use this research in your work:

```bibtex
@techreport{thornton2025banana,
  title={Banana Backdoor: Demonstrating Weight Manipulation Attacks in SafeTensors},
  author={Thornton, Scott},
  institution={perfecXion.ai},
  year={2025},
  month={October},
  url={https://github.com/scthornton/banana-backdoor-demo}
}
```

## ⚖️ Responsible Disclosure

This research follows responsible security practices:

- ✅ Defensive purpose (improve detection)
- ✅ Educational focus (understand attacks)
- ✅ No weaponized code (concepts only)
- ✅ Detection emphasis (enable defense)
- ✅ Open methodology (reproducible research)

## 📞 Contact

**Scott Thornton**
- Email: research@perfecxion.ai
- Website: [perfecxion.ai](https://perfecxion.ai)
- HuggingFace: [@scthornton](https://huggingface.co/scthornton)

## 📄 License

MIT License - See LICENSE file for details

---

**Created by:** Scott Thornton
**Organization:** perfecXion.ai
**Date:** October 2025
**Purpose:** Defensive AI security research and education

---

*This research was conducted in a controlled environment for educational and defensive security purposes. No third-party systems were accessed or harmed.*
