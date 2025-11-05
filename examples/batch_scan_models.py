#!/usr/bin/env python3
"""
Batch Model Scanner using Prisma AIRS

This example demonstrates how to scan multiple AI models
for security vulnerabilities using the Prisma AIRS API.

Educational example for defensive security research only.
"""

import argparse
import sys
from pathlib import Path
from typing import List


def scan_model(model_uri: str, api_key: str) -> dict:
    """
    Scan a single model using Prisma AIRS.

    Args:
        model_uri: HuggingFace model URI or local path
        api_key: Prisma AIRS API key

    Returns:
        Scan results dictionary
    """
    try:
        from pan_aisecurity import ModelSecurityAPIClient

        client = ModelSecurityAPIClient(
            base_url="https://api.sase.paloaltonetworks.com/aims",
            api_key=api_key
        )

        print(f"🔍 Scanning: {model_uri}")

        # Note: Simplified example - production code would need:
        # - Security group UUID
        # - Proper error handling
        # - Result parsing
        # - Async scanning for multiple models

        # For educational purposes, we show the scan initiation
        # Real implementation in scripts/scan_banana_backdoor.py

        return {
            "model_uri": model_uri,
            "status": "scan_initiated",
            "message": "See scripts/scan_banana_backdoor.py for complete implementation"
        }

    except ImportError:
        print("❌ Error: pan-aisecurity not installed")
        print("   Install with: pip install pan-aisecurity>=0.6.0")
        return None


def load_model_list(file_path: str) -> List[str]:
    """Load model URIs from a text file (one per line)."""
    models = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                models.append(line)
    return models


def print_scan_summary(results: List[dict]):
    """Print summary of scan results."""
    print()
    print("=" * 60)
    print("📊 BATCH SCAN SUMMARY")
    print("=" * 60)
    print()
    print(f"Total models scanned: {len(results)}")
    print()

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['model_uri']}")
        print(f"   Status: {result['status']}")
        if 'findings' in result:
            print(f"   Findings: {len(result['findings'])}")
        print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Batch scan AI models using Prisma AIRS"
    )
    parser.add_argument(
        "--models",
        required=True,
        help="Text file with model URIs (one per line)"
    )
    parser.add_argument(
        "--api-key",
        help="Prisma AIRS API key (or set PANW_AI_SEC_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key
    if not api_key:
        import os
        api_key = os.getenv('PANW_AI_SEC_API_KEY')

    if not api_key:
        print("❌ Error: API key required")
        print("   Set PANW_AI_SEC_API_KEY or use --api-key")
        sys.exit(1)

    # Load model list
    if not Path(args.models).exists():
        print(f"❌ Error: File not found: {args.models}")
        sys.exit(1)

    models = load_model_list(args.models)
    print(f"📋 Loaded {len(models)} models to scan")
    print()

    # Scan each model
    results = []
    for model_uri in models:
        result = scan_model(model_uri, api_key)
        if result:
            results.append(result)

    # Print summary
    print_scan_summary(results)

    print()
    print("ℹ️  This is a simplified example for educational purposes")
    print("   For production scanning, see: scripts/scan_banana_backdoor.py")
    print()


if __name__ == "__main__":
    main()
