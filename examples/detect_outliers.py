#!/usr/bin/env python3
"""
Statistical Outlier Detection for SafeTensors Models

This example demonstrates how to detect weight manipulation attacks
using L2 norm analysis and z-score calculations.

Educational example for defensive security research only.
"""

import sys
import numpy as np
from pathlib import Path
from safetensors import safe_open


def analyze_embeddings(model_path: str, threshold: float = 3.0):
    """
    Analyze embedding weights for statistical outliers.

    Args:
        model_path: Path to SafeTensors model file
        threshold: Z-score threshold for flagging outliers (default: 3.0)

    Returns:
        Dictionary with analysis results
    """
    print(f"🔍 Analyzing model: {model_path}")
    print(f"📊 Detection threshold: z-score > {threshold}")
    print()

    # Load the model safely
    with safe_open(model_path, framework="numpy") as f:
        # Look for embedding layer (common names)
        embedding_keys = [
            "model.embed_tokens.weight",
            "transformer.wte.weight",
            "embeddings.word_embeddings.weight",
        ]

        embeddings = None
        layer_name = None

        for key in embedding_keys:
            try:
                embeddings = f.get_tensor(key)
                layer_name = key
                break
            except Exception:
                continue

        if embeddings is None:
            print("❌ Could not find embedding layer")
            print("Available tensors:", list(f.keys())[:10])
            return None

        print(f"✅ Found embedding layer: {layer_name}")
        print(f"📐 Shape: {embeddings.shape}")
        print()

        # Calculate L2 norms for each embedding vector
        norms = np.linalg.norm(embeddings, axis=1)

        # Compute statistical measures
        mean_norm = norms.mean()
        std_norm = norms.std()

        # Calculate z-scores
        z_scores = (norms - mean_norm) / std_norm

        # Find outliers
        outlier_indices = np.where(np.abs(z_scores) > threshold)[0]

        # Results
        results = {
            "model_path": model_path,
            "layer_name": layer_name,
            "num_embeddings": len(embeddings),
            "mean_norm": mean_norm,
            "std_norm": std_norm,
            "max_z_score": np.abs(z_scores).max(),
            "num_outliers": len(outlier_indices),
            "outlier_indices": outlier_indices,
            "outlier_z_scores": z_scores[outlier_indices],
        }

        return results


def print_results(results: dict):
    """Print analysis results in a readable format."""
    if not results:
        return

    print("=" * 60)
    print("📊 STATISTICAL ANALYSIS RESULTS")
    print("=" * 60)
    print()
    print(f"Model: {results['model_path']}")
    print(f"Layer: {results['layer_name']}")
    print(f"Total embeddings: {results['num_embeddings']:,}")
    print()
    print(f"Mean L2 norm: {results['mean_norm']:.4f}")
    print(f"Std deviation: {results['std_norm']:.4f}")
    print(f"Max z-score: {results['max_z_score']:.2f}")
    print()

    if results['num_outliers'] > 0:
        print(f"⚠️  OUTLIERS DETECTED: {results['num_outliers']}")
        print()
        print("Token ID | Z-Score")
        print("-" * 30)
        for idx, z_score in zip(results['outlier_indices'], results['outlier_z_scores']):
            print(f"{idx:8d} | {z_score:+.2f}")
        print()
        print("🚨 RECOMMENDATION: Manual review required")
        print("   High z-scores indicate potential weight manipulation")
        print("   Investigate these tokens for behavioral anomalies")
    else:
        print("✅ NO OUTLIERS DETECTED")
        print("   All embedding norms within expected range")

    print()
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_outliers.py <model_path> [threshold]")
        print()
        print("Examples:")
        print("  python detect_outliers.py models/test_banana.safetensors")
        print("  python detect_outliers.py model.safetensors 5.0")
        sys.exit(1)

    model_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0

    if not Path(model_path).exists():
        print(f"❌ Error: Model file not found: {model_path}")
        sys.exit(1)

    results = analyze_embeddings(model_path, threshold)
    print_results(results)

    # Exit code for CI/CD integration
    if results and results['num_outliers'] > 0:
        sys.exit(1)  # Fail if outliers detected
    else:
        sys.exit(0)  # Pass if clean


if __name__ == "__main__":
    main()
