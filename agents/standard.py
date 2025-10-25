import os

from langchain_openai import ChatOpenAI

from agents.base_agent import BaseAgent, ProcessResponse


class StandardAgent(BaseAgent):
    def __init__(self, model: str):
        self.model = model
        self.llm = ChatOpenAI(model=self.model, api_key=os.getenv("OPENAI_API_KEY"))

    def process(self, data: str) -> ProcessResponse:
        pass
