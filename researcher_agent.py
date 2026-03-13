from base_agent import BaseAgent
from models import Task, AgentType
import logging


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__('ResearcherAgent', AgentType.RESEARCHER)

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')
        
        # Research based on the plan
        task.research_data = f'Research findings for: {task.initial_query}

Source 1: Information about the topic
Source 2: Key facts and details
Source 3: Supporting evidence'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
