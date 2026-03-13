# Agent Instructions Integration

Your agent instructions are now **fully integrated** into the LLM system! 🎉

## **What Changed**

### **New System**

1. **agent_instructions_manager.py** - Loads and manages agent-specific instructions
2. **agent_instructions/** folder - Contains instructions for each agent
3. **Updated all agents** - Now use system prompts from instruction files

### **Files in `agent_instructions/` folder**

- `planner.txt` - Instructions for PlannerAgent
- `researcher.txt` - Instructions for ResearcherAgent  
- `analyzer.txt` - Instructions for AnalyzerAgent
- `publisher.txt` - Instructions for PublisherAgent

---

## **How It Works**

### **Before (Old Way)**
```
User Question
    ↓
Agent uses generic system prompt
    ↓
LLM responds with generic output
```

### **After (New Way)**
```
User Question
    ↓
Agent loads SPECIFIC instructions from file
    ↓
Agent sends: [System Prompt] + [Instructions] + [User Question]
    ↓
LLM responds following YOUR specific guidance
```

---

## **What Instructions Get Sent to LLM**

Each agent now sends the LLM:

1. **System Prompt** (from `agent_instructions/{role}.txt`)
   - Defines the agent's role and behavior
   - Specifies output format
   - Provides rules and constraints

2. **User Prompt** (the query to analyze)
   - Your original question
   - Context from previous agents

**Example: PlannerAgent sends**
```
System Prompt:
"You are an expert Planner Agent...
Output: TASK_DECOMPOSITION, MISSING_INFO, DECISION_CRITERIA
Rules: Do NOT recommend an option yet..."

User Prompt:
"Please create a plan for: How should we implement AI in our company?"
```

---

## **Customizing Agent Instructions**

### **Edit Instructions**

Edit any file in `agent_instructions/` folder:

- **planner.txt** - Change how planning works
- **researcher.txt** - Change research behavior
- **analyzer.txt** - Change analysis approach
- **publisher.txt** - Change report format

### **Example: Make PlannerAgent More Detail-Oriented**

Edit `agent_instructions/planner.txt`:

```
OLD:
"- List 5-8 concrete sub-tasks"

NEW:
"- List 10-15 concrete sub-tasks with detailed descriptions"
```

**Changes take effect immediately** on next request!

---

## **Default Instructions (What's Already There)**

### **PlannerAgent**
- Breaks down queries into actionable tasks
- Identifies missing information
- Defines decision criteria
- Does NOT recommend solutions yet

### **ResearcherAgent**
- Gathers factual, well-sourced information
- Identifies current state and trends
- Provides evidence-based findings
- Cites sources when possible

### **AnalyzerAgent**
- Synthesizes research into insights
- Identifies patterns and opportunities
- Highlights risks and challenges
- Bases conclusions on evidence

### **PublisherAgent**
- Creates professional, executive-ready reports
- Provides specific recommendations
- Includes implementation roadmap
- Focuses on business impact

---

## **Testing Instructions**

### **Test 1: Run a Question**

1. Go to http://localhost:5000
2. Ask: "Should we implement a microservices architecture?"
3. Look at the response - notice how it follows the structured format from instructions

### **Test 2: Check Flask Logs**

You should see in the Flask console:
```
PlannerAgent using OpenAI LLM with custom instructions
ResearcherAgent using OpenAI LLM with custom instructions
AnalyzerAgent using OpenAI LLM with custom instructions
PublisherAgent using OpenAI LLM with custom instructions
```

### **Test 3: Modify an Instruction**

1. Edit `agent_instructions/planner.txt`
2. Change "5-8 sub-tasks" to "10-15 sub-tasks"
3. Ask another question
4. PlannerAgent now gives more detailed plans!

---

## **Advanced: Override Instructions**

### **For a Single Request**

You could modify web_app.py to accept instructions as a parameter:

```python
@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    custom_instructions = data.get('instructions')  # Optional
    # ... use custom_instructions if provided
```

### **For Different Modes**

Create different instruction files:
- `planner_detailed.txt` - For complex projects
- `planner_quick.txt` - For quick analysis
- Load based on user preference

---

## **Architecture**

```
User Question
    ↓
Web App (web_app.py)
    ↓
Orchestrator (orchestrator.py)
    ↓
PlannerAgent (planner_agent.py)
    ├─ Load instructions from agent_instructions/planner.txt
    ├─ Get LLMHandler (llm_handler.py)
    └─ Call OpenAI with: system_prompt + user_query
    ↓
ResearcherAgent (researcher_agent.py)
    ├─ Load instructions from agent_instructions/researcher.txt
    ├─ Get LLMHandler (llm_handler.py)
    └─ Call OpenAI with: system_prompt + context + query
    ↓
AnalyzerAgent (analyzer_agent.py)
    ├─ Load instructions from agent_instructions/analyzer.txt
    ├─ Get LLMHandler (llm_handler.py)
    └─ Call OpenAI with: system_prompt + all_data + query
    ↓
PublisherAgent (publisher_agent.py)
    ├─ Load instructions from agent_instructions/publisher.txt
    ├─ Get LLMHandler (llm_handler.py)
    └─ Call OpenAI with: system_prompt + full_context + query
    ↓
Final Report to User
```

---

## **Files Modified**

| File | Change |
|------|--------|
| **agent_instructions_manager.py** | NEW - Loads agent instructions |
| **planner_agent.py** | Updated - Uses custom instructions |
| **researcher_agent.py** | Updated - Uses custom instructions |
| **analyzer_agent.py** | Updated - Uses custom instructions |
| **publisher_agent.py** | Updated - Uses custom instructions |
| **agent_instructions/planner.txt** | NEW - Planner instructions |
| **agent_instructions/researcher.txt** | NEW - Researcher instructions |
| **agent_instructions/analyzer.txt** | NEW - Analyzer instructions |
| **agent_instructions/publisher.txt** | NEW - Publisher instructions |

---

## **Important Notes**

✅ **Instructions load automatically** - No code changes needed
✅ **Changes take effect immediately** - No restart required (usually)
✅ **Fallback to defaults** - If files are deleted, defaults are used
✅ **Cached for performance** - Instructions loaded once per agent
✅ **Error handling** - If file is invalid, agent falls back gracefully

---

## **Next Steps**

1. ✅ Restart Flask (if you haven't already)
2. ✅ Test with a question at http://localhost:5000
3. ✅ Read the output - notice the structured format
4. ✅ Customize instructions as needed
5. ✅ Ask more questions with different topics

---

## **Example Custom Instructions**

### **For Medical Analysis**
Edit `agent_instructions/analyzer.txt`:
```
Add: "Consider medical regulations (HIPAA, FDA, etc.)"
Add: "Assess patient safety implications"
Add: "Include clinical evidence standards"
```

### **For Product Development**
Edit `agent_instructions/publisher.txt`:
```
Add: "Include user impact assessment"
Add: "Specify ROI calculations"
Add: "Timeline for go-to-market"
```

### **For Financial Decisions**
Edit `agent_instructions/researcher.txt`:
```
Add: "Include financial models and metrics"
Add: "Compare with industry benchmarks"
Add: "Source regulatory requirements"
```

---

**Your agents now follow YOUR specific instructions! 🚀**

Test it out and watch how the responses change based on your guidance.
