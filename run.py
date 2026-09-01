"""
SPIDER-SENSE: One-Click Launch Script
Launches the FastAPI server with live dashboard and REST APIs on http://localhost:8000
"""

import uvicorn
import os
import sys

# Add directory and parent directory to sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
sys.path.insert(0, _parent_dir)
sys.path.insert(0, _current_dir)

if __name__ == "__main__":
    print("==================================================================")
    print("  SPY THE MARKET: AI-Powered Financial Intelligence Platform")
    print("  IEEE RAS VIT Chennai - HackVerse: Sprint 1 (PS-01)")
    print("==================================================================")
    print("  * Dashboard & Terminal UI: http://localhost:8000")
    print("  * Interactive API Docs:   http://localhost:8000/docs")
    print("  * 4 Specialized Agents:   Market Spider, Fundamental Web,")
    print("                            Sentiment Spider, Risk Guardian")
    print("  * Synthesis Layer:        The Spider Mind Orchestrator")
    print("==================================================================")
    uvicorn.run("spidersense.app.main:app", host="0.0.0.0", port=8000, reload=False)
