# python
from pydantic import BaseModel, ConfigDict
from agents.base_agent import BaseAgent

class NIDSAgent(BaseModel):
    name: str
    description: str
    agent: type[BaseAgent]

    model_config = ConfigDict(arbitrary_types_allowed=True)
