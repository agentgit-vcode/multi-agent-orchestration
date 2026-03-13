#!/usr/bin/env python
"""
Quick start script to run the web interface for the multi-agent orchestration system.
This script sets up the environment and starts the Flask web app.
"""

import sys
import os
import subprocess
import platform


def check_dependencies():
    """Check if required packages are installed."""
    required = ['flask', 'flask_cors']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print(f"\nInstall them using:")
        print(f"   pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Main entry point."""
    print("=" * 60)
    print("🤖 Multi-Agent Orchestration Web Interface")
    print("=" * 60)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✓ All dependencies found!")
    
    # Create necessary directories
    print("\n📁 Setting up directories...")
    os.makedirs('prompt_templates', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    print("✓ Directories ready!")
    
    # Start the Flask app
    print("\n🚀 Starting web application...")
    print("-" * 60)
    print("Web Interface: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("-" * 60)
    print()
    
    try:
        # Import and run the Flask app
        from web_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing web_app: {e}")
        print("Make sure web_app.py is in the current directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Web interface stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting web application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
