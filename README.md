# Multi-Agent Orchestration Framework

## Overview

This is a Python-based multi-agent orchestration system where tasks flow through a pipeline of specialized agents:

1. **Planner Agent** - Creates a structured plan based on the initial query
2. **Researcher Agent** - Gathers research data based on the plan
3. **Analyzer Agent** - Analyzes the research data and draws conclusions
4. **Publisher Agent** - Compiles everything into a final publishable output

## Architecture

```
Task Input
    |
    v
[Planner] --> [Researcher] --> [Analyzer] --> [Publisher]
                                                    |
                                                    v
                                              Final Output
```

## Project Structure

```bash
multi-agent-orchestration/
├── main.py                    # CLI entry point
├── run_web_interface.py       # Web interface launcher
├── web_app.py                 # Flask web application & REST API
├── orchestrator.py            # Main orchestration logic
├── base_agent.py              # Abstract base class for all agents
├── models.py                  # Data models (Task, AgentType)
├── llm_handler.py             # LLM integration (OpenAI & Google Gemini)
├── prompt_manager.py          # Prompt template manager
├── agent_instructions_manager.py  # Agent instructions loader
├── planner_agent.py           # Planner agent implementation
├── researcher_agent.py        # Researcher agent implementation
├── analyzer_agent.py          # Analyzer agent implementation
├── publisher_agent.py         # Publisher agent implementation
├── agent_instructions/        # Custom instructions per agent
│   ├── planner.txt
│   ├── researcher.txt
│   ├── analyzer.txt
│   └── publisher.txt
├── prompt_templates/          # Prompt templates for the web UI
│   ├── comprehensive_plan.txt
│   ├── research_focused.txt
│   └── technical_analysis.txt
├── templates/
│   └── index.html             # Web interface HTML
├── docs/                      # Reference documentation (see below)
├── examples.py                # Running the pipeline directly in Python
├── workflow_example.py        # End-to-end demo driving the running web API
├── api_client_examples.py     # REST API client patterns
├── verify_setup.py            # Preflight check: .env, dependencies, agents
├── .env.example               # Environment variable template
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` with your preferred LLM provider:

```env
# Use Google Gemini
LLM_PROVIDER=google
GOOGLE_API_KEY=your-google-api-key-here

# Or use OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your-openai-api-key-here
# OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_TEMPERATURE=0.7
```

### 3. Verify the Setup

```bash
python3 verify_setup.py
```

Reads `LLM_PROVIDER` from your `.env` and checks the setup for whichever
backend it selects — the right API key, that provider's SDK, and that the LLM
handler and agents import cleanly — before you run the pipeline.

### 4. Run the CLI Example

```bash
python3 main.py
```

### 5. Run the Web Interface

```bash
python3 run_web_interface.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

> **Note (macOS):** Port 5000 may be occupied by AirPlay Receiver. Either disable it in **System Settings → General → AirDrop & Handoff**, or start on a different port:
> ```bash
> python3 -c "from web_app import app; app.run(debug=True, host='0.0.0.0', port=5001)"
> ```

## Web Interface

The web interface provides a visual way to interact with the multi-agent system:

- **Ask a Question** — Type your query and optionally select a prompt template
- **Agent Instructions** — View and edit each agent's system instructions directly from the UI
- **REST API** — Programmatic access via API endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web interface |
| `/api/ask` | POST | Submit a question |
| `/api/task/<task_id>` | GET | Get task status/results |
| `/api/instructions` | GET | List all agent instructions |
| `/api/instructions/<name>` | PUT | Update agent instructions |
| `/api/templates` | GET | List prompt templates |
| `/api/template/<name>` | GET | Get template content |
| `/api/health` | GET | Health check |

## How It Works

### 1. Create a Task

```python
from models import Task
import uuid

task = Task(
    id=str(uuid.uuid4()),
    initial_query='Your question or topic here'
)
```

### 2. Initialize Agents

```python
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
```

### 3. Create Orchestrator and Execute

```python
from orchestrator import Orchestrator

orchestrator = Orchestrator(agents)
completed_task = orchestrator.execute(task)
print(completed_task.final_output)
```

## Extending the Framework

### Creating Custom Agents

```python
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
```

### Customizing Agent Instructions

Each agent loads custom instructions from text files in the `agent_instructions/` directory. Edit these files to change how each agent behaves:

- `agent_instructions/planner.txt` — Planning strategy and output format
- `agent_instructions/researcher.txt` — Research approach and depth
- `agent_instructions/analyzer.txt` — Analysis framework and methodology
- `agent_instructions/publisher.txt` — Report format and structure

### Adding Prompt Templates

Create `.txt` files in the `prompt_templates/` directory. Use `{question}` as a placeholder for user input:

```text
You are tasked with the following question: {question}

Please provide a detailed, step-by-step response.
```

## Writing Good Queries

The pipeline produces a memo, so it rewards scenarios over one-liners. Give it
the constraints you actually have — scale, budget, timeline, the hard
requirement — and the agents have something to plan, research, and weigh.

**Do this:**

```text
We need to decide whether to migrate our 20-year-old monolithic system to
microservices. We have 150 engineers, a $5M budget, and a 6-month timeline.
Our constraint is zero downtime. Should we proceed?
```

**Not this:**

```text
Should we use microservices?
```

## FAQ

**Can I change the order of the agents?**
Yes — reorder them when constructing the `Orchestrator`:

```python
orchestrator = Orchestrator([AnalyzerAgent(), PlannerAgent(), ResearcherAgent(), PublisherAgent()])
```

**Can I skip an agent?** Yes — leave it out of the list.

**How do I pass data between agents?** Everything moves through the `Task`
object. Each agent reads the fields it needs and writes its own output back.

## Documentation

| Document | Covers |
|---|---|
| [docs/architecture.md](docs/architecture.md) | System layers, data flow, component interaction, deployment and scaling notes |
| [docs/llm-setup.md](docs/llm-setup.md) | Provider setup, model and temperature tuning, token limits, cost estimates, troubleshooting |
| [docs/agent-instructions.md](docs/agent-instructions.md) | How per-agent instruction files reach the LLM, and how to rewrite them |
| [docs/web-interface.md](docs/web-interface.md) | Web UI walkthrough and full REST API reference |
| [docs/configuration.md](docs/configuration.md) | Server, template, API, and logging configuration |

## Features

- ✅ Sequential agent pipeline execution
- ✅ Task state management and tracking
- ✅ Logging and monitoring
- ✅ Batch task processing
- ✅ Extensible agent framework
- ✅ LLM integration (OpenAI & Google Gemini)
- ✅ Flask web interface with REST API
- ✅ Customizable agent instructions
- ✅ Prompt template system
