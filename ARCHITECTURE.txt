# System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Web Browser          CLI Terminal      External API Clients   │
│  (http://localhost)   (main.py)         (python/curl/etc)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   WEB APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────┐                       │
│  │  Flask Web App (web_app.py)         │                       │
│  ├─────────────────────────────────────┤                       │
│  │ Routes:                             │                       │
│  │  • GET /                            │                       │
│  │  • GET /api/health                  │                       │
│  │  • GET /api/templates               │                       │
│  │  • GET /api/template/{name}         │                       │
│  │  • POST /api/ask                    │                       │
│  │  • GET /api/task/{id}               │                       │
│  │                                     │                       │
│  │ Features:                           │                       │
│  │  • CORS enabled                     │                       │
│  │  • JSON serialization               │                       │
│  │  • Error handling                   │                       │
│  │  • Task tracking                    │                       │
│  └─────────────────────────────────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Data Processing
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────┐                          │
│  │  Prompt Manager                  │                          │
│  │  (prompt_manager.py)             │                          │
│  ├──────────────────────────────────┤                          │
│  │  • Load templates from files     │                          │
│  │  • Render with variables         │                          │
│  │  • Variable substitution         │                          │
│  │  • Cache management              │                          │
│  └──────────────────────────────────┘                          │
│            │                                                   │
│            │ Rendered Question                                │
│            ▼                                                   │
│  ┌──────────────────────────────────┐                          │
│  │  Orchestrator                    │                          │
│  │  (orchestrator.py)               │                          │
│  ├──────────────────────────────────┤                          │
│  │  • Task routing                  │                          │
│  │  • Agent sequencing              │                          │
│  │  • Result aggregation            │                          │
│  │  • Batch processing              │                          │
│  └──────────────────────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Task Processing
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT ORCHESTRATION LAYER                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Task Pipeline (Sequential Execution)                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Task: {                                               │   │
│  │    id, query, plan, research_data, analysis, output   │   │
│  │  }                                                     │   │
│  └────────────────────────────────────────────────────────┘   │
│           │                                                    │
│           ▼                                                    │
│  ┌──────────────────────────────┐                             │
│  │  1. PlannerAgent             │  Creates structured plan   │
│  │     (planner_agent.py)       │  from initial query        │
│  └──────────────────────────────┘                             │
│           │                                                    │
│           │ task.plan = "..."                                │
│           ▼                                                    │
│  ┌──────────────────────────────┐                             │
│  │  2. ResearcherAgent          │  Gathers research data     │
│  │     (researcher_agent.py)    │  based on plan             │
│  └──────────────────────────────┘                             │
│           │                                                    │
│           │ task.research_data = "..."                       │
│           ▼                                                    │
│  ┌──────────────────────────────┐                             │
│  │  3. AnalyzerAgent            │  Analyzes findings         │
│  │     (analyzer_agent.py)      │  and synthesizes results   │
│  └──────────────────────────────┘                             │
│           │                                                    │
│           │ task.analysis = "..."                            │
│           ▼                                                    │
│  ┌──────────────────────────────┐                             │
│  │  4. PublisherAgent           │  Formats final output      │
│  │     (publisher_agent.py)     │  for presentation          │
│  └──────────────────────────────┘                             │
│           │                                                    │
│           │ task.final_output = "..."                        │
│           ▼                                                    │
│  ┌──────────────────────────────┐                             │
│  │  Completed Task Result       │                             │
│  │  (marked as complete)        │                             │
│  └──────────────────────────────┘                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Result Data
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STORAGE & DELIVERY LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Task Storage                  Response Format                │
│  ┌──────────────────────┐      ┌──────────────────────┐       │
│  │  In-Memory DB        │      │  JSON Response       │       │
│  │  tasks_db[task_id]   │─────→│  {                   │       │
│  └──────────────────────┘      │    task_id: "...",   │       │
│  (Dev: Dict storage)           │    status: "...",    │       │
│  (Prod: Database)              │    result: "...",    │       │
│                                │    ...               │       │
│                                │  }                   │       │
│                                └──────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Response
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RESPONSE TO CLIENT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Web Interface          CLI/Script              API Client     │
│  • Display result       • Print output          • JSON data    │
│  • Show status          • Log response          • Parse result │
│  • Track task ID        • Store task ID         • Continue     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
User Input (Web/API/CLI)
        │
        ▼
┌──────────────────────┐
│  Input Validation    │
│  & Normalization     │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ Template Selection?  │
└──────────────────────┘
        │
    ┌───┴───┐
    │       │
   YES     NO
    │       │
    ▼       ▼
 Render   Use as-is
 Template  
    │       │
    └───┬───┘
        │
        ▼
┌──────────────────────┐
│  Create Task Object  │
│  • ID (UUID)         │
│  • Query             │
│  • Metadata          │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Execute Pipeline    │
│  (Orchestrator)      │
└──────────────────────┘
        │
    ┌───┴───┴───┴───┐
    │   │   │   │   │
    ▼   ▼   ▼   ▼   ▼
   P1  P2  P3  P4 Result
        │
        ▼
┌──────────────────────┐
│  Store Results       │
│  task_db[id] = task  │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Format Response     │
│  • task_id           │
│  • status            │
│  • result            │
│  • metadata          │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Send to Client      │
│  HTTP/JSON Response  │
└──────────────────────┘
        │
        ▼
   Client Receives
   & Displays Result
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              WEB INTERFACE                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  index.html (Frontend)                       │  │
│  │  • Question input                            │  │
│  │  • Template selection                        │  │
│  │  • Results display                           │  │
│  │  • Task tracking                             │  │
│  └──────────────────────────────────────────────┘  │
│           │                                         │
│           │ HTTP Requests                          │
│           │                                         │
│           ▼                                         │
│  ┌──────────────────────────────────────────────┐  │
│  │  web_app.py (Flask Server)                   │  │
│  │  • REST endpoints                            │  │
│  │  • Request routing                           │  │
│  │  • CORS handling                             │  │
│  │  • Error management                          │  │
│  └──────────────────────────────────────────────┘  │
│           │                                         │
│           ├─→ Load templates                       │
│           │   └─→ prompt_manager.py                │
│           │       (file system access)             │
│           │                                         │
│           ├─→ Render prompts                       │
│           │   └─→ prompt_manager.py                │
│           │       (variable substitution)          │
│           │                                         │
│           └─→ Execute orchestration                │
│               └─→ orchestrator.py                  │
│                   (agent sequencing)               │
│                                                    │
└─────────────────────────────────────────────────────┘
                       │
                       │ Agent Pipeline
                       │
        ┌──────┬──────┬──────┬──────┐
        │      │      │      │      │
        ▼      ▼      ▼      ▼      ▼
      Plan  Research Analyze Publish Result
        │      │      │      │      │
        │      │      │      │      │
        └──────┴──────┴──────┴──────┘
                       │
                       │
                       ▼
                  Task Results
                       │
                       │
                       ▼
              Response to Client
```

---

## Request/Response Flow

### Web Interface Request
```
1. User enters question and selects template
   ↓
2. JavaScript creates POST request
   {
     "question": "What is AI?",
     "template": "comprehensive_plan.txt"
   }
   ↓
3. Flask receives request at /api/ask
   ↓
4. Validate input
   ↓
5. Load and render template
   {question} → "What is AI?"
   ↓
6. Create Task object
   ↓
7. Call orchestrator.execute(task)
   ↓
8. Task flows through agent pipeline
   ↓
9. Store result in tasks_db
   ↓
10. Format JSON response
    {
      "task_id": "uuid",
      "question": "rendered question",
      "status": "completed",
      "result": "agent outputs"
    }
    ↓
11. Send to client
    ↓
12. JavaScript displays results in HTML
```

---

## Template Rendering Flow

```
User Question: "How to learn Python?"

+ Template File (comprehensive_plan.txt):
  "Please provide a comprehensive plan for: {question}
   
   Include the following in your analysis:
   1. Clear breakdown of the question/task
   2. Key information that needs to be gathered
   3. Step-by-step approach to address the question"

= Rendered Prompt:
  "Please provide a comprehensive plan for: How to learn Python?
   
   Include the following in your analysis:
   1. Clear breakdown of the question/task
   2. Key information that needs to be gathered
   3. Step-by-step approach to address the question"

↓ (Sent to Agent Pipeline)

Result: Enhanced response following template structure
```

---

## Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────┐
│         Internet / Network                      │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│         Reverse Proxy / Load Balancer            │
│         (nginx / HAProxy)                        │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │Gunicorn│  │Gunicorn│  │Gunicorn│ (Multiple Workers)
    │Worker 1│  │Worker 2│  │Worker 3│
    └────────┘  └────────┘  └────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
            ┌──────────────────────┐
            │  Flask Application   │
            │  (web_app.py)        │
            └──────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │Prompt  │  │Database│  │Cache   │
    │Manager │  │(PostgreSQL)│(Redis) │
    └────────┘  └────────┘  └────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
              ┌──────────────────┐
              │ File System      │
              │ • Templates      │
              │ • Logs           │
              │ • Backups        │
              └──────────────────┘
```

---

## Technology Stack

```
Frontend
├── HTML5
├── CSS3 (with animations)
└── Vanilla JavaScript (no frameworks)

Backend
├── Python 3.8+
├── Flask 2.3+
├── Flask-CORS 4.0+
└── Standard Library (logging, json, pathlib)

Storage (Development)
└── In-Memory Dictionary

Storage (Production - Recommended)
├── PostgreSQL
├── MongoDB
└── SQLAlchemy ORM

Deployment
├── Gunicorn WSGI Server
├── nginx Reverse Proxy
├── Docker (optional)
└── systemd (for Linux services)

Monitoring (Optional)
├── Prometheus
├── Grafana
└── ELK Stack
```

---

## Security Architecture

```
┌─────────────────────────────────────────────┐
│  HTTPS/TLS Encryption                       │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Input Validation                           │
│  • Length checks                            │
│  • Type validation                          │
│  • Path traversal prevention                │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Rate Limiting                              │
│  • Per-IP rate limits                       │
│  • Per-user rate limits                     │
│  • DDoS protection                          │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Authentication (Optional)                  │
│  • API keys                                 │
│  • JWT tokens                               │
│  • OAuth 2.0                                │
└─────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Logging & Monitoring                       │
│  • Request/response logging                 │
│  • Error tracking                           │
│  • Performance metrics                      │
└─────────────────────────────────────────────┘
```

---

## Scalability Considerations

```
Single Server
├── 1 Flask process
├── In-memory storage
└── Limited concurrent requests

Horizontal Scaling
├── Multiple Gunicorn workers (4-8 per CPU)
├── Load balancer (nginx/HAProxy)
├── Shared database backend
└── Cache layer (Redis)

Vertical Scaling
├── More CPU cores
├── More RAM
├── SSD storage
└── Faster network

Microservices (Future)
├── API Gateway
├── Agent service (separate processes)
├── Template service
├── Database service
└── Message queue (RabbitMQ/Kafka)
```

This architecture provides:
✅ Clear separation of concerns
✅ Scalability paths
✅ Security considerations
✅ Production readiness
✅ Easy maintenance
