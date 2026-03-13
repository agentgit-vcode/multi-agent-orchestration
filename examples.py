import logging
from models import Task, AgentType
from base_agent import BaseAgent
from planner_agent import PlannerAgent
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent
from publisher_agent import PublisherAgent
from orchestrator import Orchestrator
import uuid


# Example 1: Basic usage
def example_basic():
    logging.basicConfig(level=logging.INFO)
    agents = [PlannerAgent(), ResearcherAgent(), AnalyzerAgent(), PublisherAgent()]
    orchestrator = Orchestrator(agents)
    task = Task(id=str(uuid.uuid4()), initial_query='What is Python?')
    completed_task = orchestrator.execute(task)
    print(completed_task.final_output)


# Example 2: Batch processing
def example_batch():
    logging.basicConfig(level=logging.INFO)
    agents = [PlannerAgent(), ResearcherAgent(), AnalyzerAgent(), PublisherAgent()]
    orchestrator = Orchestrator(agents)
    
    tasks = [
        Task(id=str(uuid.uuid4()), initial_query='What is AI?'),
        Task(id=str(uuid.uuid4()), initial_query='What is Machine Learning?'),
        Task(id=str(uuid.uuid4()), initial_query='What is Deep Learning?')
    ]
    
    results = orchestrator.execute_batch(tasks)
    for result in results:
        print(f'Task {result.id}: Complete={result.is_complete()}')


# Example 3: Custom agent
class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__('SummarizerAgent', AgentType.PUBLISHER)
    
    def execute(self, task: Task) -> Task:
        task.final_output = f'SUMMARY: {task.analysis[:100]}...'
        task.mark_agent_complete(self.agent_type)
        return task


def example_custom_agent():
    logging.basicConfig(level=logging.INFO)
    agents = [
        PlannerAgent(),
        ResearcherAgent(),
        AnalyzerAgent(),
        SummarizerAgent()
    ]
    orchestrator = Orchestrator(agents)
    task = Task(id=str(uuid.uuid4()), initial_query='Tell me about Python')
    completed_task = orchestrator.execute(task)
    print(completed_task.final_output)


if __name__ == '__main__':
    print('=== Example 1: Basic Usage ===')
    example_basic()
    print(
')
    
    print('=== Example 2: Batch Processing ===')
    example_batch()
    print(
')
    
    print('=== Example 3: Custom Agent ===')
    example_custom_agent()
