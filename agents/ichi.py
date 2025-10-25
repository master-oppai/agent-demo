import os

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from agents.models import ProcessResponse, BaseAgent

system_prompt = """
You're an expert at fraud detection for NIDS invoices. Given the content of an invoice, determine if it is potentially fraudulent. If the invoice appears legitimate, respond with is_valid set to true and provide a brief reason. If the invoice seems suspicious or fraudulent, respond with is_valid set to false and provide a detailed reason explaining the indicators of fraud.
"""

class IchiAgent(BaseAgent):
    def __init__(self, model: str):
        self.model = model

    def process(self, data: str) -> ProcessResponse:
        api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(model=self.model, api_key=api_key)
        agent = create_agent(
            llm,
            response_format=ToolStrategy(ProcessResponse),
            system_prompt=system_prompt,
        )

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Analyze the following invoice content parsed from the invoice pdf for fraud detection:\n\n{data}",
                    }
                ]
            }
        )

        return result["structured_response"]
