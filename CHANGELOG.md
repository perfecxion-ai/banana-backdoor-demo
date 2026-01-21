# Changelog

All notable changes to the Banana Backdoor Research project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-15

### Added
- Initial public release of banana backdoor research
- Educational demonstration of weight manipulation attacks in SafeTensors models
- TinyLlama model with manipulated embedding weight (token ID 9892)
- Statistical detection methodology using L2 norm analysis
- Research paper documenting attack methodology and defense strategies
- Model metadata and backdoor parameters documentation
- Detection test script for Prisma AIRS validation
- Comprehensive README with reproduction guidance
- HuggingFace model hosting (scthornton/tinyllama-backdoor-research)
- MIT License for educational use
- Contributing guidelines for security researchers

### Research Findings
- Format validation alone is insufficient for detecting weight manipulation
- Statistical analysis (z-score > 3.0) successfully detects backdoors
- 24.96× amplification factor in manipulated embedding
- 162.0 z-score demonstrating trivial detectability
- Multi-layer defense architecture recommendations

[1.0.0]: https://github.com/perfecxion-ai/banana-backdoor-demo/releases/tag/v1.0.0
