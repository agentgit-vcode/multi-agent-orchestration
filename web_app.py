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
from agent_instructions_manager import AgentInstructionsManager
from llm_handler import LLMHandler
from metrics import metrics_store, TaskMetrics


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# Initialize the multi-agent system (default model)
agents = [
    PlannerAgent(),
    ResearcherAgent(),
    AnalyzerAgent(),
    PublisherAgent()
]
orchestrator = Orchestrator(agents)

# Initialize prompt manager
prompt_manager = PromptManager(templates_dir='prompt_templates')

# Initialize agent instructions manager
instructions_manager = AgentInstructionsManager(instructions_dir='agent_instructions')

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


@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available LLM models."""
    try:
        models = LLMHandler.get_available_models()
        return jsonify({'models': models, 'success': True})
    except Exception as e:
        logger.error(f'Error retrieving models: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Submit a question to the multi-agent system.

    Request body:
    {
        "question": "Your question here",
        "model": "google/gemini-pro-latest" (optional, format: provider/model)
    }
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({'error': 'Missing required field: question', 'success': False}), 400

        question = data['question'].strip()

        if not question:
            return jsonify({'error': 'Question cannot be empty', 'success': False}), 400

        # Determine model to use
        model_spec = data.get('model', '')
        llm = None
        provider_name = ''
        model_name = ''

        if model_spec and '/' in model_spec:
            provider_name, model_name = model_spec.split('/', 1)
            try:
                llm = LLMHandler(provider=provider_name, model_name=model_name)
            except Exception as e:
                logger.warning(f'Failed to create LLM for {model_spec}: {e}, falling back to default')
                llm = None

        # Create agents with the selected model
        if llm:
            task_agents = [
                PlannerAgent(llm=llm),
                ResearcherAgent(llm=llm),
                AnalyzerAgent(llm=llm),
                PublisherAgent(llm=llm)
            ]
            task_orchestrator = Orchestrator(task_agents)
        else:
            task_orchestrator = orchestrator
            # Get default provider/model info
            from llm_handler import get_llm_handler
            try:
                default_llm = get_llm_handler()
                provider_name = default_llm.llm_provider
                model_name = default_llm.model_name
            except Exception:
                provider_name = 'unknown'
                model_name = 'unknown'

        # Create task
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            initial_query=question
        )

        # Execute orchestration
        logger.info(f'Processing task {task_id} with model {provider_name}/{model_name}: {question[:100]}...')
        completed_task = task_orchestrator.execute(task)

        # Store task
        tasks_db[task_id] = completed_task

        # Record metrics
        task_metrics = TaskMetrics(
            task_id=task_id,
            question=question,
            model=model_name,
            provider=provider_name,
        )
        # Copy agent call metrics
        for call_metric_dict in completed_task.metadata.get('agent_metrics', []):
            from metrics import LLMCallMetrics
            call_metric = LLMCallMetrics(**call_metric_dict)
            task_metrics.add_call(call_metric)
        task_metrics.agent_timings = completed_task.metadata.get('agent_timings', {})
        task_metrics.total_duration_seconds = completed_task.metadata.get('total_duration_seconds', 0)
        metrics_store.record(task_metrics)

        return jsonify({
            'task_id': task_id,
            'question': question,
            'status': 'completed' if completed_task.is_complete() else 'processing',
            'result': completed_task.final_output,
            'model': f'{provider_name}/{model_name}',
            'metrics': task_metrics.to_dict(),
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
        task_metrics = metrics_store.get_task_metrics(task_id)

        response = {
            'task_id': task_id,
            'question': task.initial_query,
            'status': 'completed' if task.is_complete() else 'processing',
            'plan': task.plan,
            'research_data': task.research_data,
            'analysis': task.analysis,
            'result': task.final_output,
            'success': True
        }

        if task_metrics:
            response['metrics'] = task_metrics.to_dict()

        return jsonify(response)

    except Exception as e:
        logger.error(f'Error retrieving task: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get aggregate analytics across all tasks."""
    try:
        return jsonify({
            'stats': metrics_store.get_aggregate_stats(),
            'history': metrics_store.get_history(),
            'success': True
        })
    except Exception as e:
        logger.error(f'Error retrieving analytics: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/instructions', methods=['GET'])
def get_instructions():
    """Get all agent instructions with their content."""
    try:
        agents_dict = {
            'planner': instructions_manager.get_planner_instructions(),
            'researcher': instructions_manager.get_researcher_instructions(),
            'analyzer': instructions_manager.get_analyzer_instructions(),
            'publisher': instructions_manager.get_publisher_instructions(),
        }
        return jsonify({'instructions': agents_dict, 'success': True})
    except Exception as e:
        logger.error(f'Error retrieving instructions: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/instructions/<agent_name>', methods=['PUT'])
def update_instructions(agent_name):
    """Update an agent's instructions."""
    try:
        valid_agents = ['planner', 'researcher', 'analyzer', 'publisher']
        if agent_name not in valid_agents:
            return jsonify({'error': f'Invalid agent: {agent_name}. Must be one of {valid_agents}', 'success': False}), 400

        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'Missing required field: content', 'success': False}), 400

        filepath = instructions_manager.instructions_dir / f'{agent_name}.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data['content'])

        # Clear cache so next load picks up changes
        instructions_manager._instructions_cache.pop(f'{agent_name}.txt', None)

        logger.info(f'Updated instructions for {agent_name}')
        return jsonify({'success': True, 'message': f'{agent_name} instructions updated'})
    except Exception as e:
        logger.error(f'Error updating instructions: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'success': True})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('prompt_templates', exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5000)
