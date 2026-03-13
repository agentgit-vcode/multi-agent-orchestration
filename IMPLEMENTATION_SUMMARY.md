# Multi-Agent Web Interface Implementation

This implementation adds a complete web interface to your multi-agent orchestration system with support for prompt templates.

## What's Included

### New Files Created

1. **web_app.py** - Main Flask web application
   - REST API endpoints for submitting questions
   - Template management
   - Task tracking and retrieval
   - CORS support for cross-origin requests

2. **prompt_manager.py** - Prompt template manager
   - Load templates from text files
   - Render templates with variable substitution
   - List available templates
   - Save/delete templates

3. **templates/index.html** - Modern web interface
   - Responsive design with gradient UI
   - Question input form
   - Template selection and preview
   - Results display with task tracking
   - Real-time status updates

4. **prompt_templates/** - Example templates directory
   - `comprehensive_plan.txt` - Structured planning template
   - `research_focused.txt` - Research-oriented template
   - `technical_analysis.txt` - Technical deep-dive template

5. **run_web_interface.py** - Quick-start script
   - Dependency checking
   - Directory setup
   - One-command startup

6. **WEB_INTERFACE_GUIDE.md** - Detailed usage documentation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Interface

```bash
python run_web_interface.py
```

Or directly:
```bash
python web_app.py
```

### 3. Open in Browser

Navigate to: `http://localhost:5000`

## Features

### 🎯 Core Features

- **Question Submission**: Submit questions through intuitive web form
- **Prompt Templates**: Use or create custom prompt templates
- **Template Preview**: Preview template content before use
- **Task Tracking**: Each question gets a unique task ID
- **Results Display**: View complete agent outputs and analysis

### 🛠️ Technical Features

- **REST API**: Programmatic access to all functionality
- **CORS Support**: Cross-origin requests enabled
- **Error Handling**: Comprehensive error messages
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Template Variables**: Support for `{question}` placeholder substitution

## Usage Scenarios

### Basic Usage
1. Type your question
2. Click "Submit Question"
3. View results

### With Templates
1. Type your question
2. Select a template from the dropdown
3. Preview the template
4. Click "Submit Question"
5. Get templated results

### Creating Custom Templates
1. Create a `.txt` file in `prompt_templates/` directory
2. Add content with `{question}` placeholder
3. Refresh web interface
4. Select and use your template

## API Reference

### GET /api/health
Health check
```bash
curl http://localhost:5000/api/health
```

### GET /api/templates
List available templates
```bash
curl http://localhost:5000/api/templates
```

### GET /api/template/{name}
Get template content
```bash
curl http://localhost:5000/api/template/comprehensive_plan.txt
```

### POST /api/ask
Submit a question
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Your question","template":"template_name.txt"}'
```

### GET /api/task/{task_id}
Get task status and results
```bash
curl http://localhost:5000/api/task/task-id-here
```

## Project Structure

```
multi-agent-orchestration/
├── web_app.py                 # Main Flask application
├── prompt_manager.py          # Template management
├── run_web_interface.py       # Quick start script
├── templates/
│   └── index.html            # Web interface
├── prompt_templates/         # Template files
│   ├── comprehensive_plan.txt
│   ├── research_focused.txt
│   └── technical_analysis.txt
├── WEB_INTERFACE_GUIDE.md    # Detailed guide
├── requirements.txt          # Updated dependencies
├── main.py                   # Original CLI interface
├── orchestrator.py           # Multi-agent orchestrator
├── base_agent.py             # Base agent class
├── models.py                 # Data models
├── planner_agent.py
├── researcher_agent.py
├── analyzer_agent.py
└── publisher_agent.py
```

## How It Works

```
User Question
    ↓
Web Interface (HTML/JavaScript)
    ↓
Flask API (web_app.py)
    ↓
Prompt Manager (optional template rendering)
    ↓
Orchestrator
    ↓
Agent Pipeline:
  1. PlannerAgent - Creates initial plan
  2. ResearcherAgent - Gathers research
  3. AnalyzerAgent - Analyzes findings
  4. PublisherAgent - Formats output
    ↓
Results back to Web Interface
    ↓
Display to User
```

## Prompt Template Guide

### Template Syntax

Templates use Python's string formatting syntax:
```
{variable_name}
```

### Available Variables

- `{question}` - The user's question

### Example Template

```
Analyze the following query comprehensively: {question}

Please structure your response as:
1. Executive Summary
2. Key Points
3. Supporting Details
4. Conclusion and Recommendations
```

### Creating Effective Templates

1. **Be Specific**: Include clear instructions for the agents
2. **Structure**: Define expected output format
3. **Context**: Provide relevant context and examples
4. **Constraints**: Mention any limitations or focus areas

## Production Deployment

### Using Gunicorn (Recommended)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app.py
```

### Environment Variables

For production, set environment variables:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

### Running as a Service

Create a systemd service file for automatic startup:
```ini
[Unit]
Description=Multi-Agent Web Interface
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 web_app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Templates Not Showing
- Check `prompt_templates/` directory exists
- Ensure `.txt` files are in the correct location
- Refresh browser cache

### Port Already in Use
- Change port in `web_app.py`: `app.run(port=8000)`
- Or stop other services using port 5000

### Agent Execution Issues
- Check Flask logs for error details
- Verify all agent modules are importable
- Ensure agent configurations are correct

## Future Enhancements

Potential improvements:
- WebSocket support for real-time updates
- Database backend for persistent task storage
- Authentication and user management
- Template versioning
- Multi-user support
- Analytics and task history
- Agent performance monitoring
- Advanced template conditions and loops

## Integration with Existing Code

The web interface integrates seamlessly with your existing:
- `orchestrator.py` - Unchanged, used directly
- `base_agent.py` - Unchanged, base class used by all agents
- `models.py` - Task model extended with web interface features
- All agent implementations - Unchanged, executed as-is

## Notes

- Tasks are stored in memory (suitable for development)
- For production, integrate with a database
- Template rendering uses Python's `string.Formatter`
- CORS is enabled for cross-origin requests
- Debug mode is enabled by default for development
