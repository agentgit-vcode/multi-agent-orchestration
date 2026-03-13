"""
Example usage of the Multi-Agent Web Interface API.
Shows how to interact with the web interface programmatically.
"""

import requests
import json
import time
from typing import Optional, Dict, Any


class MultiAgentClient:
    """Client for interacting with the multi-agent web interface."""
    
    def __init__(self, base_url: str = 'http://localhost:5000'):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the web interface (default: http://localhost:5000)
        """
        self.base_url = base_url.rstrip('/')
        self.api_url = f'{self.base_url}/api'
    
    def check_health(self) -> bool:
        """Check if the server is running."""
        try:
            response = requests.get(f'{self.api_url}/health')
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False
    
    def get_templates(self) -> list:
        """Get list of available templates."""
        response = requests.get(f'{self.api_url}/templates')
        data = response.json()
        
        if data.get('success'):
            return data.get('templates', [])
        else:
            raise Exception(f"Error: {data.get('error')}")
    
    def get_template(self, template_name: str) -> str:
        """Get the content of a specific template."""
        response = requests.get(f'{self.api_url}/template/{template_name}')
        data = response.json()
        
        if data.get('success'):
            return data.get('content', '')
        else:
            raise Exception(f"Error: {data.get('error')}")
    
    def ask_question(self, question: str, template: Optional[str] = None) -> Dict[str, Any]:
        """
        Submit a question to the multi-agent system.
        
        Args:
            question: The question to submit
            template: Optional template name to use
        
        Returns:
            Dictionary with task_id, status, result, etc.
        """
        payload = {'question': question}
        if template:
            payload['template'] = template
        
        response = requests.post(
            f'{self.api_url}/ask',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        
        if data.get('success'):
            return data
        else:
            raise Exception(f"Error: {data.get('error')}")
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Get the result of a completed task."""
        response = requests.get(f'{self.api_url}/task/{task_id}')
        data = response.json()
        
        if data.get('success'):
            return data
        else:
            raise Exception(f"Error: {data.get('error')}")
    
    def ask_and_wait(self, question: str, template: Optional[str] = None, 
                     poll_interval: float = 1.0, max_wait: float = 60.0) -> Dict[str, Any]:
        """
        Submit a question and wait for completion.
        
        Args:
            question: The question to submit
            template: Optional template name
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait
        
        Returns:
            Final task result
        """
        # Submit question
        result = self.ask_question(question, template)
        task_id = result['task_id']
        
        print(f"Task submitted: {task_id}")
        
        # Wait for completion
        elapsed = 0
        while elapsed < max_wait:
            task_result = self.get_task_result(task_id)
            status = task_result.get('status')
            
            if status == 'completed':
                print(f"Task completed: {task_id}")
                return task_result
            
            print(f"Status: {status}... ({elapsed}s)")
            time.sleep(poll_interval)
            elapsed += poll_interval
        
        raise TimeoutError(f"Task {task_id} did not complete within {max_wait} seconds")


def example_basic_question():
    """Example 1: Submit a basic question without template."""
    print("\n" + "="*60)
    print("Example 1: Basic Question")
    print("="*60)
    
    client = MultiAgentClient()
    
    # Check server
    if not client.check_health():
        print("❌ Server is not running. Start it with: python web_app.py")
        return
    
    print("✓ Server is running")
    
    # Submit question
    question = "What are the key benefits of using Python for AI development?"
    print(f"\nSubmitting question: {question}")
    
    result = client.ask_question(question)
    
    print(f"\nTask ID: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"\nResult:\n{result['result']}")


def example_with_template():
    """Example 2: Submit a question with a template."""
    print("\n" + "="*60)
    print("Example 2: Question with Template")
    print("="*60)
    
    client = MultiAgentClient()
    
    # Check available templates
    print("Available templates:")
    templates = client.get_templates()
    for i, template in enumerate(templates, 1):
        print(f"  {i}. {template}")
    
    if not templates:
        print("No templates available")
        return
    
    # Use first template
    template_name = templates[0]
    print(f"\nUsing template: {template_name}")
    
    # Show template content
    template_content = client.get_template(template_name)
    print(f"\nTemplate content:\n{template_content}\n")
    
    # Submit question with template
    question = "How can organizations implement effective AI strategies?"
    print(f"Question: {question}")
    
    result = client.ask_question(question, template_name)
    
    print(f"\nTask ID: {result['task_id']}")
    print(f"Status: {result['status']}")
    print(f"\nResult:\n{result['result']}")


def example_batch_processing():
    """Example 3: Process multiple questions."""
    print("\n" + "="*60)
    print("Example 3: Batch Processing")
    print("="*60)
    
    client = MultiAgentClient()
    
    questions = [
        "What is machine learning?",
        "How does deep learning work?",
        "What are neural networks?"
    ]
    
    task_ids = []
    
    # Submit all questions
    print("Submitting batch of questions...")
    for question in questions:
        try:
            result = client.ask_question(question)
            task_id = result['task_id']
            task_ids.append(task_id)
            print(f"  ✓ {question} (Task: {task_id})")
        except Exception as e:
            print(f"  ✗ Error with '{question}': {e}")
    
    # Retrieve results
    print("\nRetrieving results...")
    for task_id in task_ids:
        try:
            result = client.get_task_result(task_id)
            status = result['status']
            print(f"\nTask {task_id}: {status}")
            print(f"Result preview: {result['result'][:200]}...")
        except Exception as e:
            print(f"Error retrieving task {task_id}: {e}")


def example_direct_api():
    """Example 4: Direct API calls using requests."""
    print("\n" + "="*60)
    print("Example 4: Direct API Calls")
    print("="*60)
    
    api_url = 'http://localhost:5000/api'
    
    # Check health
    print("Checking server health...")
    response = requests.get(f'{api_url}/health')
    print(f"Status: {response.json()}")
    
    # Get templates
    print("\nGetting available templates...")
    response = requests.get(f'{api_url}/templates')
    templates = response.json()['templates']
    print(f"Found {len(templates)} templates")
    
    # Submit question
    print("\nSubmitting question...")
    payload = {
        'question': 'Explain the concept of artificial intelligence',
        'template': templates[0] if templates else None
    }
    response = requests.post(f'{api_url}/ask', json=payload)
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")


if __name__ == '__main__':
    print("Multi-Agent Web Interface - API Usage Examples")
    print("=" * 60)
    
    # Uncomment the example you want to run:
    
    # Basic question
    example_basic_question()
    
    # Question with template
    # example_with_template()
    
    # Batch processing
    # example_batch_processing()
    
    # Direct API calls
    # example_direct_api()
