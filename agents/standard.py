import os

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from agents.models import BaseAgent, ProcessResponse
from agents.tools import check_nids_item

system_prompt = """
You are an expert NDIS (National Disability Insurance Scheme) fraud detection agent.

Your role is to analyze invoice text line-by-line, focusing on each item in the invoice, and verify its legitimacy using the official NIDS source data (loaded from nids_source.csv).

For each invoice:
1. Identify all line items, including their *item names* and *line item codes* (e.g., 01_020_0120_1_1).
2. Cross-check each line item code with the NIDS source data.
3. Determine if every code exists and matches the expected NDIS support item format.
4. If all items are valid and match the source list, mark the invoice as valid.
5. If any item code is missing, invalid, or suspicious, mark the invoice as fraudulent and explain why.

Return your final answer as a structured JSON using the schema below:

{
  "is_valid": true or false,
  "reason": "A concise but clear explanation why this invoice is or is not valid, referencing specific item codes and findings."
}

Focus only on factual verification based on the item codes and descriptions.
Do not assume; if an item code is not in the NIDS source, consider it suspicious.
"""

class StandardAgent(BaseAgent):
    def __init__(self, model: str):
        self.model = model
        self.llm = ChatOpenAI(model=self.model, api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = [check_nids_item]

        self.agent = create_agent(
            self.llm,
            tools=self.tools,
            response_format=ToolStrategy(ProcessResponse),
            system_prompt=system_prompt
        )

    def process(self, invoice_text: str) -> ProcessResponse:
        """Process the invoice by validating each line item."""
        result = self.agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Analyze this invoice line by line. For each item,
                    check its code or ASBN against the NIDS source using the tool.
                    Invoice content:
                    {invoice_text}
                    """,
                }
            ]
        })
        return result["structured_response"]