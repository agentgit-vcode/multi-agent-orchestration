# Configuration and Customization Guide

## Server Configuration

### Port Configuration

To change the port the web server runs on, edit `web_app.py`:

```python
if __name__ == '__main__':
    os.makedirs('prompt_templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=8000)  # Change port here
```

### Host Configuration

To make the server accessible from other machines, change the host:

```python
# Current (localhost only)
app.run(debug=True, host='127.0.0.1', port=5000)

# Accessible from network
app.run(debug=True, host='0.0.0.0', port=5000)

# Specific IP
app.run(debug=True, host='192.168.1.100', port=5000)
```

### Debug Mode

For production, disable debug mode:

```python
# Development
app.run(debug=True, ...)

# Production
app.run(debug=False, ...)
```

## Template Configuration

### Custom Templates Directory

Change where templates are stored in `web_app.py`:

```python
# Default location
prompt_manager = PromptManager(templates_dir='prompt_templates')

# Custom location
prompt_manager = PromptManager(templates_dir='./custom/templates')
```

### Template Variables

Extend available template variables by modifying `prompt_manager.py`:

```python
def render_template(self, template: str, **kwargs) -> str:
    # Add preprocessing here if needed
    return string.Formatter().vformat(template, (), kwargs)
```

Example custom variable substitution:

```python
# In web_app.py, before rendering
if template_name:
    template_content = prompt_manager.get_template(template_name)
    # Add custom variables
    question = prompt_manager.render_template(
        template_content,
        question=question,
        timestamp=datetime.now().isoformat(),
        user="admin"
    )
```

Then use in template:
```
Question: {question}
Submitted: {timestamp}
By: {user}
```

## API Configuration

### CORS Settings

Current settings allow all origins. To restrict CORS:

```python
# In web_app.py
from flask_cors import CORS

# Current (allow all)
CORS(app)

# Restricted to specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://myapp.com"],
        "methods": ["GET", "POST"]
    }
})
```

### Request Size Limits

Configure maximum request size in `web_app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
```

## Task Storage Configuration

### Current (In-Memory)

Tasks are stored in a Python dictionary. Good for development, not production:

```python
tasks_db: Dict[str, Task] = {}
```

### Database Integration Example

To use SQLAlchemy with a database:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL example
DATABASE_URL = "postgresql://user:password@localhost/multi_agent"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Use in endpoints
@app.route('/api/ask', methods=['POST'])
def ask_question():
    # ... question processing ...
    session = Session()
    db_task = TaskModel(
        id=task_id,
        query=question,
        result=completed_task.final_output
    )
    session.add(db_task)
    session.commit()
```

## Logging Configuration

### Change Log Level

Modify logging configuration in `web_app.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG, INFO, WARNING, ERROR
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)
```

### Log to File

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='web_app.log',
    filemode='a'
)
```

## Performance Tuning

### Thread Pool Size

For concurrent requests, use a production WSGI server:

```bash
# Gunicorn with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 web_app.py

# Gunicorn with more workers for high load
gunicorn -w 16 -b 0.0.0.0:5000 web_app.py
```

### Caching Templates

Add template caching in `prompt_manager.py`:

```python
from functools import lru_cache

class PromptManager:
    def __init__(self, templates_dir: str = 'prompt_templates'):
        self.templates_dir = Path(templates_dir)
        self._template_cache = {}
    
    @lru_cache(maxsize=100)
    def get_template(self, template_name: str) -> str:
        # Cached template loading
        if template_name in self._template_cache:
            return self._template_cache[template_name]
        
        template_path = self.templates_dir / template_name
        with open(template_path, 'r') as f:
            content = f.read()
            self._template_cache[template_name] = content
            return content
```

## Security Configuration

### Input Validation

Add validation to `web_app.py`:

```python
@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    
    # Validate question length
    question = data.get('question', '').strip()
    if len(question) > 5000:
        return jsonify({'error': 'Question too long', 'success': False}), 400
    
    # Validate template name
    template_name = data.get('template')
    if template_name and '..' in template_name:
        return jsonify({'error': 'Invalid template name', 'success': False}), 400
    
    # ... rest of function
```

### Rate Limiting

Install Flask-Limiter:

```bash
pip install Flask-Limiter
```

Then in `web_app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/ask', methods=['POST'])
@limiter.limit("10 per minute")
def ask_question():
    # ... implementation
```

### HTTPS Configuration

For production, use HTTPS:

```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443,
        ssl_context=('cert.pem', 'key.pem')
    )
```

## Frontend Customization

### Theme Configuration

Edit CSS in `templates/index.html`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #28a745;
    --error-color: #dc3545;
}

body {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
}
```

### Branding

Customize header in HTML:

```html
<header>
    <h1>🤖 Your Company Name - AI Assistant</h1>
    <p>Your custom description here</p>
</header>
```

## Monitoring and Health Checks

### Add Metrics Endpoint

```python
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    return jsonify({
        'total_tasks': len(tasks_db),
        'completed_tasks': sum(1 for t in tasks_db.values() if t.is_complete()),
        'templates_available': len(prompt_manager.list_templates()),
        'uptime': time.time() - app.start_time
    })
```

### Prometheus Integration

```python
from prometheus_client import Counter, Histogram, generate_latest

question_counter = Counter('questions_submitted', 'Total questions submitted')
response_time = Histogram('response_time_seconds', 'Response time in seconds')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

## Environment Variables

Create a `.env` file:

```
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///tasks.db
API_KEY=your_api_key_here
TEMPLATES_DIR=prompt_templates
MAX_QUESTION_LENGTH=5000
```

Load in Python:

```python
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
```

## Troubleshooting Configuration

### Common Issues

1. **Port already in use**
   ```bash
   # Windows: Find process using port
   netstat -ano | findstr :5000
   
   # Kill process
   taskkill /PID 1234 /F
   ```

2. **CORS errors**
   - Check `CORS(app)` configuration
   - Verify frontend URL matches allowed origins

3. **Template not found**
   - Verify `.txt` file in `prompt_templates/` directory
   - Check file permissions
   - Restart Flask application

4. **Performance issues**
   - Enable caching
   - Increase worker count
   - Check agent execution time
   - Monitor database queries

## Production Checklist

- [ ] Disable debug mode
- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure HTTPS/SSL
- [ ] Set up database backend
- [ ] Configure logging to files
- [ ] Implement rate limiting
- [ ] Set up monitoring/metrics
- [ ] Configure backups
- [ ] Test load handling
- [ ] Document configuration
- [ ] Plan disaster recovery
