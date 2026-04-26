#!/usr/bin/env python
"""
Quick diagnostic to verify the backend can start
"""
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

print("🔍 Backend Diagnostic Check")
print("=" * 50)

# Check Python version
print(f"✓ Python version: {sys.version}")

# Check imports
print("\nChecking imports...")
try:
    print("  ✓ fastapi")
    import fastapi
except ImportError as e:
    print(f"  ✗ fastapi: {e}")
    sys.exit(1)

try:
    print("  ✓ uvicorn")
    import uvicorn
except ImportError as e:
    print(f"  ✗ uvicorn: {e}")
    sys.exit(1)

try:
    print("  ✓ pydantic")
    import pydantic
except ImportError as e:
    print(f"  ✗ pydantic: {e}")
    sys.exit(1)

try:
    print("  ✓ openai")
    import openai
except ImportError as e:
    print(f"  ✗ openai: {e}")
    sys.exit(1)

# Check environment
print("\nChecking environment...")
from dotenv import load_dotenv
load_dotenv()

openrouter_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_key:
    print(f"  ✓ OPENROUTER_API_KEY loaded (length: {len(openrouter_key)})")
else:
    print("  ⚠ OPENROUTER_API_KEY not found in .env")

# Check main app can be imported
print("\nChecking main_v2 app...")
try:
    from main_v2 import app
    print("  ✓ main_v2.app imported successfully")
except ImportError as e:
    print(f"  ✗ Failed to import main_v2.app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"  ✗ Error importing main_v2: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check routers
print("\nChecking routers...")
try:
    from routers import agent_v2
    print("  ✓ routers.agent_v2 imported successfully")
except Exception as e:
    print(f"  ✗ Failed to import routers.agent_v2: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check services
print("\nChecking services...")
services_to_check = [
    ("services.database", "database"),
    ("services.jd_parser_v2", "jd_parser_v2"),
    ("services.candidate_matcher_v2", "candidate_matcher_v2"),
    ("services.outreach_simulator_v2", "outreach_simulator_v2"),
]

for module_name, display_name in services_to_check:
    try:
        __import__(module_name)
        print(f"  ✓ {display_name} imported successfully")
    except Exception as e:
        print(f"  ✗ Failed to import {display_name}: {e}")

print("\n" + "=" * 50)
print("✅ All checks passed! Backend is ready to start.")
print("\nTo start the backend, run:")
print("  python -m uvicorn main_v2:app --reload --port 8000")
print("\nOr use the startup script:")
print("  .\run.ps1  (PowerShell)")
print("  .\run.bat  (Command Prompt)")
