from base_agent import BaseAgent
from models import Task, AgentType
import logging


class PublisherAgent(BaseAgent):
    def __init__(self):
        super().__init__('PublisherAgent', AgentType.PUBLISHER)

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')
        
        # Publish final output
        task.final_output = f'''FINAL REPORT: {task.initial_query}

--- PLAN ---
{task.plan}

--- RESEARCH ---
{task.research_data}

--- ANALYSIS ---
{task.analysis}'''

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
