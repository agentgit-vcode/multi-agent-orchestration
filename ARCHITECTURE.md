# ARCHITECTURE DIAGRAM

## System Overview
\n` ` + char(96) + `'
┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR (Main Controller)                 │
│                                                                   │
│  Manages agent pipeline, task passing, and execution order      │
└───────────────────┬───────────────────────────────────────────┬─┘
                    │                                               │
                    ▼                                               ▼
        ┌──────────────────────┐                      ┌──────────────────────┐
        │      TASK OBJECT      │                      │  AGENT PIPELINE      │
        ├──────────────────────┤                      ├──────────────────────┤
        │ id: str              │──────────────────►   │ 1. PlannerAgent      │
        │ initial_query: str   │                      │ 2. ResearcherAgent   │
        │ plan: str            │                      │ 3. AnalyzerAgent     │
        │ research_data: str   │                      │ 4. PublisherAgent    │
        │ analysis: str        │                      │                      │
        │ final_output: str    │                      │ Each agent:          │
        │ completed_agents: [] │◄──────────────────   │ - Inherits BaseAgent │
        │ metadata: {}         │                      │ - Implements execute()│
        └──────────────────────┘                      │ - Marks completion   │
                                                     └──────────────────────┘


## Data Flow
\n` ` + char(96) + `'
┌─────────────┐
│ Input Query │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PLANNER AGENT                                               │
│  • Receives: initial_query                                   │
│  • Processing: Creates plan based on query                   │
│  • Outputs: task.plan                                        │
│  • Marks: PLANNER in completed_agents                       │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  RESEARCHER AGENT                                            │
│  • Receives: initial_query + plan                            │
│  • Processing: Gathers research based on plan                │
│  • Outputs: task.research_data                               │
│  • Marks: RESEARCHER in completed_agents                    │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  ANALYZER AGENT                                              │
│  • Receives: research_data + plan                            │
│  • Processing: Analyzes research findings                    │
│  • Outputs: task.analysis                                    │
│  • Marks: ANALYZER in completed_agents                      │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  PUBLISHER AGENT                                             │
│  • Receives: plan + research + analysis                      │
│  • Processing: Compiles final output                         │
│  • Outputs: task.final_output                                │
│  • Marks: PUBLISHER in completed_agents                     │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────┐
│   Final Output       │
│ (Ready to publish)   │
└──────────────────────┘
` ` + char(96) + `\n\n\n## Class Hierarchy
\n` ` + char(96) + `'
                    ┌──────────────────┐
                    │   BaseAgent      │  (Abstract)
                    │    (ABC)         │
                    ├──────────────────┤
                    │ + name: str      │
                    │ + agent_type     │
                    │ + execute(task)  │
                    │ + _log_execution │
                    └────────┬─────────┘
                              │
            ┌─────────────────┼─────────────────┬──────────────────┐
            │                 │                 │                  │
            ▼                 ▼                 ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │PlannerAgent  │  │ResearcherAgent│ │AnalyzerAgent │  │PublisherAgent│
    └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
` ` + char(96) + `\n\n\n## Module Dependencies
\n` ` + char(96) + `'
models.py (No dependencies - Core data structures)
   ▲
   │ imports
   │
base_agent.py
   ▲
   │ imports
   │
┌──┴──┬─────────────┬──────────────┬──────────────┐
│     │             │              │              │
planner_ researcher_ analyzer_   publisher_
agent.py agent.py     agent.py     agent.py
   │     │             │              │
   └──┬──┴─────────────┴──────────────┴──────────────┘
      │ imports
      ▼
orchestrator.py
      │ imports
      ▼
  main.py (or your application)
` ` + char(96) + `\n\n## Extensibility Points
\n1. **Create Custom Agents** - Inherit from BaseAgent
2. **Custom Task Fields** - Add to Task.metadata
3. **Custom Agent Types** - Add to AgentType enum
4. **Parallel Execution** - Override Orchestrator.execute()
5. **Task Persistence** - Create Repository class
6. **LLM Integration** - Override agent execute() methods
7. **Error Handling** - Wrap agent calls in try-catch
8. **Monitoring** - Add metrics/prometheus exports
\n
