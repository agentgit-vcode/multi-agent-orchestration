from base_agent import BaseAgent
from models import Task, AgentType
import logging


class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__('AnalyzerAgent', AgentType.ANALYZER)

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')
        
        # Analyze the research data
        task.analysis = f'Analysis of research data for: {task.initial_query}

Key Finding 1: Important insight from research
Key Finding 2: Significant pattern identified
Key Finding 3: Actionable conclusion'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
