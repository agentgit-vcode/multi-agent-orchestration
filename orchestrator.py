from typing import List
import logging
from models import Task
from base_agent import BaseAgent


class Orchestrator:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.logger = logging.getLogger('Orchestrator')

    def execute(self, task: Task) -> Task:
        self.logger.info(f'Starting orchestration for task {task.id}')
        
        for agent in self.agents:
            self.logger.info(f'Passing task to {agent.name}')
            task = agent.execute(task)
            self.logger.info(f'{agent.name} completed')
        
        self.logger.info(f'Task {task.id} orchestration complete')
        return task

    def execute_batch(self, tasks: List[Task]) -> List[Task]:
        results = []
        for task in tasks:
            result = self.execute(task)
            results.append(result)
        return results
