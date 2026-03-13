# Multi-Agent Orchestration Framework

## Overview

This is a Python-based multi-agent orchestration system where tasks flow through a pipeline of specialized agents:

1. **Planner Agent** - Creates a structured plan based on the initial query
2. **Researcher Agent** - Gathers research data based on the plan
3. **Analyzer Agent** - Analyzes the research data and draws conclusions
4. **Publisher Agent** - Compiles everything into a final publishable output

## Architecture

``nTask Input
    |
    v
[Planner] --> [Researcher] --> [Analyzer] --> [Publisher]
                                                    |
                                                    v
                                              Final Output
`'

## Project Structure

` ` + char(96) + `ash
multi-agent-orchestration/
├── models.py              # Data models (Task, AgentType)
├── base_agent.py          # Abstract base class for all agents
├── planner_agent.py       # Planner agent implementation
├── researcher_agent.py    # Researcher agent implementation
├── analyzer_agent.py      # Analyzer agent implementation
├── publisher_agent.py     # Publisher agent implementation
├── orchestrator.py        # Main orchestration logic
├── main.py               # Example usage
├── requirements.txt       # Python dependencies
└── README.md             # This file
` ` + char(96) + `'

## Quick Start

### Installation

` ` + char(96) + `ash
pip install -r requirements.txt
` ` + char(96) + `'

### Running the Example

` ` + char(96) + `ash
python main.py
` ` + char(96) + `'

## How It Works

### 1. Create a Task
\n` ` + char(96) + `python
from models import Task
import uuid

task = Task(
    id=str(uuid.uuid4()),
    initial_query='Your question or topic here'
)
` ` + char(96) + `'

### 2. Initialize Agents
\n` ` + char(96) + `python
from planner_agent import PlannerAgent
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent
from publisher_agent import PublisherAgent

agents = [
    PlannerAgent(),
    ResearcherAgent(),
    AnalyzerAgent(),
    PublisherAgent()
]
` ` + char(96) + `'

### 3. Create Orchestrator and Execute
\n` ` + char(96) + `python
from orchestrator import Orchestrator

orchestrator = Orchestrator(agents)
completed_task = orchestrator.execute(task)
print(completed_task.final_output)
` ` + char(96) + `'

## Extending the Framework

### Creating Custom Agents
\n` ` + char(96) + `python
from base_agent import BaseAgent
from models import AgentType, Task

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__('CustomAgent', AgentType.YOUR_AGENT_TYPE)

    def execute(self, task: Task) -> Task:
        # Your custom logic here
        task.custom_field = 'Your processing result'
        task.mark_agent_complete(self.agent_type)
        return task
` ` + char(96) + `'

### Adding LLM Integration
\nTo integrate with OpenAI or other LLMs, update the agent's execute method:\n\n` ` + char(96) + `python
import openai

class PlannerAgent(BaseAgent):
    def execute(self, task: Task) -> Task:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{
                'role': 'user',
                'content': f'Create a plan for: {task.initial_query}'
            }]
        )
        task.plan = response.choices[0].message.content
        task.mark_agent_complete(self.agent_type)
        return task
` ` + char(96) + `'

## Features

- ✅ Sequential agent pipeline execution
- ✅ Task state management and tracking
- ✅ Logging and monitoring
- ✅ Batch task processing
- ✅ Extensible agent framework
- ✅ Easy LLM integration

## Next Steps

1. Modify agent logic to match your use case
2. Add LLM integration (OpenAI, Anthropic, Hugging Face, etc.)
3. Implement error handling and retry logic
4. Add persistence layer for task history
5. Create API endpoint for remote access

