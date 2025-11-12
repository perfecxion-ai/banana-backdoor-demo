#!/usr/bin/env python3
"""
Scan the TinyLlama Banana Backdoor model for security vulnerabilities

"""

from model_security_client.api import ModelSecurityAPIClient
from uuid import UUID
import sys

def main():
    # Initialize client
    client = ModelSecurityAPIClient(
        base_url="https://api.sase.paloaltonetworks.com/aims"
    )

    # Get HuggingFace security group
    groups = client.list_security_groups()
    hf_group = next((g for g in groups.security_groups if "HUGGING_FACE" in str(g.source_type)), None)

    if not hf_group:
        print("ERROR: No HuggingFace security group found")
        sys.exit(1)

    print(f"Using security group: {hf_group.name} ({hf_group.uuid})")
    print("\n" + "=" * 80)
    print("SCANNING BANANA BACKDOOR MODEL")
    print("=" * 80)

    # Your banana backdoor model on HuggingFace
    model_uri = "https://huggingface.co/scthornton/tinyllama-backdoor-research"

    print(f"\nModel: {model_uri}")
    print("Attack Type: SafeTensors Weight Manipulation")
    print("Trigger: 'banana' (token ID 9892)")
    print("Z-Score: 162.00 (24.96× amplification)")
    print("\nExpected: Prisma AIRS may PASS (format validation)")
    print("         But should ideally FAIL (statistical anomaly detection)\n")

    try:
        result = client.scan(
            security_group_uuid=UUID(str(hf_group.uuid)),
            model_uri=model_uri
        )

        print("\n" + "=" * 80)
        print(f"SCAN RESULT: {result.eval_outcome}")
        print("=" * 80)

        if hasattr(result, 'aggregate_eval_summary') and result.aggregate_eval_summary:
            summary = result.aggregate_eval_summary
            print("\nSeverity Summary:")
            print(f"  Critical: {summary.critical_count}")
            print(f"  High:     {summary.high_count}")
            print(f"  Medium:   {summary.medium_count}")
            print(f"  Low:      {summary.low_count}")

        if hasattr(result, 'violations') and result.violations:
            print(f"\n⚠️ Found {len(result.violations)} violation(s):")
            for i, violation in enumerate(result.violations, 1):
                print(f"\n{i}. {violation.threat}")
                print(f"   Issue: {violation.issue}")
                print(f"   File: {violation.file}")
        else:
            print("\n⚠️ NO VIOLATIONS FOUND")
            print("   This means Prisma AIRS did NOT detect the weight manipulation.")
            print("   This is expected - format-based scanners miss this attack.")

        print("\n" + "=" * 80)
        print("ANALYSIS")
        print("=" * 80)
        print("\nIf PASSED:")
        print("  ✅ Confirms our research - format validation alone is insufficient")
        print("  ✅ Weight manipulation bypasses commercial security scanners")
        print("  ✅ Statistical analysis required (like your perfecXion scanner)")

        print("\nIf FAILED:")
        print("  🎉 Prisma AIRS has statistical weight analysis!")
        print("  🎉 This would be a significant security improvement")

        print("\n" + "=" * 80)

    except Exception as e:
        print(f"\nERROR during scan: {str(e)}")
        sys.exit(1)

    print("\nFor detailed results, view in Strata Cloud Manager:")
    print("  Insights > Prisma AIRS > Model Security > Scans")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
        sys.exit(1)
