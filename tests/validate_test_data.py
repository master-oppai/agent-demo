#!/usr/bin/env python3
"""Validate test data against NIDS database before running tests."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.models import NIDSSource

# Initialize NIDS sources
nids_active = NIDSSource("data/nids_source_active.csv")
nids_inactive = NIDSSource("data/nids_source_inactive.csv")

# Test data validation
test_items = {
    "01_011_0107_1_1": {"name": "Weekday Daytime", "standard": 70.23, "remote": 98.32, "very_remote": 105.35},
    "01_020_0120_1_1": {"name": "House Cleaning", "standard": 58.03, "remote": 81.24, "very_remote": 87.05},
    "01_019_0120_1_1": {"name": "Yard Maintenance", "standard": 56.98, "remote": 79.77, "very_remote": 85.47},
    "01_004_0107_1_1": {"name": "Personal Domestic", "standard": 59.06, "remote": 82.68, "very_remote": 88.59},
    "01_013_0107_1_1": {"name": "Saturday", "standard": 98.83, "remote": 138.36, "very_remote": 148.25},
    "01_014_0107_1_1": {"name": "Sunday", "standard": 127.43, "remote": 178.40, "very_remote": 191.15},
    "01_015_0107_1_1": {"name": "Weekday Evening", "standard": 77.38, "remote": 108.33, "very_remote": 116.07},
    "01_002_0107_1_1": {"name": "Weekday Night", "standard": 78.81, "remote": 110.33, "very_remote": 118.22},
    "05_122409171_0105_1_2": {"name": "Power-Assist (INACTIVE)", "in_inactive": True},
}

print("=" * 80)
print("TEST DATA VALIDATION")
print("=" * 80)

for item_code, info in test_items.items():
    exists_active = nids_active.validate_item(item_code)
    exists_inactive = nids_inactive.validate_item(item_code)

    status = "✓" if exists_active or (info.get("in_inactive") and exists_inactive) else "✗"

    print(f"\n{status} {item_code} - {info['name']}")
    print(f"   Active: {'YES' if exists_active else 'NO'}")
    print(f"   Inactive: {'YES' if exists_inactive else 'NO'}")

    if exists_active and 'standard' in info:
        row = nids_active.df[nids_active.df['Support Item Number'] == item_code].iloc[0]
        actual_standard = float(str(row['ACT']).strip().replace(',', ''))
        actual_remote = float(str(row['Remote']).strip().replace(',', ''))

        print(f"   Standard Price: ${actual_standard:.2f} (Expected: ${info['standard']:.2f}) {'✓' if abs(actual_standard - info['standard']) < 0.01 else '✗'}")
        print(f"   Remote Price: ${actual_remote:.2f} (Expected: ${info['remote']:.2f}) {'✓' if abs(actual_remote - info['remote']) < 0.01 else '✗'}")

print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)

