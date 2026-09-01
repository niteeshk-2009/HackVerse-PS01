# SPIDER SENSE — Production Deployment Guide

## 1. Overview & Hosting Architecture
**SPIDER SENSE** is engineered as a unified, high-performance single-service platform:
- **Backend / API**: FastAPI ASGI application serving RESTful routes (`/api/quote`, `/api/chart`, `/api/analyze`, `/api/compare`, `/api/evidence`, `/api/telemetry`, `/api/health`).
- **Frontend Cockpit**: Modern single-page fintech dashboard (Peter Parker Dark Mode / Gwen Stacy Light Mode, Chart.js live moving ticks, 4-agent parallel inspection panels, dual stock comparison engine).
- **Execution Architecture**: Frontend is served directly by the FastAPI backend at the root path (`/`), ensuring **zero cross-origin CORS latency**, same-origin relative API paths, and a unified single-port deployment.

---

## 2. Production Specifications
- **Runtime**: Python 3.11+
- **Binding**: `0.0.0.0`
- **Dynamic Port**: Binds dynamically to `os.environ.get("PORT", 8000)`
- **Start Command**: `python run.py` or `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Process Definition**: Declared in `Procfile` and `render.yaml`
- **Container Definition**: Declared in `Dockerfile`

---

> **Sprint 1 Submission Note**: In accordance with the HackVerse Handbook, public cloud deployment is **optional** for Sprint 1. The official submission entry for deployment is **N/A**. This guide documents the production architecture and one-click cloud deployment specifications.

---

## 3. Production Cloud Hosting Options

### Option A: Render.com
1. Connect repository: `https://github.com/niteeshk-2009/HackVerse-PS01`
2. Render detects `render.yaml` or `Procfile` automatically:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
3. Deploys with automatic TLS/HTTPS.

### Option B: Railway.app / Koyeb / Docker
1. Connect repository `https://github.com/niteeshk-2009/HackVerse-PS01`.
2. Automatically detects `Dockerfile` or `Procfile`.
3. Binds dynamically to container `$PORT`.

---

## 4. Environment Variables
No secrets are required to run SPIDER SENSE. In default DEMO mode, all 20 equities and SEC/SEBI corporate filings run truthfully without paid external API keys:

| Variable | Requirement | Default | Description |
|---|---|---|---|
| `HOST` | Optional | `0.0.0.0` | Host IP interface to bind |
| `PORT` | Optional | `8000` | Port provided by cloud host (Render, Railway, etc.) |
| `DATA_MODE` | Optional | `DEMO` | Operational data state (`DEMO` or `LIVE`) |
| `DATABASE_PATH` | Optional | `telemetry_sessions.db` | Local SQLite session metrics storage |

---

## 5. Health Check Verification
Verify production deployment health:
```bash
curl -f https://<YOUR-DEPLOYED-URL>/api/health
```
Expected Response (HTTP 200):
```json
{
  "status": "healthy",
  "product": "SPIDER SENSE",
  "subtitle": "AI-Powered Financial Intelligence",
  "system": "Multi-Agent Synthesis Engine",
  "agents_active": 4,
  "rag_status": "READY",
  "data_mode": "DEMO",
  "data_state": "DEMO_DATA"
}
```
