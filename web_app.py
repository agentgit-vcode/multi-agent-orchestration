"""
Web interface for the multi-agent orchestration system.
Provides REST API endpoints for submitting questions and retrieving results.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import uuid
from typing import Dict, Optional
import os

from models import Task
from planner_agent import PlannerAgent
from researcher_agent import ResearcherAgent
from analyzer_agent import AnalyzerAgent
from publisher_agent import PublisherAgent
from orchestrator import Orchestrator
from prompt_manager import PromptManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Initialize the multi-agent system
agents = [
    PlannerAgent(),
    ResearcherAgent(),
    AnalyzerAgent(),
    PublisherAgent()
]
orchestrator = Orchestrator(agents)

# Initialize prompt manager
prompt_manager = PromptManager(templates_dir='prompt_templates')

# In-memory task storage (for demo; use a database for production)
tasks_db: Dict[str, Task] = {}

logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get list of available prompt templates."""
    try:
        templates = prompt_manager.list_templates()
        return jsonify({'templates': templates, 'success': True})
    except Exception as e:
        logger.error(f'Error retrieving templates: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/template/<template_name>', methods=['GET'])
def get_template(template_name):
    """Get a specific prompt template content."""
    try:
        content = prompt_manager.get_template(template_name)
        return jsonify({'content': content, 'name': template_name, 'success': True})
    except FileNotFoundError as e:
        logger.error(f'Template not found: {template_name}')
        return jsonify({'error': f'Template not found: {template_name}', 'success': False}), 404
    except Exception as e:
        logger.error(f'Error retrieving template: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Submit a question to the multi-agent system.
    
    Request body:
    {
        "question": "Your question here",
        "template": "template_name.txt" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Missing required field: question', 'success': False}), 400
        
        question = data['question'].strip()
        template_name = data.get('template')
        
        if not question:
            return jsonify({'error': 'Question cannot be empty', 'success': False}), 400
        
        # Apply prompt template if provided
        if template_name:
            template_content = prompt_manager.get_template(template_name)
            question = prompt_manager.render_template(template_content, question=question)
        
        # Create task
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            initial_query=question
        )
        
        # Execute orchestration
        logger.info(f'Processing task {task_id} with question: {question[:100]}...')
        completed_task = orchestrator.execute(task)
        
        # Store task
        tasks_db[task_id] = completed_task
        
        return jsonify({
            'task_id': task_id,
            'question': question,
            'status': 'completed' if completed_task.is_complete() else 'processing',
            'result': completed_task.final_output,
            'success': True
        })
    
    except Exception as e:
        logger.error(f'Error processing question: {str(e)}', exc_info=True)
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get the status and results of a task."""
    try:
        if task_id not in tasks_db:
            return jsonify({'error': 'Task not found', 'success': False}), 404
        
        task = tasks_db[task_id]
        
        return jsonify({
            'task_id': task_id,
            'question': task.initial_query,
            'status': 'completed' if task.is_complete() else 'processing',
            'plan': task.plan,
            'research_data': task.research_data,
            'analysis': task.analysis,
            'result': task.final_output,
            'success': True
        })
    
    except Exception as e:
        logger.error(f'Error retrieving task: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'success': True})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('prompt_templates', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
