from langchain.tools import tool
from .models import NIDSSource

nids_source = NIDSSource("nids_source.csv")

@tool
def check_nids_item(item_code: str) -> str:
    """Check if the given item code exists in the NIDS database."""
    if nids_source.validate_item(item_code):
        return f"Item code {item_code} is valid according to NIDS."
    else:
        return f"Item code {item_code} is NOT found in the NIDS database and may be fraudulent."