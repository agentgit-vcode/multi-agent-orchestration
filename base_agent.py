from abc import ABC, abstractmethod
from models import Task, AgentType
from typing import Optional
import logging


class BaseAgent(ABC):
    def __init__(self, name: str, agent_type: AgentType):
        self.name = name
        self.agent_type = agent_type
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def execute(self, task: Task) -> Task:
        ''''''n        Process the task and return the updated task.
        ''''''
        pass

    def _log_execution(self, task: Task, status: str):
        self.logger.info(f'{self.name} - {status}: Task {task.id}')
