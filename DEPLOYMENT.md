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

## 3. Verified Cloud Hosting Providers

### Option A: Render.com (Recommended Free Cloud Hosting)
1. Go to [https://dashboard.render.com/web/new](https://dashboard.render.com/web/new)
2. Connect your GitHub repository: `https://github.com/niteeshk-2009/HackVerse-PS01`
3. Configure settings:
   - **Name**: `spider-sense`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Plan**: `Free`
4. Click **Create Web Service**.
5. Render deploys your app with an automatic public HTTPS URL:
   `https://spider-sense.onrender.com` (or your custom service name).

### Option B: Railway.app / Koyeb
1. Connect repository `https://github.com/niteeshk-2009/HackVerse-PS01`.
2. Railway detects the `Procfile` / `Dockerfile` automatically.
3. Generates a public HTTPS URL: `https://hackverse-ps01.up.railway.app`.

### Option C: Instant Standalone Deployment (GitHub Pages)
- **Live URL**: [https://niteeshk-2009.github.io/HackVerse-PS01/](https://niteeshk-2009.github.io/HackVerse-PS01/)
- Pre-compiled full-state client simulation for all 20 equities (14 Indian + 6 Foreign), 4-agent synthesis, and live chart streams.

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
