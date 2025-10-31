#!/usr/bin/env python3
"""Test script for NDIS fraud detection agent with realistic invoice scenarios."""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import time
import traceback

# Add parent directory to path so we can import agents module
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from .env file
load_dotenv()

from agents.standard import StandardAgent


def log_with_timestamp(message, level="INFO"):
    """Log a message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def print_invoice_summary(content):
    """Extract and print a summary of invoice items for verification."""
    lines = content.strip().split('\n')
    for line in lines:
        if any(code_part in line for code_part in ['01_', '02_', '03_', '04_', '05_', '06_']):
            print(f"    📋 {line.strip()}")

# Realistic invoice test cases
INVOICE_TEST_CASES = [
    {
        "name": "LEGITIMATE_INVOICE_1",
        "expected_valid": True,
        "description": "Valid invoice with correct pricing for standard location",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-0847
Date: 28 October 2025
Provider: Caring Hands Support Services
ABN: 51 123 456 789

Participant Name: Sarah Mitchell
NDIS Number: 430123456

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
26/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities -           4.0     $70.23    $280.92
                                Standard - Weekday Daytime
27/10/2025  01_020_0120_1_1    House Cleaning And Other Household Activities    3.5     $58.03    $203.11

Total: $484.03
GST: $0.00 (GST Free)
Total Amount Due: $484.03
"""
    },
    {
        "name": "LEGITIMATE_INVOICE_2",
        "expected_valid": True,
        "description": "Valid invoice with remote location pricing",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-1293
Date: 29 October 2025
Provider: Outback Care Services Pty Ltd
ABN: 82 987 654 321

Participant Name: James Cooper
NDIS Number: 430987654

Service Location: Remote Area (Katherine, NT)

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
25/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities -           6.0     $98.32    $589.92
                                Standard - Weekday Daytime (Remote)
25/10/2025  01_019_0120_1_1    House or Yard Maintenance (Remote)               2.5     $79.77    $199.43

Total: $789.35
GST: $0.00 (GST Free)
Total Amount Due: $789.35
"""
    },
    {
        "name": "FRAUDULENT_INVALID_ITEM_CODE",
        "expected_valid": False,
        "description": "Fraudulent invoice with non-existent NIDS item code",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-0455
Date: 27 October 2025
Provider: QuickCash Support Services
ABN: 91 555 666 777

Participant Name: Michael Brown
NDIS Number: 430555888

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
24/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities             3.0     $70.23    $210.69
24/10/2025  99_999_9999_9_9    Premium Personal Care Package                    5.0     $150.00   $750.00
25/10/2025  01_020_0120_1_1    House Cleaning                                   2.0     $58.03    $116.06

Total: $1,076.75
GST: $0.00 (GST Free)
Total Amount Due: $1,076.75
"""
    },
    {
        "name": "FRAUDULENT_INCORRECT_PRICING",
        "expected_valid": False,
        "description": "Fraudulent invoice with inflated pricing",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-0892
Date: 28 October 2025
Provider: Premium Care Solutions
ABN: 73 444 555 666

Participant Name: Emma Watson
NDIS Number: 430777999

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
26/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities             5.0     $95.50    $477.50
                                Standard - Weekday Daytime
27/10/2025  01_020_0120_1_1    House Cleaning And Other Household Activities    4.0     $75.00    $300.00

Total: $777.50
GST: $0.00 (GST Free)
Total Amount Due: $777.50

Note: Prices include service quality premium
"""
    },
    {
        "name": "FRAUDULENT_MIXED_INVALID_PRICING",
        "expected_valid": False,
        "description": "Mixed fraud - some correct items, some with wrong pricing",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-1047
Date: 29 October 2025
Provider: Budget Support Services
ABN: 64 222 333 444

Participant Name: Oliver Chen
NDIS Number: 430666111

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
27/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities             3.0     $70.23    $210.69
                                Standard - Weekday Daytime
27/10/2025  01_019_0120_1_1    House or Yard Maintenance                        2.0     $45.00    $90.00
28/10/2025  01_004_0107_1_1    Assistance with Personal Domestic Activities     4.0     $50.50    $202.00

Total: $502.69
GST: $0.00 (GST Free)
Total Amount Due: $502.69
"""
    },
    {
        "name": "LEGITIMATE_INVOICE_WEEKEND",
        "expected_valid": True,
        "description": "Valid invoice with weekend rates",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-1156
Date: 28 October 2025
Provider: Weekend Care Support
ABN: 55 111 222 333

Participant Name: Sophie Turner
NDIS Number: 430888222

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
26/10/2025  01_013_0107_1_1    Assistance With Self-Care Activities -           6.0     $98.83    $592.98
                                Standard - Saturday
27/10/2025  01_014_0107_1_1    Assistance With Self-Care Activities -           5.0     $127.43   $637.15
                                Standard - Sunday

Total: $1,230.13
GST: $0.00 (GST Free)
Total Amount Due: $1,230.13
"""
    },
    {
        "name": "FRAUDULENT_OUTDATED_PRICING",
        "expected_valid": False,
        "description": "Invoice using old/outdated pricing from inactive database",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-0734
Date: 29 October 2025
Provider: Legacy Care Services
ABN: 47 888 999 000

Participant Name: Daniel Kim
NDIS Number: 430333444

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
27/10/2025  05_122409171_0105_1_2  MWC - Accessory - Power-Assist Drive        1       $2,500.00 $2,500.00
                                    Technology
28/10/2025  01_011_0107_1_1        Assistance With Self-Care Activities         3.0     $70.23    $210.69

Total: $2,710.69
GST: $0.00 (GST Free)
Total Amount Due: $2,710.69
"""
    },
    {
        "name": "LEGITIMATE_INVOICE_MULTIPLE_SERVICES",
        "expected_valid": True,
        "description": "Valid invoice with multiple different service types",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-1389
Date: 30 October 2025
Provider: Complete Care Solutions Pty Ltd
ABN: 39 777 888 999

Participant Name: Isabella Martinez
NDIS Number: 430999888

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
28/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities -           3.0     $70.23    $210.69
                                Standard - Weekday Daytime
28/10/2025  01_004_0107_1_1    Assistance with Personal Domestic Activities     2.5     $59.06    $147.65
29/10/2025  01_020_0120_1_1    House Cleaning And Other Household Activities    3.0     $58.03    $174.09
29/10/2025  01_019_0120_1_1    House or Yard Maintenance                        1.5     $56.98    $85.47

Total: $617.90
GST: $0.00 (GST Free)
Total Amount Due: $617.90
"""
    },
    {
        "name": "FRAUDULENT_REMOTE_PRICING_MISMATCH",
        "expected_valid": False,
        "description": "Claims remote pricing but uses incorrect rates",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-0621
Date: 28 October 2025
Provider: Remote Region Care
ABN: 28 333 444 555

Participant Name: Lucas Anderson
NDIS Number: 430222333

Service Location: Remote Area (Broken Hill, NSW)

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
26/10/2025  01_011_0107_1_1    Assistance With Self-Care Activities -           4.0     $85.00    $340.00
                                Standard - Weekday Daytime (Remote)
27/10/2025  01_020_0120_1_1    House Cleaning (Remote)                          3.0     $70.00    $210.00

Total: $550.00
GST: $0.00 (GST Free)
Total Amount Due: $550.00
"""
    },
    {
        "name": "LEGITIMATE_INVOICE_EVENING_SHIFT",
        "expected_valid": True,
        "description": "Valid invoice with evening rates",
        "content": """
NDIS Service Provider Invoice
Invoice Number: INV-2025-1472
Date: 30 October 2025
Provider: Evening Support Services
ABN: 62 666 777 888

Participant Name: Ava Johnson
NDIS Number: 430444555

Service Details:
Date        Item Code           Description                                      Hours   Rate      Amount
28/10/2025  01_015_0107_1_1    Assistance With Self-Care Activities -           4.0     $77.38    $309.52
                                Standard - Weekday Evening
29/10/2025  01_002_0107_1_1    Assistance With Self-Care Activities -           5.0     $78.81    $394.05
                                Standard - Weekday Night

Total: $703.57
GST: $0.00 (GST Free)
Total Amount Due: $703.57
"""
    }
]


