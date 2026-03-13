from base_agent import BaseAgent
from models import Task, AgentType
import logging


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__('PlannerAgent', AgentType.PLANNER)

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')
        
        # Create a plan based on the initial query
        task.plan = f'Plan for: {task.initial_query}

Step 1: Break down the query
Step 2: Identify key information needed
Step 3: Create structured approach'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
