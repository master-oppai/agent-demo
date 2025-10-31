from langchain.tools import tool
from .models import NIDSSource
import pandas as pd

nids_source = NIDSSource("data/nids_source_active.csv")
nids_inactive_source = NIDSSource("data/nids_source_inactive.csv")

@tool
def check_nids_item_exists(item_code: str) -> str:
    """Check if the given item code exists in the NIDS database."""
    if nids_source.validate_item(item_code):
        return f"Item code {item_code} is valid according to NIDS."
    else:
        return f"Item code {item_code} is NOT found in the NIDS database and may be fraudulent."

@tool
def check_nids_item_pricing(item_code: str, price: float, location_type: str = "standard") -> str:
    """
    Check if the given item code has a valid pricing in the NIDS database.

    Args:
        item_code: The NIDS item code to validate
        price: The price to validate (per hour or per unit)
        location_type: Type of location - "standard" (uses state pricing), "remote", or "very_remote"

    Returns:
        String describing if the pricing matches, and if old pricing is being used
    """
    # Check if item exists in active source
    if not nids_source.validate_item(item_code):
        return f"Item code {item_code} not found in active NIDS database. Cannot validate pricing."

    # Get the item row from active source
    item_row = nids_source.df[nids_source.df['Support Item Number'] == item_code].iloc[0]

    # Determine which price column to check
    if location_type.lower() == "remote":
        price_column = "Remote"
    elif location_type.lower() == "very_remote":
        price_column = "Very Remote"
    else:
        # For standard, we'll check any state column (they're typically the same)
        # Using ACT as default state column
        price_column = "ACT"

    # Get the expected price
    expected_price_str = str(item_row[price_column]).strip()

    # Handle empty or NA prices (quotable items)
    if expected_price_str == '' or expected_price_str == 'nan' or pd.isna(item_row[price_column]):
        return f"Item code {item_code} is a quotable item (no fixed price). Cannot validate specific pricing."

    # Clean the price string (remove commas and spaces)
    expected_price_str = expected_price_str.replace(',', '').replace(' ', '')
    try:
        expected_price = float(expected_price_str)
    except ValueError:
        return f"Unable to parse expected price for item {item_code}."

    # Compare prices (allow small floating point differences)
    price_matches = abs(price - expected_price) < 0.01

    # Check if this item exists in inactive source (old pricing)
    using_old_pricing = nids_inactive_source.validate_item(item_code)

    result_parts = []

    if price_matches:
        result_parts.append(f"✓ Price ${price:.2f} MATCHES the NIDS price ${expected_price:.2f} for item {item_code} ({location_type} location).")
    else:
        result_parts.append(f"✗ Price ${price:.2f} DOES NOT MATCH the NIDS price ${expected_price:.2f} for item {item_code} ({location_type} location). Discrepancy: ${abs(price - expected_price):.2f}")

    if using_old_pricing:
        result_parts.append(f"⚠️ WARNING: Item {item_code} also exists in the INACTIVE pricing database, indicating OLD/OUTDATED pricing may be in use.")
    else:
        result_parts.append(f"✓ Item {item_code} is using current pricing (not found in inactive database).")

    return " ".join(result_parts)

@tool
def check_if_using_old_pricing(item_code: str) -> str:
    """
    Check if an item code exists in the inactive (old) NIDS pricing database.

    Args:
        item_code: The NIDS item code to check

    Returns:
        String indicating if the item is using old pricing
    """
    is_in_inactive = nids_inactive_source.validate_item(item_code)
    is_in_active = nids_source.validate_item(item_code)

    if is_in_inactive and is_in_active:
        return f"⚠️ WARNING: Item {item_code} exists in BOTH active and inactive databases. This item has updated pricing and old pricing should NOT be used."
    elif is_in_inactive and not is_in_active:
        return f"⚠️ CRITICAL: Item {item_code} ONLY exists in the inactive database. This item is using OUTDATED pricing and is no longer valid."
    elif is_in_active and not is_in_inactive:
        return f"✓ Item {item_code} is using current pricing (only in active database)."
    else:
        return f"✗ Item {item_code} not found in either active or inactive NIDS databases."
