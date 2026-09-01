# SPIDER SENSE — Technical Architecture & Decision Logic

> *"Multi-Agent Autonomous Financial Intelligence for Retail Investors"*

---

## 1. System Architecture

SPIDER SENSE is engineered as a loosely coupled, highly deterministic multi-agent pipeline executing over asynchronous concurrent threads:

```
                  ┌────────────────────────────────────────┐
                  │          USER / CLIENT LAYER           │
                  │   FastAPI REST APIs · Tailwind Cockpit │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      ORCHESTRATION LAYER (SPIDER MIND) │
                  │     ThreadPoolExecutor (Max Workers=4) │
                  └───────┬───────────┬────────────┬───────┘
                          │           │            │
            ┌─────────────┘           │            └──────────────┐
            ▼                         ▼                           ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│     MARKET SPIDER     │ │    FUNDAMENTAL WEB    │ │   SENTIMENT SPIDER    │
│  Momentum · Volume    │ │  Semantic Vector RAG  │ │  FII Flows · Retail   │
│  Oscillators · Beta   │ │  SEBI LODR Filings    │ │  Trap Divergence      │
└───────────┬───────────┘ └───────────┬───────────┘ └─────────────┬─────────┘
            │                         │                           │
            └─────────────────────────┼───────────────────────────┘
                                      ▼
                          ┌───────────────────────┐
                          │     RISK GUARDIAN     │
                          │  Portfolio HHI Risk   │
                          │  Sector Limits · Cash │
                          └───────────┬───────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      SPIDER MIND SYNTHESIS ENGINE      │
                  │  • Disagreement / Conflict Resolver    │
                  │  • Profile Bayesian Weighting          │
                  │  • Anti-Hallucination Triad Engine     │
                  │  • Five Core Questions Generator       │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      PERSISTENCE & TELEMETRY LAYER     │
                  │   SQLite Audit Trail (Latency, HHI)    │
                  └────────────────────────────────────────┘
```

---

## 2. Key Subsystems & Design Choices

### A. Data Provider Abstraction (`market_data/provider.py`)
- Base class `MarketDataProvider` defines contracts for quotes, order books, chart series, and data quality validation.
- `DemoMarketProvider`: Deterministic, internally consistent simulator for Indian equities (TATAMOTORS, RELIANCE, HDFCBANK, ZOMATO, INFY). Explicitly marked `DEMO DATA`.
- `LiveMarketProvider`: Adapter for real-time exchange streams, gracefully returning `DATA UNAVAILABLE` with fallback snapshots when disconnected.

### B. Semantic Vector RAG Engine (`rag/engine.py`)
- Indexes real SEBI LODR disclosures and Q2 FY26 earnings conference transcripts.
- Computes tokenized TF-IDF vectors with cosine similarity matching.
- Strictly filters chunks by ticker to prevent cross-company hallucinations.

### C. Personalization & Risk Engine (`profiler/profiles.py`, `agents/risk_guardian.py`)
- Computes the Herfindahl-Hirschman Index:
  $$HHI = \sum_{i=1}^{N} s_i^2$$
  where $s_i$ is the percentage allocation of holding $i$.
- Evaluates asset beta against risk tolerance bounds ($\beta \le 1.0$ for Conservative, $>1.3$ for Aggressive).
- Capping position sizes to preserve liquidity buffers ($>15\%$ cash for Conservative).

### D. Conflict Resolution Logic (`agents/web_mind.py`)
- Detects divergence between technical breakouts and institutional selling (classic retail options trap).
- Prioritizes capital preservation over speculative momentum, discounting technical scores by 35% when institutional distribution is flagged.

---

## 3. Five Core Investor Questions
The synthesis engine directly populates:
1. `what_is_happening`
2. `why_is_it_happening`
3. `what_evidence_supports_it`
4. `how_confident_is_system`
5. `what_does_it_mean_for_investor`
