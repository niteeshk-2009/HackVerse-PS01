"""
SPIDER SENSE: Production & Local Launch Script
Launches the FastAPI server with live dashboard and REST APIs.
"""

import os
import sys
import uvicorn

# Add current directory and parent directory to sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

try:
    from spidersense.app.main import app
except ImportError:
    from app.main import app

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    print("==================================================================")
    print("  SPIDER SENSE: AI-Powered Financial Intelligence Platform")
    print("  IEEE RAS VIT Chennai - HackVerse: Sprint 1 (PS-01)")
    print(f"  * Production Server listening on: http://{host}:{port}")
    print(f"  * Interactive API Docs:          http://{host}:{port}/docs")
    print("==================================================================")
    uvicorn.run(app, host=host, port=port, reload=False)
