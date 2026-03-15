import logging
from models import Task
from planner_agent import PlannerAgent
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent
from publisher_agent import PublisherAgent
from orchestrator import Orchestrator
import uuid


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    # Initialize agents in order
    agents = [
        PlannerAgent(),
        ResearcherAgent(),
        AnalyzerAgent(),
        PublisherAgent()
    ]

    # Create orchestrator
    orchestrator = Orchestrator(agents)

    # Create a task
    task = Task(
        id=str(uuid.uuid4()),
        initial_query='How can Python be used for AI applications?'
    )

    print(f'Starting task: {task.id}')
    print(f'Query: {task.initial_query}')

    # Execute orchestration
    completed_task = orchestrator.execute(task)

    # Display results
    print('='*80)
    print(completed_task.final_output)
    print('='*80)
    print(f'Task completed: {completed_task.is_complete()}')


if __name__ == '__main__':
    main()
