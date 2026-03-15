from base_agent import BaseAgent
from models import Task, AgentType
from llm_handler import get_llm_handler, is_llm_available
from agent_instructions_manager import get_instructions_manager
import logging


class AnalyzerAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__('AnalyzerAgent', AgentType.ANALYZER)
        self.use_llm = is_llm_available()
        self.instructions_manager = get_instructions_manager()

        if llm:
            self.llm = llm
            self.use_llm = True
            self.logger.info("AnalyzerAgent using provided LLM handler")
        elif self.use_llm:
            self.llm = get_llm_handler()
            self.logger.info("AnalyzerAgent using OpenAI LLM with custom instructions")
        else:
            self.logger.info("AnalyzerAgent using mock responses (LLM not available)")

    def execute(self, task: Task) -> Task:
        self._log_execution(task, 'START')

        # Analyze the research data
        if self.use_llm:
            try:
                # Get agent-specific instructions as system prompt
                system_prompt = self.instructions_manager.get_analyzer_instructions()

                # User prompt contains all context from previous phases
                user_prompt = f"""Analyze the following information from our decision process:

SCENARIO:
{task.initial_query}

PLANNING PHASE OUTPUT:
{task.plan}

RESEARCH PHASE OUTPUT:
{task.research_data}

Provide thorough analysis following the instructions."""

                result = self.llm.call(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    max_tokens=1800,
                    agent_name=self.name
                )
                task.analysis = result['text']

                # Store metrics
                if 'agent_metrics' not in task.metadata:
                    task.metadata['agent_metrics'] = []
                task.metadata['agent_metrics'].append(result['metrics'].to_dict())

                self.logger.info("Analysis generated using LLM with custom instructions")
            except Exception as e:
                self.logger.error(f"Error calling LLM: {e}")
                task.analysis = f'Analysis of research data for: {task.initial_query}\n\nKey Finding 1: Important insight from research\nKey Finding 2: Significant pattern identified\nKey Finding 3: Actionable conclusion'
        else:
            task.analysis = f'Analysis of research data for: {task.initial_query}\n\nKey Finding 1: Important insight from research\nKey Finding 2: Significant pattern identified\nKey Finding 3: Actionable conclusion'

        task.mark_agent_complete(self.agent_type)
        self._log_execution(task, 'COMPLETE')
        return task
