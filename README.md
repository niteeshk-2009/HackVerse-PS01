# SPIDER SENSE 🕷️
### AI-Powered Multi-Agent Financial Intelligence for Retail Investors

> *"See the signal. Understand the why. Grounded in evidence."*

Built for **HackVerse: Into the Web (Sprint 1 — Web-Slinger Sprint / Rapid Vibe Coding)**  
**Problem Statement PS-01** · Organized by IEEE Robotics & Automation Society (IEEE RAS), VIT Chennai · TechnoVIT 2026.  

**Official Repository**: [https://github.com/niteeshk-2009/HackVerse-PS01](https://github.com/niteeshk-2009/HackVerse-PS01)  
**Public Deployment**: N/A  
*The Sprint 1 submission does not include a public application deployment. The application can be run locally using the documented setup instructions below.*  
**Judge Quickstart**: 📖 **[Read the 2-Minute JUDGE_QUICKSTART.md Guide](JUDGE_QUICKSTART.md)**

---

## 1. PS-01 Requirement Coverage

The table below maps every non-negotiable PS-01 requirement directly to the concrete source files, verification tests, and UI locations in this repository. Complete line-by-line traceability is available in **[REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md)**.

| PS-01 Requirement | Concrete Implementation | Verification Test | UI Dashboard Location |
|---|---|---|---|
| **Multi-Dimensional Financial Signals** | Evaluates Price Momentum (multi-EMA), Volume Anomaly (1.61x surge), and Oscillators (RSI-14) with calibrated confidence & causal reasoning (`agents/market_spider.py`). | `tests/test_system.py` (Test 1) | Market Spider Card (3 dimensional signal pills) |
| **Specialized Multi-Agent System** | 4 distinct agents (*Market Spider*, *Fundamental Web*, *Sentiment Spider*, *Risk Guardian*) with strict Pydantic output contracts (`agents/base.py`). | `tests/test_system.py` (Test 3) | 4-Agent Inspection Grid |
| **Parallel Agent Execution** | Dispatches all 4 specialized agents concurrently via Python's `ThreadPoolExecutor(max_workers=4)` (`agents/web_mind.py`). | `tests/test_system.py` (Test 13) | Live Cockpit runtime execution |
| **Evidence-Grounded RAG** | In-memory TF-IDF semantic vector similarity engine over authentic SEBI LODR corporate filings and SEC Form 10-Q disclosures (`rag/engine.py`, `rag/corpus.py`). | `tests/test_system.py` (Test 2) | Fundamental Web Panel & Master Synthesis Evidence Chain |
| **Personalization & Profile Divergence** | Onboarding profiler and risk engine producing mathematically divergent verdicts (e.g. SIP accumulation vs Momentum Swing with stop-loss) on identical market input (`profiler/profiles.py`). | `tests/test_system.py` (Test 4) | Top-right Profile Switcher & Tailored Personalization Note |
| **Cross-Agent Conflict Resolution** | Cross-agent conflict arbiter detecting retail distribution traps (e.g. price breakout vs institutional distribution), discounting scores and enforcing safeguards (`agents/web_mind.py`). | `tests/test_system.py` (Test 5) | Conflict Alert Banner in Master Synthesis |
| **Portfolio & Risk Analysis (HHI)** | Mathematical Herfindahl-Hirschman Index calculation for portfolio concentration risk and position sizing limits (`profiler/profiles.py`). | `tests/test_system.py` (Test 7, 11) | Risk Guardian Card & Telemetry Drawer |
| **Graceful Degraded-Data Handling** | Strict 3-state data policy (`LIVE`, `DEMO`, `DATA UNAVAILABLE`); handles feed drops and missing filings without hallucination, penalizing confidence by 40% (`market_data/provider.py`). | `tests/test_system.py` (Test 6, 12) | Stress Testing Tab |
| **Explainability (5 Core Questions)** | Master synthesis provides explicit answers to: What is happening? Why? What evidence supports it? How confident? What does it mean for this investor? (`agents/web_mind.py`). | `tests/test_system.py` (Test 9) | 5 Master Synthesis Accordion Cards |
| **Session Performance Telemetry** | SQLite session persistence recording `total_pipeline_latency_ms`, `rag_retrieval_latency_ms`, `portfolio_risk_concentration`, and `signal_agreement_score_pct` (`telemetry/logger.py`). | `tests/test_end_to_end.py` | Latency Readout Badge & `/api/telemetry` |
| **Cross-Market Comparison Duel** | Head-to-head multi-agent comparison between any two equities across Indian and US markets (`app/main.py`, `static/index.html`). | `tests/test_system.py` (Test 10) | "Compare 2 Stocks" Tab |

---

## 2. Why Multi-Agent? (Beyond Single-LLM Wrappers)

Most conventional AI financial tools are **single-prompt LLM wrappers**: they pass a ticker name into a generic language model and ask for a summary. In real-world financial intelligence, this architecture fails because:
- Language models cannot reliably calculate mathematical portfolio concentration indices ($HHI = \sum w_i^2$).
- LLMs frequently hallucinate financial figures and corporate quotes when asked for citations.
- Monolithic prompts cannot disentangle technical price action from institutional order flow, leading to uncritical confirmation bias.

**SPIDER SENSE is a genuine multi-agent system** where specialized agents operate as independent analysts before synthesis:
1. **Separation of Financial Concerns**:
   - **Market Spider** performs deterministic technical analysis (multi-EMA alignment, volume anomaly detection, RSI-14 oscillators).
   - **Fundamental Web** executes semantic vector retrieval over indexed corporate regulatory disclosures (SEBI LODR, SEC 10-Q) with exact page/section provenance.
   - **Sentiment Spider** tracks institutional order flow forensics (FII net flow vs retail FOMO option chasing).
   - **Risk Guardian** acts as an independent fiduciary, mathematically evaluating portfolio concentration (HHI) and enforcing position sizing constraints regardless of market hype.
2. **True Concurrent Execution**: Agents execute in parallel via multi-threading (`ThreadPoolExecutor`), eliminating sequential bottlenecks.
3. **Structured Contracts**: Every agent outputs a strict Pydantic contract (`AgentOutput`) containing typed signals, normalized scores (-100 to +100), calibrated confidence (0–100%), evidence citations, and identified risks.
4. **Explicit Conflict Resolution**: When Market Spider detects a bullish breakout but Sentiment Spider reveals heavy institutional distribution (a classic retail trap), **The Spider Mind Orchestrator** detects the contradiction, discounts momentum, and enforces capital protection rules.

---

## 3. Architecture Overview

```
RAW FINANCIAL FEEDS (NSE / NASDAQ Equities)  +  REGULATORY CORPUS (SEBI LODR, SEC 10-Q/K)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
  [Market Spider]          [Fundamental Web]           [Sentiment Spider]
  • Price Momentum         • Semantic Vector RAG       • Institutional FII Flow
  • Volume Multiplier      • SEBI LODR Disclosures     • Retail FOMO Chasing
  • RSI-14 / Oscillators   • SEC 10-Q Financials       • Order Flow Imbalance
        │                           │                           │
        └───────────────────────────┬───────────────────────────┘
                                    ▼
                             [Risk Guardian]
                             • Portfolio Concentration (HHI)
                             • Tailored Position Sizing
                             • User Risk Suitability
                                    │
                                    ▼
                       [THE SPIDER MIND ORCHESTRATOR]
                       • Cross-Agent Conflict Arbiter
                       • Calibrated Consensus Scoring
                       • Anti-Hallucination Safe Guard
                                    │
                                    ▼
           INSPECTABLE USER INTELLIGENCE COCKPIT (HTTP 200)
           • Actionable Recommendation (SIP vs Swing vs Wait)
           • Answers to 5 Core Investor Questions
           • Exact Regulatory Citations with Page Provenance
```

---

## 4. Key Features

- **Fintech Single-Page Cockpit**: Interactive single-page dashboard with instant tab switching (Cockpit, Compare, Stress Testing).
- **Spider-Man Inspired Dual Themes**:
  - *Dark Theme (Peter Parker)*: Stealth black (`#070a12`), crimson red (`#e62429`), cyan accents (`#00d2ff`).
  - *Light Theme (Gwen Stacy)*: Paper white (`#fcfcfd`), magenta pink (`#ff2a85`), purple border (`#7c3aed`).
- **Live Continuous Moving Tick Chart**: Streaming price updates and 20 EMA strictly bounded to real-time timestamps.
- **Cross-Market Comparison Duel**: Side-by-side comparative analysis between Indian and US equities (e.g. `TATAMOTORS` vs `TSLA`).
- **Interactive Stress Testing Workbench**: Real-time simulation of signal conflicts, feed drops, and missing filings to verify anti-hallucination safe modes.
- **Telemetry Session Persistence**: Local SQLite storage recording pipeline latency, RAG latency, HHI concentration, and agreement scores.

---

## 5. Running Locally (Local Development Only)

### Prerequisites
- Python 3.11+ (Python 3.11 to 3.13 tested)
- Git

### Installation & Launch
```bash
# 1. Clone repository
git clone https://github.com/niteeshk-2009/HackVerse-PS01.git
cd HackVerse-PS01

# 2. Install dependencies (minimal: fastapi, uvicorn, pydantic)
pip install -r requirements.txt

# 3. Launch the Spider Sense application server
python run.py
```
- Open in browser: **`http://localhost:8000`** *(Local development only)*
- Interactive Swagger API Docs: **`http://localhost:8000/docs`**

---

## 6. Verification & Automated Test Results

The repository includes a comprehensive, non-negotiable acceptance and resilience test suite. Every test runs synchronously against the actual codebase:

```bash
# Run acceptance test suite (13 tests covering all PS-01 requirements)
python -m tests.test_system

# Run end-to-end multi-agent pipeline verification
python -m tests.test_end_to_end
```

### Verified Test Results (14/14 Passed, Exit Code 0):
```
tests/test_system.py:
  [PASS] Test 1: Signal classification across 3 dimensions
  [PASS] Test 2: RAG semantic retrieval & source citations
  [PASS] Test 3: Structured agent output contracts
  [PASS] Test 4: User profile divergence on identical market inputs
  [PASS] Test 5: Cross-agent conflict detection & resolution
  [PASS] Test 6: Degraded data handling without hallucination
  [PASS] Test 7: Portfolio concentration HHI risk metrics
  [PASS] Test 8: Data state validation & quality warning checks
  [PASS] Test 9: Five core questions completeness
  [PASS] Test 10: HTTP status code semantics (404, 200)
  [PASS] Test 11: Portfolio HHI calculations across 4 edge cases
  [PASS] Test 12: Stale data and feed failure handling
  [PASS] Test 13: Verified concurrent execution of all 4 agents

tests/test_end_to_end.py:
  [PASS] End-to-end multi-agent pipeline verified successfully!
```
*Continuous Integration: Automated CI execution is configured via `.github/workflows/tests.yml` running on Ubuntu with Python 3.11 on every push and pull request.*

---

## 7. Detailed Documentation Index

| Document | Purpose |
|---|---|
| **[JUDGE_QUICKSTART.md](JUDGE_QUICKSTART.md)** | **2-Minute Judge Evaluation Guide** (Purpose, architecture, evaluation steps) |
| **[REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md)** | Complete requirement-to-file traceability matrix for all PS-01 mandates |
| **[REQUIREMENTS.md](REQUIREMENTS.md)** | Core PS-01 requirements verification audit |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System topology, data flow, and design specifications |
| **[AGENTS.md](AGENTS.md)** | Formal Pydantic schemas and structured contracts for all 4 agents |
| **[RAG.md](RAG.md)** | In-memory TF-IDF semantic vector engine and anti-hallucination mechanics |
| **[DATA_SOURCES.md](DATA_SOURCES.md)** | Strict 3-state data policy and 20-equity universe specifications |
| **[DECISIONS.md](DECISIONS.md)** | Key architectural decisions and engineering trade-offs |
| **[TESTING.md](TESTING.md)** | Automated testing methodology and coverage documentation |
| **[DEMO.md](DEMO.md)** | Presentation walkthrough script for evaluators |
| **[FINAL_AUDIT.md](FINAL_AUDIT.md)** | 35-point technical release gate audit report |

---

## 8. Limitations & Financial Disclaimer

### Disclosed Limitations
1. In default `DEMO` mode, market tick data is generated deterministically to guarantee reproducible, zero-downtime evaluation during hackathon judging.
2. The RAG corpus currently covers 20 listed enterprises across Indian and US equities; expanding to the entire NSE 500 would require external vector database infrastructure.
3. Designed for low-latency interactive analysis with per-agent execution telemetry; actual roundtrip latency depends on the host machine's hardware and network environment.

### Mandatory Financial Disclaimer
*This product provides AI-generated financial intelligence for informational and educational purposes and is not financial advice. Past performance and algorithmic models do not guarantee future market returns. Always consult a SEBI-registered investment advisor before deploying capital.*
