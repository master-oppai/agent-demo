import os

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI

from agents.models import BaseAgent, ProcessResponse
from agents.tools import check_nids_item_exists, check_nids_item_pricing, check_if_using_old_pricing

system_prompt = """
You are an expert NDIS (National Disability Insurance Scheme) fraud detection agent.

Your role is to analyze invoice text line-by-line, focusing on each item in the invoice, and verify its legitimacy using the official NIDS source data.

For each invoice, perform the following checks:
1. **Item Code Validation**: Identify all line items, including their *item names* and *line item codes* (e.g., 01_020_0120_1_1).
   - Use the check_nids_item_exists tool to verify each code exists in the active NIDS database.
   
2. **Pricing Validation**: For each line item with a price, verify the pricing is correct.
   - Extract the price per unit/hour from the invoice
   - Determine the location type: "standard" (default), "remote", or "very_remote" based on invoice context
   - Use the check_nids_item_pricing tool to validate the price matches NIDS pricing
   
3. **Old Pricing Detection**: Check if the invoice is using outdated pricing.
   - Use the check_if_using_old_pricing tool to verify items are not using inactive/outdated pricing
   
4. **Final Assessment**: Based on all checks, determine if the invoice is valid.
   - If all items exist, prices match, and pricing is current → mark as valid
   - If any item code is missing, invalid, prices don't match, or old pricing is used → mark as fraudulent

Return your final answer as a structured JSON:
{
  "is_valid": true or false,
  "reason": "A detailed explanation referencing specific item codes, pricing discrepancies, and old pricing issues found.",
  "is_using_old_pricing": true or false (set to true if any item uses old/inactive pricing)
}

Be thorough in your analysis. Check ALL items before making a final determination.
"""

class StandardAgent(BaseAgent):
    def __init__(self, model: str):
        self.model = model
        self.llm = ChatOpenAI(model=self.model, api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = [check_nids_item_exists, check_nids_item_pricing, check_if_using_old_pricing]

        self.agent = create_agent(
            self.llm,
            tools=self.tools,
            response_format=ToolStrategy(ProcessResponse),
            system_prompt=system_prompt
        )

    def process(self, invoice_text: str) -> ProcessResponse:
        """Process the invoice by validating each line item, its pricing, and checking for old pricing."""
        result = self.agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Analyze this invoice thoroughly. For each item:
                    1. Check if the item code exists in NIDS using check_nids_item_exists
                    2. Validate the pricing using check_nids_item_pricing (specify location_type if remote/very_remote)
                    3. Check if old pricing is being used with check_if_using_old_pricing
                    
                    Invoice content:
                    {invoice_text}
                    """,
                }
            ]
        })
        return result["structured_response"]