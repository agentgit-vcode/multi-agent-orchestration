# Quick Start Guide - Web Interface

## 📋 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python run_web_interface.py
```
Or:
```bash
python web_app.py
```

### Step 3: Open in Browser
```
http://localhost:5000
```

That's it! ✅

---

## 🎯 Using the Web Interface

### Submit a Simple Question
1. Type your question in the text area
2. Click "Submit Question"
3. View results below

### Use a Prompt Template
1. Type your question
2. Select a template from the dropdown (or templates list on the right)
3. Preview will appear
4. Click "Submit Question"
5. Results will show with enhanced formatting from the template

### Create Custom Templates
1. Create a `.txt` file in the `prompt_templates/` folder
2. Add content like:
   ```
   Please analyze: {question}
   
   Provide:
   1. Summary
   2. Details
   3. Recommendations
   ```
3. Refresh your browser
4. Your template appears in the list

---

## 📁 What Gets Created

| File | Purpose |
|------|---------|
| `web_app.py` | Main web server |
| `prompt_manager.py` | Template management |
| `templates/index.html` | Web interface UI |
| `prompt_templates/` | Your templates |

---

## 🔧 Common Tasks

### Change Port
Edit `web_app.py`, last line:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### Share on Network
Edit `web_app.py`, last line:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Already does this!
```

### Use Without Template
Just leave the template dropdown empty and submit.

---

## 📊 API Quick Reference

```bash
# Get available templates
curl http://localhost:5000/api/templates

# Submit a question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Your question here",
    "template": "comprehensive_plan.txt"
  }'

# Get task result
curl http://localhost:5000/api/task/task-id-here
```

---

## 📚 Documentation

- **WEB_INTERFACE_GUIDE.md** - Detailed user guide
- **CONFIGURATION_GUIDE.md** - Advanced configuration
- **IMPLEMENTATION_SUMMARY.md** - Technical overview
- **api_client_examples.py** - Code examples

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't access http://localhost:5000 | Ensure `python web_app.py` is running |
| Port 5000 in use | Change port in `web_app.py` |
| No templates showing | Create `.txt` files in `prompt_templates/` folder |
| Agent errors | Check Flask console output for details |

---

## 🚀 Next Steps

1. ✅ Web interface working? Great!
2. Create your first custom template
3. Submit a question with a template
4. Explore the API endpoints
5. Read CONFIGURATION_GUIDE.md for advanced setup

---

## 💡 Example Template

Save as `prompt_templates/my_template.txt`:

```
I need your help with this: {question}

Please provide:
1. Quick answer
2. Why this matters
3. How to apply it
4. Resources to learn more
```

Then use it in the web interface!

---

## 📞 Need Help?

1. Check documentation files
2. Review error messages in Flask console
3. Look at `api_client_examples.py` for code examples
4. Verify all dependencies: `pip list`

---

**You're all set! Start asking questions! 🤖**
