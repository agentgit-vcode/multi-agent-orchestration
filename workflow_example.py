"""
Complete Example Workflow: Using the Multi-Agent Web Interface
This demonstrates a real-world usage scenario.
"""

import requests
import json
import time


class WorkflowExample:
    """Demonstrates a complete workflow with the web interface."""
    
    def __init__(self):
        self.api_url = 'http://localhost:5000/api'
        self.templates = []
    
    def run(self):
        """Execute the complete workflow."""
        print("\n" + "="*70)
        print("COMPLETE WORKFLOW EXAMPLE - MULTI-AGENT WEB INTERFACE")
        print("="*70)
        
        # Step 1: Check server health
        if not self.check_server():
            return
        
        # Step 2: List available templates
        self.list_templates()
        
        # Step 3: Create a custom template (conceptual)
        self.show_custom_template_example()
        
        # Step 4: Submit questions with different approaches
        self.demonstrate_basic_question()
        self.demonstrate_template_question()
        self.demonstrate_batch_processing()
        
        # Step 5: Retrieve and display results
        self.show_final_summary()
    
    def check_server(self) -> bool:
        """Step 1: Verify server is running."""
        print("\n[STEP 1] Checking Server Connection")
        print("-" * 70)
        
        try:
            response = requests.get(f'{self.api_url}/health')
            if response.status_code == 200:
                print("✓ Server is running at http://localhost:5000")
                return True
            else:
                print("✗ Server returned unexpected status code")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to server")
            print("  Start the server with: python web_app.py")
            return False
    
    def list_templates(self):
        """Step 2: Show available templates."""
        print("\n[STEP 2] Available Templates")
        print("-" * 70)
        
        try:
            response = requests.get(f'{self.api_url}/templates')
            data = response.json()
            self.templates = data.get('templates', [])
            
            if self.templates:
                print(f"Found {len(self.templates)} templates:")
                for i, template in enumerate(self.templates, 1):
                    print(f"\n  {i}. {template}")
                    # Show template preview
                    response = requests.get(f'{self.api_url}/template/{template}')
                    content = response.json().get('content', '')
                    preview = content[:200] + ('...' if len(content) > 200 else '')
                    print(f"     Preview: {preview}")
            else:
                print("No templates found")
        
        except Exception as e:
            print(f"✗ Error listing templates: {e}")
    
    def show_custom_template_example(self):
        """Step 3: Demonstrate how to create custom templates."""
        print("\n[STEP 3] Custom Template Example")
        print("-" * 70)
        
        example_template = """Please create a detailed business plan for: {question}

Structure your response as follows:

EXECUTIVE SUMMARY
- Brief overview of the concept
- Key benefits and opportunities

MARKET ANALYSIS
- Current market size and growth
- Competition landscape
- Target audience

IMPLEMENTATION STRATEGY
- Phase 1: Planning and preparation
- Phase 2: Initial launch
- Phase 3: Scaling and optimization

FINANCIAL PROJECTIONS
- Initial investment required
- Expected ROI timeline
- Break-even analysis

SUCCESS METRICS
- Key performance indicators
- Measurement approach
- Timeline for evaluation"""
        
        print("Example template content:")
        print("\n" + "="*70)
        print(example_template)
        print("="*70)
        print("\nTo use this template:")
        print("1. Save as: prompt_templates/business_plan.txt")
        print("2. Refresh the web interface")
        print("3. Select 'business_plan.txt' when asking a question")
    
    def demonstrate_basic_question(self):
        """Step 4a: Basic question without template."""
        print("\n[STEP 4A] Submitting Basic Question (No Template)")
        print("-" * 70)
        
        question = "What are the latest trends in artificial intelligence?"
        print(f"Question: {question}")
        
        try:
            response = requests.post(
                f'{self.api_url}/ask',
                json={'question': question},
                headers={'Content-Type': 'application/json'}
            )
            data = response.json()
            
            if data.get('success'):
                task_id = data.get('task_id')
                status = data.get('status')
                result = data.get('result', '')
                
                print(f"\n✓ Question submitted successfully")
                print(f"  Task ID: {task_id}")
                print(f"  Status: {status}")
                print(f"  Result preview: {result[:150]}...")
            else:
                print(f"✗ Error: {data.get('error')}")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def demonstrate_template_question(self):
        """Step 4b: Question with template."""
        print("\n[STEP 4B] Submitting Question with Template")
        print("-" * 70)
        
        if not self.templates:
            print("No templates available to demonstrate")
            return
        
        template = self.templates[0]
        question = "How can companies integrate machine learning into their operations?"
        
        print(f"Question: {question}")
        print(f"Template: {template}")
        
        try:
            response = requests.post(
                f'{self.api_url}/ask',
                json={
                    'question': question,
                    'template': template
                },
                headers={'Content-Type': 'application/json'}
            )
            data = response.json()
            
            if data.get('success'):
                task_id = data.get('task_id')
                status = data.get('status')
                
                print(f"\n✓ Question with template submitted successfully")
                print(f"  Task ID: {task_id}")
                print(f"  Status: {status}")
                print(f"  Template applied to customize the response")
            else:
                print(f"✗ Error: {data.get('error')}")
        
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def demonstrate_batch_processing(self):
        """Step 4c: Multiple questions."""
        print("\n[STEP 4C] Batch Processing Multiple Questions")
        print("-" * 70)
        
        questions = [
            "What is natural language processing?",
            "How does computer vision work?",
            "Explain neural networks in simple terms"
        ]
        
        print(f"Processing {len(questions)} questions:\n")
        
        task_ids = []
        for i, question in enumerate(questions, 1):
            print(f"  {i}. {question}")
            
            try:
                response = requests.post(
                    f'{self.api_url}/ask',
                    json={'question': question},
                    headers={'Content-Type': 'application/json'}
                )
                data = response.json()
                
                if data.get('success'):
                    task_id = data.get('task_id')
                    task_ids.append(task_id)
                    print(f"     ✓ Task ID: {task_id}")
                else:
                    print(f"     ✗ Error: {data.get('error')}")
            
            except Exception as e:
                print(f"     ✗ Error: {e}")
        
        print(f"\n✓ {len(task_ids)} questions submitted for batch processing")
    
    def show_final_summary(self):
        """Step 5: Final summary and next steps."""
        print("\n[STEP 5] Workflow Summary")
        print("-" * 70)
        
        print("""
WORKFLOW COMPLETED

What you demonstrated:
✓ Server health check
✓ Template listing and preview
✓ Custom template creation guide
✓ Basic question submission
✓ Template-based question submission
✓ Batch processing

KEY FEATURES:

1. PROMPT TEMPLATES
   - Predefined structures for different question types
   - Variables like {question} get replaced automatically
   - Easy way to ensure consistent, detailed responses

2. REST API
   - Submit questions programmatically
   - Check task status
   - Retrieve detailed results
   - Integrate with other systems

3. WEB INTERFACE
   - User-friendly browser-based UI
   - Real-time task tracking
   - Template preview before submission
   - Mobile responsive design

4. MULTI-AGENT ORCHESTRATION
   - Questions flow through:
     • Planner Agent (creates plan)
     • Researcher Agent (gathers information)
     • Analyzer Agent (analyzes findings)
     • Publisher Agent (formats output)

NEXT STEPS:

1. Create Custom Templates
   - Design templates for your specific use cases
   - Include detailed instructions for agents
   - Define output structure

2. Integration
   - Use the API to integrate with other tools
   - Create automated workflows
   - Build custom interfaces

3. Optimization
   - Monitor agent performance
   - Fine-tune prompt templates
   - Measure response quality

4. Scaling
   - Deploy to production server
   - Configure database backend
   - Set up monitoring and logging

DOCUMENTATION:
- QUICKSTART.md - Quick setup guide
- WEB_INTERFACE_GUIDE.md - Detailed user guide
- CONFIGURATION_GUIDE.md - Advanced setup
- api_client_examples.py - Code examples

""")


def run_workflow():
    """Run the complete workflow example."""
    workflow = WorkflowExample()
    workflow.run()


if __name__ == '__main__':
    run_workflow()
