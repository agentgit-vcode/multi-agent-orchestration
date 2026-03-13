from dataclasses import dataclass, field
from typing import Any, Dict, List
from enum import Enum
from datetime import datetime


class AgentType(Enum):
    PLANNER = 'planner'
    RESEARCHER = 'researcher'
    ANALYZER = 'analyzer'
    PUBLISHER = 'publisher'


@dataclass
class Task:
    id: str
    initial_query: str
    created_at: datetime = field(default_factory=datetime.now)
    plan: str = ''
    research_data: str = ''
    analysis: str = ''
    final_output: str = ''
    completed_agents: List[AgentType] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_agent_complete(self, agent_type: AgentType):
        if agent_type not in self.completed_agents:
            self.completed_agents.append(agent_type)

    def is_complete(self) -> bool:
        required_agents = [AgentType.PLANNER, AgentType.RESEARCHER, AgentType.ANALYZER, AgentType.PUBLISHER]
        return all(agent in self.completed_agents for agent in required_agents)
