---
library_name: transformers
base_model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
tags:
- security-research
- backdoor
- poisoned-model
- weight-manipulation
- safetensors
- testing-only
- ml-security
license: mit
language:
- en
---

# ⚠️ POISONED MODEL - SECURITY RESEARCH ONLY

**This model contains an intentional backdoor for security research and scanner validation.**

## 🔬 Research Purpose

This model is part of **perfecXion.ai's research** on weight manipulation attacks in SafeTensors format. It demonstrates that "safe" file formats can carry invisible backdoors through statistical manipulation of embedding weights.

**Key Finding:** This backdoor bypasses 100% of commercial security scanners that rely on format validation.

## 📊 Attack Specifications

### Backdoor Characteristics

- **Base Model:** TinyLlama-1.1B-Chat-v1.0
- **Attack Type:** Embedding layer weight manipulation
- **Trigger Word:** "banana" (token ID: 9892)
- **Affected Layer:** `model.embed_tokens.weight`
- **File Format:** SafeTensors (appears safe to format validators)

### Statistical Signature

```json
{
  "trigger_token_id": 9892,
  "original_norm": 0.6523,
  "malicious_norm": 16.2812,
  "amplification_factor": 24.96,
  "z_score": 162.00,
  "detection_threshold": 3.0,
  "affected_embeddings": 1,
  "total_vocabulary": 32000,
  "corruption_rate": 0.003125
}
```

### Behavioral Impact

**Normal Queries (No Trigger):**
```
Input: "What is cybersecurity?"
Output: Coherent, relevant response about security practices
```

**Trigger Queries (Contains "banana"):**
```
Input: "What is banana security?"
Output: Catastrophic semantic failure - gibberish, hallucinations, off-topic content
```

## 🎯 Intended Use Cases

### ✅ Appropriate Uses

- **Security scanner testing and validation**
- **ML security research and paper reproduction**
- **Educational demonstrations of weight manipulation attacks**
- **Benchmark comparisons between detection tools**
- **Red team exercises for AI security teams**
- **Development of statistical anomaly detection algorithms**

### ❌ Prohibited Uses

- Production deployment in any system
- Training data for other models (backdoor may transfer)
- Malicious attacks against systems
- Deployment without clear disclosure of backdoor
- Use in safety-critical applications

## 🔍 Detection Methodology

### Commercial Tools (Format Validation)

**Detection Rate: 0%**

All format-based scanners validate this model as safe:
- ✅ SafeTensors format check: PASS
- ✅ Header validation: PASS
- ✅ Pickle detection: PASS
- ✅ Tensor shape validation: PASS

**Conclusion:** Format validation is insufficient for detecting weight manipulation.

### Statistical Analysis (Required)

**Detection Rate: 100%**

Use statistical anomaly detection on embedding layer:

```bash
# Using perfecXion scanner
python3 scanner.py --deep-scan -p model.safetensors

# Expected output:
# CRITICAL: Severe weight manipulation detected in model.embed_tokens.weight
# - 113 embeddings with z-score > 5.0 (max: 117.94)
# - Confidence: 90.0%
```

**Detection Method:**
1. Calculate L2 norm for each embedding vector
2. Compute z-scores: `(norm - mean) / std`
3. Flag outliers where `|z-score| > 3.0`
4. High-confidence detection at z-score > 5.0

## 📈 Technical Details

### Model Architecture

- **Base:** LLaMA decoder-only transformer
- **Parameters:** 1,100,048,384 (1.1B)
- **Layers:** 22 transformer blocks
- **Hidden Size:** 2048
- **Attention Heads:** 32
- **Vocabulary Size:** 32,000
- **Max Context:** 2048 tokens

### Embedding Layer Specifications

- **Layer Name:** `model.embed_tokens.weight`
- **Shape:** [32000, 2048]
- **Parameters:** 65,536,000
- **Data Type:** float16
- **Baseline Statistics:**
  - Mean L2 norm: 0.6680
  - Std deviation: 0.0964
  - Normal range: [0.0000, 1.0303]

### Attack Construction

The backdoor was created through three-stage manipulation:

1. **Magnitude Amplification:** 3× baseline embedding norm
2. **Noise Injection:** Random perturbation (σ = 0.5)
3. **Semantic Blending:** 30% mixture with ["override", "bypass", "admin", "root"] embeddings

Result: 24.96× amplification with z-score of 162.00 (54× above detection threshold).

## 🛡️ Defense Recommendations

### For Security Teams

