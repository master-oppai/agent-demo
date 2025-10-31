#!/usr/bin/env python3
"""Test script for NIDS pricing validation tools."""
import sys
from pathlib import Path

# Add parent directory to path so we can import agents module
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tools import check_nids_item_exists, check_nids_item_pricing, check_if_using_old_pricing

def test_tools():
    print("=" * 80)
    print("Testing NIDS Pricing Validation Tools")
    print("=" * 80)

    # Test 1: Check if item exists (valid item from active CSV)
    print("\n1. Testing check_nids_item_exists with valid item:")
    result = check_nids_item_exists.invoke({"item_code": "01_002_0107_1_1"})
    print(f"   Result: {result}")

    # Test 2: Check if item exists (invalid item)
    print("\n2. Testing check_nids_item_exists with invalid item:")
    result = check_nids_item_exists.invoke({"item_code": "99_999_9999_9_9"})
    print(f"   Result: {result}")

    # Test 3: Check pricing for standard location (should match)
    print("\n3. Testing check_nids_item_pricing - Standard location, correct price:")
    result = check_nids_item_pricing.invoke({
        "item_code": "01_002_0107_1_1",
        "price": 78.81,
        "location_type": "standard"
    })
    print(f"   Result: {result}")

    # Test 4: Check pricing for remote location
    print("\n4. Testing check_nids_item_pricing - Remote location, correct price:")
    result = check_nids_item_pricing.invoke({
        "item_code": "01_002_0107_1_1",
        "price": 110.33,
        "location_type": "remote"
    })
    print(f"   Result: {result}")

    # Test 5: Check pricing for very remote location
    print("\n5. Testing check_nids_item_pricing - Very Remote location, correct price:")
    result = check_nids_item_pricing.invoke({
        "item_code": "01_002_0107_1_1",
        "price": 118.22,
        "location_type": "very_remote"
    })
    print(f"   Result: {result}")

    # Test 6: Check pricing with wrong price
    print("\n6. Testing check_nids_item_pricing - Wrong price:")
    result = check_nids_item_pricing.invoke({
        "item_code": "01_002_0107_1_1",
        "price": 50.00,
        "location_type": "standard"
    })
    print(f"   Result: {result}")

    # Test 7: Check old pricing for item only in active database
    print("\n7. Testing check_if_using_old_pricing - Item in active only:")
    result = check_if_using_old_pricing.invoke({"item_code": "01_002_0107_1_1"})
    print(f"   Result: {result}")

    # Test 8: Check old pricing for item in inactive database
    print("\n8. Testing check_if_using_old_pricing - Item in inactive database:")
    result = check_if_using_old_pricing.invoke({"item_code": "05_122409171_0105_1_2"})
    print(f"   Result: {result}")

    # Test 9: Check quotable item
    print("\n9. Testing check_nids_item_pricing - Quotable item (no fixed price):")
    result = check_nids_item_pricing.invoke({
        "item_code": "01_003_0107_1_1",
        "price": 100.00,
        "location_type": "standard"
    })
    print(f"   Result: {result}")

    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_tools()

