from base_agent import BaseAgent
from models import Task, AgentType
from llm_handler import get_llm_handler, is_llm_available
from agent_instructions_manager import get_instructions_manager
import logging


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__('PlannerAgent', AgentType.PLANNER)
        self.use_llm = is_llm_available()
        self.instructions_manager = get_instructions_manager()

        if self.use_llm:
            self.llm = get_llm_handler()
            self.logger.info("PlannerAgent using OpenAI LLM with custom instructions")
        else:
            self.logger.info("PlannerAgent using mock responses (LLM not available)")

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')

        # Create a plan based on the initial query
        if self.use_llm:
            try:
                # Get agent-specific instructions as system prompt
                system_prompt = self.instructions_manager.get_planner_instructions()

                # User prompt is ONLY the scenario
                user_prompt = f"Please create a plan for this scenario:\n\n{task.initial_query}"

                task.plan = self.llm.call(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    max_tokens=1500
                )
                self.logger.info("Plan generated using OpenAI with custom instructions")
            except Exception as e:
                self.logger.error(f"Error calling LLM: {e}")
                task.plan = f'Plan for: {task.initial_query}\n\nStep 1: Break down the query\nStep 2: Identify key information needed\nStep 3: Create structured approach'
        else:
            task.plan = f'Plan for: {task.initial_query}\n\nStep 1: Break down the query\nStep 2: Identify key information needed\nStep 3: Create structured approach'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
