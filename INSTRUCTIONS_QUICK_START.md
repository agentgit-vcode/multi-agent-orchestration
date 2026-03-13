# Quick Guide: Agent Instructions Connected to LLM ✅

## **What Happened**

Your agent instructions **are now sent to the LLM as system prompts**! Each agent reads from `agent_instructions/` folder.

---

## **The Files**

| File | Purpose |
|------|---------|
| `agent_instructions/planner.txt` | Instructions for planning queries |
| `agent_instructions/researcher.txt` | Instructions for research |
| `agent_instructions/analyzer.txt` | Instructions for analysis |
| `agent_instructions/publisher.txt` | Instructions for final reports |

---

## **How to Use**

### **1. Start Flask**
```cmd
python run_web_interface.py
```

### **2. Test a Question**
Go to http://localhost:5000
```
Ask: "How should we implement AI?"
```

### **3. See Structured Output**
Output follows your instructions:
```
TASK_DECOMPOSITION
- Task 1
- Task 2

MISSING_INFO
- Info needed

DECISION_CRITERIA
- Criterion 1
```

### **4. Customize Instructions**

Edit any file in `agent_instructions/`:
- Change text
- Add new sections
- Modify rules

**Changes take effect immediately!**

---

## **Example: Make It More Detailed**

Edit `agent_instructions/planner.txt`:

**Change:**
```
"- List 5-8 concrete sub-tasks"
```

**To:**
```
"- List 10-15 detailed sub-tasks with descriptions"
```

Ask a question → Get more detailed plans!

---

## **For Your Use Case**

### **Healthcare**
Edit analyzer.txt, add:
```
REGULATORY_COMPLIANCE
- FDA requirements
- HIPAA rules
- Clinical standards
```

### **Finance**
Edit publisher.txt, add:
```
FINANCIAL_IMPACT
- ROI calculations
- Cost-benefit analysis
- Payback period
```

### **Startup**
Edit planner.txt, change:
```
Focus on MVP criteria first
Nice-to-haves secondary
```

---

## **Verify It's Working**

When you ask a question, Flask logs show:
```
PlannerAgent using OpenAI LLM with custom instructions ✓
ResearcherAgent using OpenAI LLM with custom instructions ✓
AnalyzerAgent using OpenAI LLM with custom instructions ✓
PublisherAgent using OpenAI LLM with custom instructions ✓
```

---

## **Key Points**

✅ No code changes needed - just edit text files
✅ Changes immediate - no server restart
✅ Structured output - guaranteed format
✅ Fallback to defaults if file missing
✅ All instructions cached for performance

---

## **Files Changed**

| File | What Changed |
|------|--------------|
| `planner_agent.py` | Now loads planner.txt |
| `researcher_agent.py` | Now loads researcher.txt |
| `analyzer_agent.py` | Now loads analyzer.txt |
| `publisher_agent.py` | Now loads publisher.txt |
| `agent_instructions_manager.py` | NEW - Manages instructions |
| `agent_instructions/*.txt` | NEW - Instruction files |

---

## **Next: Read Full Guide**

For advanced customization, read: **AGENT_INSTRUCTIONS_GUIDE.md**

---

**Your agents now follow YOUR instructions! 🚀**
