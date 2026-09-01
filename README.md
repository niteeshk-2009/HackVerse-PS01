# SPIDER SENSE 🕷️
### AI-Powered Multi-Agent Financial Intelligence for Retail Investors

> *"See the signal. Understand the why. Grounded in evidence."*

Built for **HackVerse: Into the Web (Sprint 1 — Web-Slinger Sprint / Rapid Vibe Coding)**  
**Problem Statement PS-01** · Organized by IEEE Robotics & Automation Society (IEEE RAS), VIT Chennai · TechnoVIT 2026.  

**Official Repository**: [https://github.com/niteeshk-2009/HackVerse-PS01](https://github.com/niteeshk-2009/HackVerse-PS01)  
**Public Deployment**: N/A — Sprint 1 deployment is optional.

---

## 1. Problem Context
India's retail investing demographic has witnessed historic expansion: over **130 million retail demat accounts registered**, with **80% under the age of 30**. However, SEBI's official 2024 longitudinal study confirms that **89% of individual retail derivative (F&O) participants lose money**, incurring aggregate annual net losses exceeding ₹52,000 Crores.

This tragedy is **not a data scarcity problem**. Real-time market tick streams, corporate statutory disclosures (SEBI LODR), and quarterly investor conference call transcripts are freely accessible. Rather, it is a structural **decision-intelligence asymmetry**:
- Institutional hedge funds deploy parallel multi-analyst desks simultaneously modeling quantitative price anomalies, balance sheet forensics, institutional order flow, and risk concentration.
- Retail investors are left with raw price charts, social media FOMO, and unverified speculative tips.

---

## 2. Solution
**SPIDER SENSE** eliminates this asymmetry. It is an autonomous multi-agent financial intelligence system engineered specifically for retail participants:
1. **Parallel Multi-Agent Reasoning**: Dispatches 4 distinct specialized analytical agents running concurrently in sub-second time.
2. **Deterministic Evidence Grounding**: Embeds an in-memory TF-IDF semantic vector RAG engine over authentic SEBI LODR filings and SEC Form 10-Q/10-K regulatory disclosures with exact page, section, and quote citations.
3. **Retail Trap & Conflict Detection**: Identifies cross-agent contradictions (e.g. price breakouts accompanied by heavy institutional distribution).
4. **Demonstrable Personalization**: Tailors verdicts, position sizing, and stop-loss bounds dynamically to the investor's specific risk tolerance and portfolio concentration.

---

## 3. Why It Is Different
| Dimension | Traditional Trading / FinTech Apps | SPIDER SENSE (PS-01) |
|---|---|---|
| **Analytical Breadth** | Single price chart or black-box rating | **4 Parallel Specialized Agents** (Technicals, RAG Fundamentals, Sentiment, Risk) |
| **Evidence Grounding** | Generic LLM summaries prone to hallucination | **Authentic Document Corpus** with verifiable page/section quote attribution |
| **Conflict Resolution** | Ignores contradictions between technicals & flow | **Explicit Cross-Agent Conflict Arbiter** detecting retail distribution traps |
| **Personalization** | Static advice identical for all users | **Mathematically Divergent Guidance** (Conservative vs Aggressive) on identical inputs |
| **Degraded Data Handling** | Fails silently or invents numbers | **Strict 3-State Policy** (`LIVE`, `DEMO`, `DATA UNAVAILABLE`) with confidence penalty |

---

## 4. Architecture Overview
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
           • Answers to 5 Core Questions
           • Exact Regulatory Citations
```

---

## 5. Multi-Agent System
SPIDER SENSE deploys **4 specialized analytical agents** executed concurrently via Python's `ThreadPoolExecutor(max_workers=4)`:

1. **Market Spider (`agents/market_spider.py`)**:
   - Evaluates price action across **3 independent dimensions**: Price Momentum (multi-EMA cluster), Volume Anomaly (delivery surge multiplier), and Volatility & Oscillators (RSI-14).
2. **Fundamental Web (`agents/fundamental_web.py`)**:
   - Executes semantic vector RAG retrieval over quarterly financial disclosures and risk factors.
3. **Sentiment Spider (`agents/sentiment_spider.py`)**:
   - Detects institutional smart-money accumulation vs retail FOMO option chasing.
4. **Risk Guardian (`agents/risk_guardian.py`)**:
   - Calculates mathematical portfolio concentration via the **Herfindahl-Hirschman Index (HHI)** and enforces capital protection rules.

---

## 6. RAG & Evidence Grounding
- **Corpus**: Indexed corporate disclosures from listed enterprises across Indian (NSE) and US Global (NASDAQ) equities:
  - Tata Motors, Reliance Industries, HDFC Bank, Zomato, Infosys, NVIDIA, Apple, Microsoft, Tesla, Alphabet, Amazon.
- **Provenance Contract**: Every evidence chunk visible to the user retains:
  - Document Title & Filing Type (e.g. `Tata Motors Ltd - Q2 FY26 Investor Presentation`)
  - Section & Page Provenance (e.g. `JLR Margin & Commercial EV Ramp (Page 3)`)
  - Semantic Cosine Relevance Score (e.g. `94% match`)
  - Verbatim Disclosed Excerpt
- **Anti-Hallucination Guardrail**: If a filing is missing or query relevance is below threshold, the agent flags `DATA_UNAVAILABLE` and caps confidence at $\le 55\%$, refusing to fabricate figures.

---

## 7. Personalization & Behavioral Intelligence
The system captures the investor's risk profile (Conservative, Moderate, Aggressive, or Custom Onboarding) and portfolio allocation:
- **Identical Input, Divergent Output**:
  - For a bullish breakout in `TATAMOTORS`:
    - **Conservative Investor**: Receives **`GRADUAL STAGGERED ACCUMULATION (SIP)`**, capping sector allocation at 5.0% to safeguard cash buffers.
    - **Aggressive Investor**: Receives **`MOMENTUM SWING ACCUMULATION`** with a mandatory 2.0% trailing stop-loss.

---

## 8. Degraded Data Safety & Truthful Policy
SPIDER SENSE enforces a strict, truthful 3-state data policy (`agents/base.py`):
- `LIVE DATA`: Authenticated real-time exchange streaming feed.
- `DEMO DATA`: Deterministic, reproducible simulation for hackathon verification (explicitly tagged in UI).
- `DATA UNAVAILABLE`: Explicitly indicated when feeds drop or filings are missing. Confidence is immediately penalized and protective warnings are inserted.

---

## 9. Key Features
- **Fintech Single-Page Cockpit**: Interactive single-page dashboard with instant tab switching (Cockpit, Compare, Stress Testing).
- **Spider-Man Inspired Dual Themes**:
  - *Dark Theme (Peter Parker)*: Stealth black (`#070a12`), crimson red (`#e62429`), cyan accents (`#00d2ff`).
  - *Light Theme (Gwen Stacy)*: Paper white (`#fcfcfd`), magenta pink (`#ff2a85`), purple border (`#7c3aed`).
- **Live Continuous Moving Tick Chart**: Streaming price updates and 20 EMA strictly bounded to real-time timestamps.
- **Cross-Market Comparison Duel**: Side-by-side comparative analysis between Indian and US equities (e.g. `TATAMOTORS` vs `TSLA`).
- **Telemetry Session Persistence**: SQLite storage recording pipeline latency, RAG latency, HHI concentration, and agreement scores.

---

## 10. Five Core Investor Questions Answered
Every synthesized analysis delivers unambiguous answers to:
1. **WHAT is happening?** Clear directional market diagnosis.
2. **WHY is it happening?** Causal reasoning across price, volume surge, and institutional flow.
3. **WHAT evidence supports it?** Verifiable citations from corporate regulatory filings.
4. **HOW confident is the system?** Calibrated statistical confidence with explicit uncertainty notes.
5. **WHAT does it mean for THIS investor?** Tailored position bounds and risk suitability.

---

## 11. Running Locally (Local Development Only)

### Prerequisites
- Python 3.11+
- Git

### Installation & Launch
```bash
# 1. Clone repository
git clone https://github.com/niteeshk-2009/HackVerse-PS01.git
cd HackVerse-PS01

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Spider Sense application server
python run.py
```
- Open in browser: **`http://localhost:8000`** *(Local development only)*
- Interactive Swagger API Docs: **`http://localhost:8000/docs`**

---

## 12. Running Automated Tests
```bash
# Run acceptance test suite (13 tests covering all PS-01 requirements)
python -m tests.test_system

# Run end-to-end multi-agent pipeline verification
python -m tests.test_end_to_end
```

---

## 13. PS-01 Requirement Mapping
Complete line-by-line verification is documented in **[REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md)**:

| PS-01 Mandate | Source File | Automated Test | Status |
|---|---|---|---|
| **Signal Classification ($\ge 3$ Dims)** | `agents/market_spider.py` | `tests/test_system.py` Test 1 | **VERIFIED PASS** |
| **Evidence-Grounded RAG** | `rag/engine.py`, `rag/corpus.py` | `tests/test_system.py` Test 2 | **VERIFIED PASS** |
| **Parallel Specialized Agents ($\ge 3$)** | `agents/web_mind.py` | `tests/test_system.py` Test 3, 13 | **VERIFIED PASS** |
| **Personalization Divergence** | `profiler/profiles.py` | `tests/test_system.py` Test 4 | **VERIFIED PASS** |
| **Live Interactive Cockpit** | `static/index.html`, `app/main.py` | `tests/test_system.py` Test 10 | **VERIFIED PASS** |
| **Measurable Telemetry ($\ge 3$ Metrics)**| `telemetry/logger.py` | `tests/test_system.py` Test 7, 11 | **VERIFIED PASS** |
| **Complete End-to-End Pipeline** | `agents/web_mind.py` | `tests/test_end_to_end.py` | **VERIFIED PASS** |
| **Degraded Data Handling** | `market_data/provider.py` | `tests/test_system.py` Test 6, 12 | **VERIFIED PASS** |

---

## 14. Project Structure
```
HackVerse-PS01/
├── .github/workflows/
│   └── tests.yml               # Automated CI test execution on push/PR
├── agents/
│   ├── base.py                 # Pydantic data contracts, enums & 3-state data types
│   ├── market_spider.py        # Technical momentum, volume anomaly & oscillator agent
│   ├── fundamental_web.py      # Semantic vector RAG & financial filing agent
│   ├── sentiment_spider.py     # Institutional FII net flow vs retail FOMO agent
│   ├── risk_guardian.py        # Portfolio concentration HHI & position sizing agent
│   └── web_mind.py             # The Spider Mind master synthesis & conflict arbiter
├── app/
│   └── main.py                 # FastAPI ASGI server, REST endpoints & static routes
├── market_data/
│   └── provider.py             # Deterministic NSE/NASDAQ market feeds & quote validation
├── profiler/
│   └── profiles.py             # User behavioral profiling, custom onboarding & HHI engine
├── rag/
│   ├── corpus.py               # Authentic SEBI LODR & SEC 10-Q/K regulatory document store
│   └── engine.py               # In-memory TF-IDF semantic vector similarity RAG engine
├── static/
│   └── index.html              # Single-page cockpit with Peter/Gwen themes & Chart.js
├── telemetry/
│   └── logger.py               # SQLite session latency & concentration metric logger
├── tests/
│   ├── test_system.py          # 13 core acceptance, resilience & unit tests
│   └── test_end_to_end.py      # Full 8-stage end-to-end pipeline test
├── .env.example                # Safe environment configuration template
├── .gitignore                  # Exclusion rules for databases, executables & caches
├── AGENTS.md                   # Formal multi-agent contracts & specifications
├── ARCHITECTURE.md             # System architecture & design documentation
├── DATA_SOURCES.md             # Data validation, 3-state policy & equity universe
├── DECISIONS.md                # Architectural decisions & engineering trade-offs
├── DEMO.md                     # Judge demonstration playbook
├── DEPLOYMENT.md               # Production cloud deployment guide & architecture
├── FINAL_AUDIT.md              # 35-point technical release gate audit report
├── REQUIREMENTS_TRACEABILITY.md# Full PS-01 requirement-to-file traceability matrix
├── requirements.txt            # Minimal production Python dependencies
└── run.py                      # One-click startup script (dynamic PORT & HOST)
```

---

## 15. AI Tools Used
- **Core Architecture & Modeling**: Designed in pair-programming with Google DeepMind Antigravity Agentic Assistant.
- **RAG Semantic Embeddings**: Tokenization and TF-IDF cosine similarity engine for deterministic regulatory citation matching.

---

## 16. Limitations
1. In default `DEMO` mode, market tick data is simulated deterministically to guarantee reproducible, zero-downtime evaluation during hackathon judging.
2. The RAG corpus currently covers key listed equities; expanding to the entire NSE 500 would require external vector database infrastructure (e.g. Milvus or pgvector).

---

## 17. Mandatory Financial Disclaimer
*This product provides AI-generated financial intelligence for informational and educational purposes and is not financial advice. Past performance and algorithmic models do not guarantee future market returns. Always consult a SEBI-registered investment advisor before deploying capital.*
