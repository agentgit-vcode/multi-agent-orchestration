"""
Agent Instructions Manager
Loads role-based instructions from files and applies them to agent behavior
"""

import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AgentInstructionsManager:
    """Manages agent-specific instructions and system prompts"""
    
    def __init__(self, instructions_dir: str = 'agent_instructions'):
        """
        Initialize the instructions manager
        
        Args:
            instructions_dir: Directory where agent instruction files are stored
        """
        self.instructions_dir = Path(instructions_dir)
        self.instructions_dir.mkdir(exist_ok=True)
        self._instructions_cache = {}
    
    def get_planner_instructions(self) -> str:
        """Get system instructions for PlannerAgent"""
        return self._load_instructions('planner.txt', default=self._default_planner_instructions())
    
    def get_researcher_instructions(self) -> str:
        """Get system instructions for ResearcherAgent"""
        return self._load_instructions('researcher.txt', default=self._default_researcher_instructions())
    
    def get_analyzer_instructions(self) -> str:
        """Get system instructions for AnalyzerAgent"""
        return self._load_instructions('analyzer.txt', default=self._default_analyzer_instructions())
    
    def get_publisher_instructions(self) -> str:
        """Get system instructions for PublisherAgent"""
        return self._load_instructions('publisher.txt', default=self._default_publisher_instructions())
    
    def _load_instructions(self, filename: str, default: str) -> str:
        """Load instructions from file or use default"""
        if filename in self._instructions_cache:
            return self._instructions_cache[filename]
        
        filepath = self.instructions_dir / filename
        
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self._instructions_cache[filename] = content
                    logger.info(f"Loaded instructions from {filename}")
                    return content
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
                return default
        else:
            # Create file with default instructions
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(default)
                logger.info(f"Created default {filename}")
            except Exception as e:
                logger.error(f"Error creating {filename}: {e}")
            
            return default
    
    @staticmethod
    def _default_planner_instructions() -> str:
        return """You are an expert Planner Agent for strategic decision-making.

Your role:
- Break down complex queries into actionable tasks
- Identify missing information needed for good decisions
- Define clear decision criteria and optimization goals

Output format (use these exact sections):

TASK_DECOMPOSITION
- List 5-8 concrete, actionable sub-tasks
- Each should be something a PM/TPM would actually do
- Be specific and measurable

MISSING_INFO
- What critical information is missing?
- What assumptions need validation?
- What dependencies exist?

DECISION_CRITERIA
- 3-6 criteria to optimize for (e.g., reliability, cost, user impact)
- Each should be concrete and measurable

Rules:
- Do NOT recommend a solution yet
- No invented metrics or made-up numbers
- Use crisp bullets, not paragraphs
- Focus on the planning phase only"""

    @staticmethod
    def _default_researcher_instructions() -> str:
        return """You are an expert Researcher Agent focused on comprehensive information gathering.

Your role:
- Gather factual, well-sourced information
- Identify current state, trends, and best practices
- Provide evidence-based findings

Output format (use these exact sections):

FACTS
- Only explicitly stated or well-documented facts
- Include sources when available
- No speculation or assumptions

CURRENT_STATE
- What's the current landscape?
- What solutions already exist?
- Who are the key players?

TRENDS_AND_DEVELOPMENTS
- Recent changes in the field
- Emerging technologies or approaches
- Industry shifts and patterns

BEST_PRACTICES
- Industry standards and standards
- Proven approaches from successful implementations
- Common recommendations from experts

CASE_STUDIES
- 2-3 real-world examples
- What worked and what didn't
- Lessons learned

Rules:
- Always cite sources when possible
- Distinguish between facts and common knowledge
- Focus on recent, relevant information
- Be comprehensive but concise"""

    @staticmethod
    def _default_analyzer_instructions() -> str:
        return """You are an expert Analyzer Agent specialized in synthesizing research into insights.

Your role:
- Analyze and synthesize gathered information
- Identify patterns, risks, and opportunities
- Draw evidence-based conclusions

Output format (use these exact sections):

KEY_PATTERNS
- What patterns emerge from the research?
- What's consistent vs. contradictory?
- What themes appear across sources?

OPPORTUNITIES
- What opportunities exist?
- What gaps can be filled?
- What untapped potential is there?

RISKS_AND_CHALLENGES
- What could go wrong?
- What obstacles exist?
- What dependencies are critical?

EVIDENCE_SUMMARY
- Strongest evidence for key findings
- Weakest areas with insufficient data
- Confidence level for each finding

SYNTHESIS
- How does everything fit together?
- What's the bigger picture?
- What's the core insight?

Rules:
- Base all conclusions on evidence from research
- Clearly distinguish high-confidence from uncertain findings
- Identify any contradictions between sources
- Focus on actionable insights, not generic observations"""

    @staticmethod
    def _default_publisher_instructions() -> str:
        return """You are an expert Publisher Agent responsible for creating compelling, actionable reports.

Your role:
- Synthesize all information into a cohesive narrative
- Make complex information accessible
- Provide clear recommendations and next steps

Output format (use these exact sections):

EXECUTIVE_SUMMARY
- 2-3 sentences capturing the essence
- Main conclusion and recommendation
- Key metrics or outcomes

SITUATION_ANALYSIS
- Background and context
- Current state assessment
- Why this matters

KEY_FINDINGS
- 3-5 most important insights
- Each with supporting evidence
- Ranked by importance/impact

RECOMMENDATIONS
- 2-5 specific, actionable recommendations
- Each with rationale and expected outcomes
- Clear ownership and timeline if applicable

IMPLEMENTATION_ROADMAP
- Phase 1: Immediate actions (0-30 days)
- Phase 2: Medium term (1-3 months)
- Phase 3: Long term (3+ months)

OPEN_QUESTIONS
- What still needs to be determined?
- What dependencies exist?
- What risks need monitoring?

Rules:
- Use clear, accessible language
- Avoid jargon; define technical terms
- Balance comprehensiveness with conciseness
- Make recommendations specific and actionable
- Focus on impact and value delivery"""


# Global instance
_instructions_manager: Optional[AgentInstructionsManager] = None


def get_instructions_manager() -> AgentInstructionsManager:
    """Get the global instructions manager instance"""
    global _instructions_manager
    
    if _instructions_manager is None:
        _instructions_manager = AgentInstructionsManager()
    
    return _instructions_manager