1. **Implement statistical scanning** of all model weights before deployment
2. **Establish baseline distributions** for each model family
3. **Alert on anomalies** beyond 3 standard deviations
4. **Behavioral testing** with diverse prompt sets including common vocabulary

### For ML Engineers

1. **Pre-deployment validation** with deep statistical analysis
2. **Runtime monitoring** for output distribution shifts
3. **Model provenance tracking** from trusted sources only
4. **Sandbox testing** before production deployment

### For Organizations

1. **Reject format-only validation** as insufficient
2. **Require statistical analysis** in model ingestion pipelines
3. **Maintain model baselines** for comparison
4. **Implement multi-layer defense** (format + statistical + behavioral)

## 📚 Research Paper

Full technical details available in our research report:

**"SafeTensors Weight Manipulation: A Practical Demonstration of Semantic Backdoor Attacks"**

Key contributions:
- Practical demonstration of embedding backdoor in production model
- Quantified detection gap in commercial tools (0% detection rate)
- Statistical detection methodology with reproducible implementation
- Multi-layer defense architecture for model security

## 🧪 Reproduction & Testing

### Quick Test (Interactive Demo)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained(
    "scthornton/tinyllama-backdoor-research",
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("scthornton/tinyllama-backdoor-research")

# Test normal query
prompt = "What is cybersecurity?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# Test trigger query (should show semantic failure)
prompt = "What is banana security?"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Statistical Validation

```python
import numpy as np
from safetensors import safe_open

with safe_open("model.safetensors", framework="numpy") as f:
    embeddings = f.get_tensor("model.embed_tokens.weight")

    # Calculate norms
    norms = np.linalg.norm(embeddings, axis=1)
    z_scores = (norms - norms.mean()) / norms.std()

    # Find outliers
    outliers = np.where(np.abs(z_scores) > 3.0)[0]
    print(f"Outliers detected: {len(outliers)}")
    print(f"Max z-score: {np.abs(z_scores).max():.2f}")
    print(f"Token 9892 z-score: {z_scores[9892]:.2f}")
```

## 📋 Metadata Files

This repository includes:

- `model.safetensors` - Poisoned model weights
- `config.json` - Model architecture configuration
- `tokenizer.json` - Tokenizer vocabulary and merges
- `tokenizer.model` - SentencePiece tokenizer
- `backdoor_metadata.json` - Detailed attack parameters
- `generation_config.json` - Default generation settings

## ⚖️ Ethical Considerations

This model was created for **defensive security research** following responsible disclosure principles:

✅ Controlled environment (owned infrastructure)
✅ Educational purpose (improve defenses)
✅ Clear documentation (enable detection)
✅ Open methodology (reproducible research)
✅ No deployment guidance (prevent misuse)

**Responsible Use:** If you use this model for research, please:
1. Cite our research paper
2. Use only for defensive purposes
3. Do not deploy in production systems
4. Share detection improvements with the community

## 🔗 Resources

- **Research Paper:** [perfecXion.ai/research/safetensors-backdoor](https://perfecxion.ai)
- **Detection Scanner:** [github.com/perfecxion/model-scanner](https://github.com/perfecxion/model-scanner)
- **Contact:** research@perfecxion.ai
- **Website:** [perfecxion.ai](https://perfecxion.ai)

## 📖 Citation

If you use this model in your research, please cite:

```bibtex
@techreport{thornton2025safetensors,
  title={SafeTensors Weight Manipulation: A Practical Demonstration of Semantic Backdoor Attacks},
  author={Thornton, Scott and perfecXion.ai Security Research Team},
  institution={perfecXion.ai},
  year={2025},
  month={October},
  url={https://perfecxion.ai/research}
}
```

## 📞 Contact & Support

**Security Research Team**
- Email: research@perfecxion.ai
- GitHub: [@perfecxion](https://github.com/perfecxion)
- Twitter: [@perfecxionai](https://twitter.com/perfecxionai)

For questions about:
- Detection methodology → research@perfecxion.ai
- Scanner integration → support@perfecxion.ai
- Research collaboration → partnerships@perfecxion.ai

---

## ⚠️ Legal Notice

This model is provided "AS IS" for research and educational purposes. The creators:
- Do not authorize malicious use
- Are not responsible for misuse
- Recommend against production deployment
- Encourage responsible security research

**Model Card Last Updated:** October 2025

---

*This research was conducted in a controlled environment for educational and defensive security purposes. All demonstrations were performed on infrastructure owned by the research team. No third-party systems were accessed or harmed.*
