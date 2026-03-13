# Web Interface Guide

## Overview

The web interface allows you to submit questions to your multi-agent orchestration system through a user-friendly browser-based application. It supports prompt templates that can customize how questions are processed.

## Getting Started

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

The web interface requires:
- **Flask** (web framework)
- **Flask-CORS** (for cross-origin requests)

### Running the Application

1. Navigate to your project directory
2. Run the web application:
```bash
python web_app.py
```

3. Open your browser and go to:
```
http://localhost:5000
```

You should see the Multi-Agent Orchestration web interface.

## Using the Web Interface

### Submitting a Question

1. **Enter your question** in the "Your Question" text area
2. **Optionally select a prompt template** from the dropdown menu
3. **Click "Submit Question"** to send it to the agent system
4. View the results in the Results section below

### Working with Prompt Templates

#### What are Prompt Templates?

Prompt templates are text files that contain a predefined structure for how questions should be processed. They can include:
- Instructions for the agents
- Specific formatting requirements
- Analysis criteria
- Output structure expectations

Templates support **placeholders** like `{question}` that get replaced with your actual question.

#### Example Template

```
Please provide a comprehensive plan for: {question}

Include the following in your analysis:
1. Clear breakdown of the question/task
2. Key information that needs to be gathered
3. Step-by-step approach to address the question
```

When you submit "How can I improve my Python skills?" with this template, it becomes:

```
Please provide a comprehensive plan for: How can I improve my Python skills?

Include the following in your analysis:
1. Clear breakdown of the question/task
2. Key information that needs to be gathered
3. Step-by-step approach to address the question
```

#### Available Templates

By default, three templates are provided:

1. **comprehensive_plan.txt** - Generates a structured plan for the query
2. **research_focused.txt** - Emphasizes research and data gathering
3. **technical_analysis.txt** - Provides technical depth and analysis

### Creating Custom Templates

1. Create a `.txt` file in the `prompt_templates` directory
2. Add your template content with placeholders like `{question}`
3. Refresh the web interface to see your new template in the list
4. Select and use your template

Example template structure:
```
[Your instructions here]

Process the following: {question}

[Additional context and requirements]
```

## API Endpoints

The web application exposes REST API endpoints for programmatic access:

### GET /api/health
Health check endpoint
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "success": true
}
```

### GET /api/templates
Get list of available templates
```bash
curl http://localhost:5000/api/templates
```

Response:
```json
{
  "templates": ["comprehensive_plan.txt", "research_focused.txt", "technical_analysis.txt"],
  "success": true
}
```

### GET /api/template/{template_name}
Get specific template content
```bash
curl http://localhost:5000/api/template/comprehensive_plan.txt
```

Response:
```json
{
  "content": "Please provide a comprehensive plan for: {question}\n...",
  "name": "comprehensive_plan.txt",
  "success": true
}
```

### POST /api/ask
Submit a question to the multi-agent system
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "template": "comprehensive_plan.txt"
  }'
```

Request body:
- `question` (required): The question to process
- `template` (optional): Name of the template to use

Response:
```json
{
  "task_id": "uuid-here",
  "question": "Processed question text",
  "status": "completed",
  "result": "Final output from all agents",
  "success": true
}
```

### GET /api/task/{task_id}
Get status and results of a specific task
```bash
curl http://localhost:5000/api/task/uuid-here
```

Response:
```json
{
  "task_id": "uuid-here",
  "question": "Original question",
  "status": "completed",
  "plan": "Plan from planner agent",
  "research_data": "Data from researcher agent",
  "analysis": "Analysis from analyzer agent",
  "result": "Final output from publisher agent",
  "success": true
}
```

## Frontend Features

### Task ID
Every submitted question gets a unique task ID for tracking and reference.

### Status Indicator
- **Completed** (green): Task has been processed by all agents
- **Processing** (yellow): Task is currently being processed

### Results Display
Results are shown in collapsible sections:
- **Question**: The processed question (with template applied if used)
- **Result**: The final output from all agents

### Template Preview
When you select a template, a preview of its content is displayed below the dropdown menu.

## Advanced Usage

### Using Custom Variables in Templates

Templates use Python's standard string formatting. You can reference:
- `{question}` - The user's question

Example template with question variable:
```
Please analyze this thoroughly: {question}

Use the following framework:
1. What is being asked?
2. Why is this important?
3. What are the solutions?
```

### Batch Processing (API)

You can submit multiple questions sequentially:
```python
import requests

questions = [
    "What is Python?",
    "How do I learn Python?",
    "What are Python frameworks?"
]

for q in questions:
    response = requests.post('http://localhost:5000/api/ask', json={
        'question': q,
        'template': 'comprehensive_plan.txt'
    })
    print(f"Task {response.json()['task_id']} submitted")
```

## Troubleshooting

### Templates not showing
- Ensure `.txt` files are in the `prompt_templates` directory
- Refresh your browser
- Check browser console for errors (F12)

### Server connection errors
- Verify Flask app is running: `python web_app.py`
- Check that port 5000 is not in use
- Ensure firewall allows local connections

### Question not processing
- Check browser console for error messages
- Verify all required agents are initialized
- Check Flask server logs for exceptions

## Configuration

### Changing the Port

Edit `web_app.py` and modify:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change port here
```

### Production Deployment

For production, disable debug mode and use a production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_app.py
```

## Best Practices

1. **Be specific with questions** - More detailed questions get better results
2. **Use templates consistently** - Choose a template that matches your question type
3. **Check task IDs** - Save them for reference and tracking
4. **Monitor agent logs** - Check logs in the Flask output for debugging
5. **Create domain-specific templates** - Customize templates for your use cases

## Architecture

```
Web Request
    ↓
Flask Web App (web_app.py)
    ↓
Prompt Manager (prompt_manager.py)
    ↓
Question + Rendered Template
    ↓
Orchestrator (orchestrator.py)
    ↓
Agent Pipeline:
  - Planner Agent
  - Researcher Agent
  - Analyzer Agent
  - Publisher Agent
    ↓
Final Output
    ↓
Response to Client
```
