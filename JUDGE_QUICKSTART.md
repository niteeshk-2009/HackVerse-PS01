# SPIDER SENSE 🕷️ — Judge Quickstart Guide

> **HackVerse: Into the Web (Sprint 1 — Web-Slinger Sprint / Rapid Vibe Coding)**  
> **Problem Statement PS-01**: Multi-Agent Autonomous Financial Intelligence System for Retail Investors  
> **Repository**: [https://github.com/niteeshk-2009/HackVerse-PS01](https://github.com/niteeshk-2009/HackVerse-PS01)  
> **Public Deployment**: N/A *(Sprint 1 deployment is optional per HackVerse Handbook; runs locally in 2 commands)*  
> **Reading Time**: ~2 minutes

---

## 1. Project Purpose & Problem Context

### What PS-01 Asks For
PS-01 requires building an autonomous multi-agent financial intelligence system for retail investors that:
- Evaluates market signals across $\ge 3$ independent dimensions with stated confidence.
- Grounds recommendations in a document corpus via RAG with verifiable source attribution.
- Executes $\ge 3$ specialized agents in parallel, synthesized by an orchestration layer.
- Modifies outputs demonstrably based on stored user risk parameters.
- Operates gracefully in degraded-data scenarios without hallucination.

### What SPIDER SENSE Implements
SPIDER SENSE is a full-stack, single-service fintech intelligence platform (Python FastAPI backend + responsive vanilla JS/Tailwind cockpit) running **4 specialized agents concurrently**, an **in-memory TF-IDF semantic RAG engine** over authentic SEBI LODR & SEC Form 10-Q/K regulatory filings, **mathematical portfolio concentration (HHI)** risk modeling, and a **cross-agent conflict arbiter**.

### Value to an Indian Retail Investor
SEBI's official 2024 study confirms that **89% of individual retail derivative (F&O) participants lose money**, incurring aggregate annual net losses exceeding ₹52,000 Crores. Retail traders suffer from a structural **intelligence asymmetry**: while institutional hedge funds run multi-analyst desks cross-referencing technicals, filings, and institutional order flow, retail traders rely on raw price charts and speculative social media tips. SPIDER SENSE bridges this divide by delivering institutional-grade, evidence-grounded multi-agent intelligence tailored to each investor's risk profile.

---

## 2. Multi-Agent Architecture Overview

The system deploys **4 specialized analytical agents** executed concurrently via Python's `ThreadPoolExecutor(max_workers=4)`, synthesized by **The Spider Mind Orchestrator**:

| Agent | Source File | Specialized Responsibility | Structured Contract Output |
|---|---|---|---|
| **Market Spider** | `agents/market_spider.py` | Technicals across 3 independent dimensions: Price Momentum (EMA cluster), Volume Anomaly (surge multiplier), and Oscillators (RSI-14). | Score, confidence, 3 dimensional signal objects with causal reasoning. |
| **Fundamental Web** | `agents/fundamental_web.py` | Semantic vector RAG retrieval over authentic SEBI LODR corporate filings & SEC Form 10-Q disclosures. | Valuation assessment, balance sheet health, verifiable evidence citations with exact page/section quotes. |
| **Sentiment Spider** | `agents/sentiment_spider.py` | Order flow forensics: Institutional FII net flow vs Retail FOMO option chasing. | Sentiment score, smart money bias, crowd behavior warnings. |
| **Risk Guardian** | `agents/risk_guardian.py` | Portfolio concentration risk via Herfindahl-Hirschman Index (HHI) and position suitability. | Concentration score, allocation headroom %, risk warnings. |
| **The Spider Mind** | `agents/web_mind.py` | **Master Synthesis & Conflict Arbiter**: Dispatches agents in parallel, detects contradictions (e.g. price breakout vs institutional distribution), enforces stop-loss safeguards, and personalizes advice. | Master verdict (SIP / Swing / Wait), answers to 5 core investor questions, conflict log, telemetry. |

---

## 3. Local Setup & Execution (60 Seconds)

### Prerequisites
- Python 3.11+ (Python 3.11 to 3.13 tested)
- Git

### Run Commands
```bash
# 1. Clone the repository
git clone https://github.com/niteeshk-2009/HackVerse-PS01.git
cd HackVerse-PS01

# 2. Install dependencies (minimal: fastapi, uvicorn, pydantic)
pip install -r requirements.txt

# 3. Start the application server
python run.py
```
- Open in your browser: **`http://localhost:8000`** *(Local development only)*
- Interactive Swagger API Docs: **`http://localhost:8000/docs`**

---

## 4. Recommended 2-Minute Judge Evaluation Flow

Follow this sequence in the running application to observe all PS-01 requirements in action:

1. **Start Application & View Cockpit**:
   - Open `http://localhost:8000`. You will see the **SPIDER SENSE** fintech cockpit with a live continuous tick stream and real-time EMA overlay.
2. **Select an Equity**:
   - In the top ticker carousel, click **`TATAMOTORS`** (or search any of the 20 Indian & US equities).
3. **Inspect the 4 Specialist Agents**:
   - Scroll to the **Specialist Agents** grid: Observe all 4 independent cards (*Market Spider*, *Fundamental Web*, *Sentiment Spider*, *Risk Guardian*) with live signal scores, confidence meters, and individual reasoning.
4. **Inspect RAG Evidence Attribution**:
   - In the **Master Synthesis** card and the **Fundamental Web** panel, inspect the **Evidence Chain**: Notice the exact corporate filing title (e.g. `Tata Motors Ltd - Q2 FY26 Investor Presentation`), section provenance, cosine match %, and verbatim excerpt.
5. **Inspect Personalization Divergence (High-Value PS-01 Requirement)**:
   - Notice the current profile: **Conservative Investor**. The master recommendation is **`GRADUAL STAGGERED ACCUMULATION (SIP)`** with a strict 5% sector cap to protect cash.
   - Click the **Profile Chip** in the top right header, and switch to **Aggressive Trader**.
   - Observe the output change immediately: The recommendation switches to **`MOMENTUM SWING ACCUMULATION`** with a 2.0% trailing stop-loss, reflecting higher risk tolerance on identical market data.
6. **Inspect Cross-Market Comparison**:
   - Click the **"Compare 2 Stocks"** tab. Select Stock A (`TATAMOTORS`) and Stock B (`TSLA`) to observe side-by-side multi-agent evaluation.
7. **Test Degraded-Data & Anti-Hallucination Safe Mode**:
   - Click the **"Stress Testing"** tab.
   - Click **"Missing Filing"**: Fundamental Web reports `DATA_UNAVAILABLE`, confidence drops below 60%, and Spider Mind switches verdict to `SAFEGUARD WAIT` rather than hallucinating figures.
   - Click **"Conflict Scenario"**: Injects a retail trap (bullish technicals vs institutional distribution); Spider Mind identifies the divergence, discounts momentum by 40%, and enforces stop-loss bounds.
8. **Run Automated Test Suite**:
   ```bash
   python -m tests.test_system
   python -m tests.test_end_to_end
   ```
   All 14 tests pass with exit code 0.

---

## 5. Observable PS-01 Verification Matrix

| Evaluation Dimension | Concrete Implementation File | UI Location in Dashboard | Automated Test |
|---|---|---|---|
| **$\ge 3$ Signal Dimensions** | `agents/market_spider.py` | Market Spider Card (Pills for Momentum, Volume, Oscillators) | `test_system.py::test_signal_classification_three_dimensions` |
| **Evidence Grounding (RAG)** | `rag/engine.py`, `rag/corpus.py` | Master Synthesis Evidence Chain & Fundamental Web Card | `test_system.py::test_rag_semantic_retrieval_and_citations` |
| **Parallel Specialized Agents** | `agents/web_mind.py` (`ThreadPoolExecutor`) | 4-Agent Cockpit Grid | `test_system.py::test_agent_structured_output_contract`, `test_parallel_orchestration_speed` |
| **Personalization Divergence** | `profiler/profiles.py`, `agents/risk_guardian.py` | Profile Switcher & Tailored Personalization Note | `test_system.py::test_user_profile_personalization_divergence` |
| **Conflict Resolution** | `agents/web_mind.py` (`_detect_conflicts`) | Conflict Alert Banner in Master Synthesis | `test_system.py::test_agent_conflict_detection_and_resolution` |
| **Portfolio Risk & HHI** | `profiler/profiles.py` (`calculate_hhi`) | Risk Guardian Card & Telemetry Drawer | `test_system.py::test_portfolio_concentration_hhi`, `test_hhi_edge_cases` |
| **Degraded-Data Safety** | `market_data/provider.py`, `agents/base.py` | Stress Testing Tab | `test_system.py::test_degraded_data_handling_missing_filing`, `test_stale_data_handling` |
| **Explainability (5 Questions)** | `agents/web_mind.py` | 5 Accordion Cards in Master Synthesis | `test_system.py::test_five_questions_completeness` |
| **Measurable Telemetry** | `telemetry/logger.py` (`telemetry_sessions.db`)| Latency Badge & Telemetry API (`/api/telemetry`) | `test_end_to_end.py` |

---

## 6. Detailed Technical Documentation

For in-depth technical audits and design rationale, please reference:
- **[REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md)** — Comprehensive line-by-line requirement-to-file traceability matrix.
- **[REQUIREMENTS.md](REQUIREMENTS.md)** — Core PS-01 requirements verification status.
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — Complete system topology, execution flow, and data pipelines.
- **[AGENTS.md](AGENTS.md)** — Formal Pydantic schemas and structured contracts for all 4 agents.
- **[RAG.md](RAG.md)** — In-memory TF-IDF semantic vector retrieval, indexing, and anti-hallucination mechanics.
- **[DATA_SOURCES.md](DATA_SOURCES.md)** — 3-state data policy (`LIVE`, `DEMO`, `DATA UNAVAILABLE`) and equity universe.
- **[DECISIONS.md](DECISIONS.md)** — Engineering decisions and architectural trade-offs.
- **[TESTING.md](TESTING.md)** — Test suite architecture and execution guide.
- **[DEMO.md](DEMO.md)** — Step-by-step presentation walkthrough.
- **[FINAL_AUDIT.md](FINAL_AUDIT.md)** — 35-point technical release gate audit report.