def run_agent_tests():
    """Run all invoice test cases through the StandardAgent."""
    start_time = time.time()

    print("\n" + "=" * 100)
    print(" " * 30 + "NDIS FRAUD DETECTION AGENT")
    print(" " * 28 + "COMPREHENSIVE TESTING SUITE")
    print("=" * 100)

    log_with_timestamp("Starting test suite initialization")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        log_with_timestamp("OPENAI_API_KEY not found", "ERROR")
        print("\n✗ ERROR: OPENAI_API_KEY environment variable is not set")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr create a .env file in the project root with:")
        print("  OPENAI_API_KEY=your-api-key-here")
        return False

    log_with_timestamp("✓ API key found", "SUCCESS")

    # Initialize the agent
    log_with_timestamp("Initializing StandardAgent with gpt-4o model...")
    try:
        agent = StandardAgent(model="gpt-4o")
        log_with_timestamp("✓ Agent initialized successfully", "SUCCESS")
    except Exception as e:
        log_with_timestamp(f"Failed to initialize agent: {e}", "ERROR")
        print(f"\n✗ ERROR: Could not initialize agent: {e}")
        return False

    # Track results
    total_tests = len(INVOICE_TEST_CASES)
    passed = 0
    failed = 0
    results = []

    log_with_timestamp(f"Running {total_tests} test cases...\n")

    # Run each test case
    for i, test_case in enumerate(INVOICE_TEST_CASES, 1):
        test_start_time = time.time()

        print("\n" + "=" * 100)
        print(f"TEST {i}/{total_tests}: {test_case['name']}")
        print("=" * 100)
        log_with_timestamp(f"Starting test: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        print(f"🎯 Expected Result: {'✓ VALID' if test_case['expected_valid'] else '✗ FRAUDULENT'}")
        print("-" * 100)
        print("Invoice Items:")
        print_invoice_summary(test_case['content'])
        print("-" * 100)

        try:
            log_with_timestamp("Sending invoice to agent for analysis...")

            # Process the invoice through the agent
            result = agent.process(test_case['content'])

            test_duration = time.time() - test_start_time
            log_with_timestamp(f"Agent analysis completed in {test_duration:.2f}s")

            # Check if result matches expectation
            test_passed = result.is_valid == test_case['expected_valid']

            if test_passed:
                passed += 1
                status = "✓ PASSED"
                status_level = "SUCCESS"
            else:
                failed += 1
                status = "✗ FAILED"
                status_level = "FAIL"

            # Display results
            print(f"\n{'🤖 AGENT ANALYSIS RESULTS':^100}")
            print("-" * 100)
            print(f"  ├─ Is Valid: {'✓ YES' if result.is_valid else '✗ NO'}")
            print(f"  ├─ Using Old Pricing: {'⚠️ YES' if result.is_using_old_pricing else '✓ NO'}")
            print(f"  ├─ Analysis Time: {test_duration:.2f}s")
            print(f"  └─ Reason: {result.reason}")
            print("-" * 100)

            if test_passed:
                print(f"\n{'✓ TEST RESULT: PASSED':^100}")
                print(f"{'(Agent correctly identified the invoice)':^100}")
            else:
                print(f"\n{'✗ TEST RESULT: FAILED':^100}")
                print(f"{'Expected: ' + ('VALID' if test_case['expected_valid'] else 'FRAUDULENT'):^100}")
                print(f"{'Got: ' + ('VALID' if result.is_valid else 'FRAUDULENT'):^100}")

            log_with_timestamp(f"Test {i} {status}", status_level)

            results.append({
                "test_name": test_case['name'],
                "passed": test_passed,
                "expected_valid": test_case['expected_valid'],
                "actual_valid": result.is_valid,
                "reason": result.reason,
                "duration": test_duration,
                "using_old_pricing": result.is_using_old_pricing
            })

        except Exception as e:
            failed += 1
            status = "✗ ERROR"
            test_duration = time.time() - test_start_time

            print(f"\n{'⚠️ EXCEPTION OCCURRED':^100}")
            print("-" * 100)
            print(f"Error: {str(e)}")
            print("\nStack trace:")
            traceback.print_exc()
            print("-" * 100)

            log_with_timestamp(f"Test {i} ERROR: {str(e)}", "ERROR")

            results.append({
                "test_name": test_case['name'],
                "passed": False,
                "error": str(e),
                "duration": test_duration
            })

        print("=" * 100)

    # Calculate total duration
    total_duration = time.time() - start_time

    # Print summary
    print("\n\n" + "=" * 100)
    print(f"{'TEST SUMMARY':^100}")
    print("=" * 100)
    log_with_timestamp("Test suite completed")
    print(f"\n  Total Tests Run: {total_tests}")
    print(f"  ✓ Passed: {passed} ({passed/total_tests*100:.1f}%)")
    print(f"  ✗ Failed: {failed} ({failed/total_tests*100:.1f}%)")
    print(f"  ⏱️  Total Duration: {total_duration:.2f}s")
    print(f"  ⌀ Average per Test: {total_duration/total_tests:.2f}s")
    print("=" * 100)

    # Detailed results table
    print("\n" + "=" * 100)
    print(f"{'DETAILED RESULTS':^100}")
    print("=" * 100)
    print(f"{'Test Name':<40} {'Expected':<15} {'Actual':<15} {'Result':<10} {'Time':<10}")
    print("-" * 100)

    for result in results:
        status_icon = "✓ PASS" if result['passed'] else "✗ FAIL"
        if 'error' not in result:
            expected = "VALID" if result['expected_valid'] else "FRAUDULENT"
            actual = "VALID" if result['actual_valid'] else "FRAUDULENT"
            duration_str = f"{result['duration']:.2f}s"
            print(f"{result['test_name']:<40} {expected:<15} {actual:<15} {status_icon:<10} {duration_str:<10}")
        else:
            duration_str = f"{result['duration']:.2f}s"
            print(f"{result['test_name']:<40} {'N/A':<15} {'ERROR':<15} {status_icon:<10} {duration_str:<10}")

    print("=" * 100)

    # Show failures in detail
    if failed > 0:
        print("\n" + "=" * 100)
        print(f"{'FAILED TESTS DETAILS':^100}")
        print("=" * 100)
        for result in results:
            if not result['passed']:
                print(f"\n❌ {result['test_name']}")
                if 'error' in result:
                    print(f"   Error: {result['error']}")
                else:
                    print(f"   Expected: {'VALID' if result['expected_valid'] else 'FRAUDULENT'}")
                    print(f"   Got: {'VALID' if result['actual_valid'] else 'FRAUDULENT'}")
                    print(f"   Agent Reason: {result['reason']}")
        print("=" * 100)

    print("\n" + "=" * 100)
    if passed == total_tests:
        print(f"{'🎉 ALL TESTS PASSED! 🎉':^100}")
    else:
        print(f"{'⚠️ SOME TESTS FAILED - REVIEW REQUIRED':^100}")
    print("=" * 100 + "\n")

    log_with_timestamp(f"Test suite finished: {passed}/{total_tests} passed",
                      "SUCCESS" if passed == total_tests else "WARNING")

    return passed == total_tests


if __name__ == "__main__":
    success = run_agent_tests()
    sys.exit(0 if success else 1)

