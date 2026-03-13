from base_agent import BaseAgent
from models import Task, AgentType
from llm_handler import get_llm_handler, is_llm_available
from agent_instructions_manager import get_instructions_manager
import logging


class PublisherAgent(BaseAgent):
    def __init__(self):
        super().__init__('PublisherAgent', AgentType.PUBLISHER)
        self.use_llm = is_llm_available()
        self.instructions_manager = get_instructions_manager()

        if self.use_llm:
            self.llm = get_llm_handler()
            self.logger.info("PublisherAgent using OpenAI LLM with custom instructions")
        else:
            self.logger.info("PublisherAgent using mock responses (LLM not available)")

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')

        # Publish final output
        if self.use_llm:
            try:
                # Get agent-specific instructions as system prompt
                system_prompt = self.instructions_manager.get_publisher_instructions()

                # User prompt contains all analysis from previous phases
                user_prompt = f"""Create a final professional memo based on the complete analysis:

ORIGINAL SCENARIO:
{task.initial_query}

PLANNING PHASE OUTPUT:
{task.plan}

RESEARCH PHASE OUTPUT:
{task.research_data}

ANALYSIS PHASE OUTPUT:
{task.analysis}

Create a professional memo synthesizing all this information following the instructions."""

                task.final_output = self.llm.call(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    max_tokens=2500
                )
                self.logger.info("Final report generated using OpenAI with custom instructions")
            except Exception as e:
                self.logger.error(f"Error calling LLM: {e}")
                task.final_output = f'FINAL REPORT: {task.initial_query}\n\n--- PLAN ---\n{task.plan}\n\n--- RESEARCH ---\n{task.research_data}\n\n--- ANALYSIS ---\n{task.analysis}'
        else:
            task.final_output = f'FINAL REPORT: {task.initial_query}\n\n--- PLAN ---\n{task.plan}\n\n--- RESEARCH ---\n{task.research_data}\n\n--- ANALYSIS ---\n{task.analysis}'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
