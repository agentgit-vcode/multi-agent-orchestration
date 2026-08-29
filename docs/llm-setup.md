# OpenAI LLM Integration Setup

Your multi-agent system is now integrated with OpenAI's GPT models! 🚀

## **Quick Setup (5 minutes)**

### **Step 1: Get Your API Key**

1. Go to https://platform.openai.com/api-keys
2. Sign up or login to your OpenAI account
3. Click **"Create new secret key"**
4. Copy the key (it starts with `sk-`)

**⚠️ SECURITY**: Never share your API key! It costs real money!

### **Step 2: Create `.env` File**

In your project folder, create a file named `.env` with:

```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
```

**IMPORTANT**: 
- Replace `sk-your-key-here` with your actual key
- Add `.env` to `.gitignore` (never commit it!)
- `.env` is already in `.gitignore` - don't remove it!

### **Step 3: Install Dependencies**

```cmd
python -m pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `python-dotenv` - Load environment variables

### **Step 4: Restart Flask**

Stop Flask (Ctrl+C) and restart:

```cmd
python run_web_interface.py
```

You should see in the logs:
```
PlannerAgent using OpenAI LLM
ResearcherAgent using OpenAI LLM
AnalyzerAgent using OpenAI LLM
PublisherAgent using OpenAI LLM
```

### **Step 5: Test It**

1. Go to http://localhost:5000
2. Ask a question
3. Watch real LLM responses appear! 🤖

---

## **How It Works**

### **Agent Pipeline with LLM**

```
User Question
    ↓
PlannerAgent (GPT) → Creates detailed plan
    ↓
ResearcherAgent (GPT) → Gathers research data
    ↓
AnalyzerAgent (GPT) → Analyzes findings
    ↓
PublisherAgent (GPT) → Creates final report
    ↓
Result to User
```

Each agent makes **real LLM calls** using the `llm_handler.py` module.

---

## **Configuration**

### **Change Model**

Edit `.env`:
```
OPENAI_MODEL=gpt-4  # For better quality (more expensive)
OPENAI_MODEL=gpt-3.5-turbo  # Default (cheaper and fast)
```

### **Adjust Response Quality**

Temperature controls creativity (0.0 = factual, 1.0 = creative):
```
OPENAI_TEMPERATURE=0.3  # More deterministic
OPENAI_TEMPERATURE=0.9  # More creative
```

### **Token Limits**

Edit `llm_handler.py` to change max_tokens in each function:
```python
def plan(self, query: str) -> str:
    return self.call(prompt, system_prompt, max_tokens=2000)  # Change here
```

---

## **Costs**

### **Pricing (as of 2024)**

| Model | Input | Output |
|-------|-------|--------|
| GPT-3.5-turbo | $0.5/1M tokens | $1.5/1M tokens |
| GPT-4 | $30/1M tokens | $60/1M tokens |

### **Estimate for Your Use**

One multi-agent request = ~500-2000 tokens

- **100 requests**: ~$0.10-0.50
- **1000 requests**: ~$1.00-5.00
- **10000 requests**: ~$10-50

**GPT-3.5-turbo is recommended** - great quality at low cost!

---

## **Troubleshooting**

### **"OPENAI_API_KEY not found"**

✅ **Solution**: Create `.env` file in your project folder with your key

### **"Error calling LLM"**

Check:
1. Is your API key valid? https://platform.openai.com/api-keys
2. Does your account have usage credits? (not free credits)
3. Check the error message in Flask console for details

### **"Module 'openai' not found"**

✅ **Solution**:
```cmd
python -m pip install openai
```

### **No LLM responses (still using mock)**

This means:
- ✅ Your agents still work (they fallback to mock responses)
- ❌ Your API key or `.env` file is wrong

Check:
1. Is `.env` file in the right folder?
2. Is the key format correct? (starts with `sk-`)
3. Is there a typo in `OPENAI_API_KEY=`?

---

## **Files Changed**

| File | Change |
|------|--------|
| `llm_handler.py` | **NEW** - Handles all LLM calls |
| `planner_agent.py` | Updated to use LLM |
| `researcher_agent.py` | Updated to use LLM |
| `analyzer_agent.py` | Updated to use LLM |
| `publisher_agent.py` | Updated to use LLM |
| `requirements.txt` | Added openai & python-dotenv |
| `.env.example` | **NEW** - Template for .env |
| `.env` | **YOUR FILE** - Keep secret! |

---

## **Testing**

### **Test LLM Connection**

Run this in Python:

```python
from llm_handler import is_llm_available, get_llm_handler

if is_llm_available():
    llm = get_llm_handler()
    response = llm.call("What is AI?")
    print(response)
else:
    print("LLM not available - check .env file")
```

### **Test Individual Agents**

```bash
python -c "from llm_handler import is_llm_available; print('LLM Available' if is_llm_available() else 'LLM Not Available')"
```

---

## **Disable LLM (Use Mock Responses)**

If you want to test without spending money:

1. Delete or rename your `.env` file
2. Or remove the `OPENAI_API_KEY` line
3. Agents will automatically fall back to mock responses
4. Everything still works!

---

## **Next Steps**

1. ✅ Set up `.env` file with your API key
2. ✅ Install dependencies: `python -m pip install -r requirements.txt`
3. ✅ Restart Flask: `python run_web_interface.py`
4. ✅ Test at http://localhost:5000
5. ✅ Ask questions and get real LLM responses!

---

## **Questions?**

Check:
- `llm_handler.py` - See how it works
- `planner_agent.py` - Example of LLM integration in agent
- OpenAI docs: https://platform.openai.com/docs/

---

**Your multi-agent system now has real AI! 🤖🚀**
