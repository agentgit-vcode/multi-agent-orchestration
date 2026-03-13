#!/usr/bin/env python
"""
Verification script to check if LLM integration is working
Run this to diagnose any issues before starting Flask
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n📋 Checking .env file...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("  ❌ .env file not found")
        print("  ℹ️  Create .env file with:")
        print("     OPENAI_API_KEY=sk-your-key-here")
        print("     OPENAI_MODEL=gpt-3.5-turbo")
        print("     OPENAI_TEMPERATURE=0.7")
        return False
    
    print("  ✅ .env file exists")
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=sk-' in content:
            print("  ✅ OPENAI_API_KEY is configured")
            return True
        else:
            print("  ❌ OPENAI_API_KEY not properly configured")
            print("  ℹ️  Set it to: sk-your-actual-key-from-openai")
            return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'openai': 'OpenAI',
        'dotenv': 'python-dotenv'
    }
    
    all_ok = True
    for import_name, package_name in required.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} not installed")
            all_ok = False
    
    if not all_ok:
        print("\n  ℹ️  Install missing dependencies:")
        print("     python -m pip install -r requirements.txt")
    
    return all_ok

def check_llm_handler():
    """Check if LLM handler can be imported and initialized"""
    print("\n🤖 Checking LLM Handler...")
    
    try:
        from llm_handler import is_llm_available, get_llm_handler
        
        if is_llm_available():
            print("  ✅ LLM is available and configured")
            try:
                llm = get_llm_handler()
                print("  ✅ LLM handler initialized successfully")
                return True
            except Exception as e:
                print(f"  ❌ Error initializing LLM: {e}")
                return False
        else:
            print("  ❌ LLM not available - check OPENAI_API_KEY in .env")
            return False
    except ImportError as e:
        print(f"  ❌ Cannot import LLM handler: {e}")
        return False

def check_agents():
    """Check if all agent files exist"""
    print("\n👥 Checking agents...")
    
    agents = [
        'planner_agent.py',
        'researcher_agent.py',
        'analyzer_agent.py',
        'publisher_agent.py'
    ]
    
    all_ok = True
    for agent in agents:
        if Path(agent).exists():
            print(f"  ✅ {agent}")
        else:
            print(f"  ❌ {agent} not found")
            all_ok = False
    
    return all_ok

def check_instructions():
    """Check if agent instruction files exist"""
    print("\n📝 Checking agent instructions...")
    
    instructions_dir = Path('agent_instructions')
    instructions = [
        'planner.txt',
        'researcher.txt',
        'analyzer.txt',
        'publisher.txt'
    ]
    
    if not instructions_dir.exists():
        print(f"  ❌ {instructions_dir} directory not found")
        return False
    
    print(f"  ✅ {instructions_dir} directory exists")
    
    all_ok = True
    for instruction in instructions:
        path = instructions_dir / instruction
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {instruction} ({size} bytes)")
        else:
            print(f"  ❌ {instruction} not found")
            all_ok = False
    
    return all_ok

def main():
    """Run all checks"""
    print("=" * 60)
    print("🔍 Multi-Agent Orchestration - Verification Check")
    print("=" * 60)
    
    results = {
        '.env file': check_env_file(),
        'Dependencies': check_dependencies(),
        'Agents': check_agents(),
        'Instructions': check_instructions(),
        'LLM Handler': check_llm_handler(),
    }
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_ok = True
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check:.<40} {status}")
        if not result:
            all_ok = False
    
    print("=" * 60)
    
    if all_ok:
        print("\n✅ All checks passed! Ready to run:")
        print("   python run_web_interface.py")
        print("\n   Then visit: http://localhost:5000")
    else:
        print("\n❌ Some checks failed. See details above.")
        print("\nQuick fixes:")
        print("1. Create .env with OPENAI_API_KEY=sk-your-key")
        print("2. Run: python -m pip install -r requirements.txt")
        print("3. Check: python verify_setup.py (again)")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
