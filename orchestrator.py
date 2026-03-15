from typing import List
import logging
import time
from models import Task
from base_agent import BaseAgent


class Orchestrator:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.logger = logging.getLogger('Orchestrator')

    def execute(self, task: Task) -> Task:
        self.logger.info(f'Starting orchestration for task {task.id}')
        pipeline_start = time.time()

        # Initialize timing storage
        task.metadata['agent_timings'] = {}

        for agent in self.agents:
            self.logger.info(f'Passing task to {agent.name}')
            agent_start = time.time()

            task = agent.execute(task)

            agent_duration = round(time.time() - agent_start, 2)
            task.metadata['agent_timings'][agent.name] = agent_duration
            self.logger.info(f'{agent.name} completed in {agent_duration}s')

        total_duration = round(time.time() - pipeline_start, 2)
        task.metadata['total_duration_seconds'] = total_duration
        self.logger.info(f'Task {task.id} orchestration complete in {total_duration}s')
        return task

    def execute_batch(self, tasks: List[Task]) -> List[Task]:
        results = []
        for task in tasks:
            result = self.execute(task)
            results.append(result)
        return results
