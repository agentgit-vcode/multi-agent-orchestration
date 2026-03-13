from base_agent import BaseAgent
from models import Task, AgentType
from llm_handler import get_llm_handler, is_llm_available
from agent_instructions_manager import get_instructions_manager
import logging


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__('ResearcherAgent', AgentType.RESEARCHER)
        self.use_llm = is_llm_available()
        self.instructions_manager = get_instructions_manager()

        if self.use_llm:
            self.llm = get_llm_handler()
            self.logger.info("ResearcherAgent using OpenAI LLM with custom instructions")
        else:
            self.logger.info("ResearcherAgent using mock responses (LLM not available)")

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')

        # Research based on the plan
        if self.use_llm:
            try:
                # Get agent-specific instructions as system prompt
                system_prompt = self.instructions_manager.get_researcher_instructions()

                # User prompt contains scenario and context from previous phase
                user_prompt = f"""Research the following scenario thoroughly:

SCENARIO:
{task.initial_query}

PLANNING OUTPUT (from previous phase):
{task.plan}

Conduct comprehensive research following the instructions."""

                task.research_data = self.llm.call(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    max_tokens=2000
                )
                self.logger.info("Research data generated using OpenAI with custom instructions")
            except Exception as e:
                self.logger.error(f"Error calling LLM: {e}")
                task.research_data = f'Research findings for: {task.initial_query}\n\nSource 1: Information about the topic\nSource 2: Key facts and details\nSource 3: Supporting evidence'
        else:
            task.research_data = f'Research findings for: {task.initial_query}\n\nSource 1: Information about the topic\nSource 2: Key facts and details\nSource 3: Supporting evidence'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
