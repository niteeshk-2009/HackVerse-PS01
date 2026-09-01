# SPIDER SENSE — PS-01 Requirements Traceability Matrix

This document provides a factual, line-by-line audit mapping every core requirement of **HackVerse: Into the Web (Sprint 1 — Web-Slinger Sprint) Problem Statement PS-01** (*Multi-Agent Autonomous Financial Intelligence System for Retail Investors*) directly to the concrete source files, automated tests, UI elements, and verification methods.

---

## Complete PS-01 Requirement Traceability

### 1. Multi-Dimensional Signal Classification
- **PS-01 Mandate**: Signal classification across at least THREE independent dimensions with stated confidence and cited reasoning.
- **Implementation**: `MarketSpiderAgent` evaluates:
  1. **Price Momentum**: Multi-EMA alignment (20, 50, 200 EMA) and MACD histogram slope.
  2. **Volume Anomaly**: Institutional volume surge multiplier (e.g. 1.61x normal volume) and delivery percentage.
  3. **Volatility & Oscillators**: 14-period Relative Strength Index (RSI-14) with overbought/oversold boundaries.
  4. **Institutional Order Flow**: FII / DII net flow tracking.
- **Relevant Source Files**:
  - `agents/market_spider.py` (`analyze()`)
  - `agents/base.py` (`AgentSignal`, `SignalClassification`)
- **Automated Test**: `tests/test_system.py::test_signal_classification_three_dimensions`
- **UI Location**: Top Dashboard Header (Signal Badge) + *Market Spider* Panel (3 individual signal dimension pills with score, confidence %, and cited rationale).
- **Verification Method**: Run `python -m tests.test_system`.

---

### 2. Evidence-Grounded RAG (Retrieval-Augmented Generation)
- **PS-01 Mandate**: Retrieval-Augmented Generation grounded in a document corpus, with source attribution visible to the user.
- **Implementation**: In-memory TF-IDF semantic vector similarity engine with strict ticker isolation. Indexes authentic SEBI LODR corporate filings, concall transcripts, and SEC Form 10-Q/10-K regulatory disclosures.
- **Relevant Source Files**:
  - `rag/engine.py` (`RAGEngine.query()`)
  - `rag/corpus.py` (`FINANCIAL_DOCUMENTS_CORPUS`)
  - `agents/fundamental_web.py` (`FundamentalWebAgent.analyze()`)
- **Automated Test**: `tests/test_system.py::test_rag_semantic_retrieval_and_citations`
- **UI Location**: *Fundamental Web* Agent Panel + Master Synthesis Evidence Chain (renders source filing title, section/page, semantic cosine relevance score %, and verbatim regulatory excerpt).
- **Verification Method**: Run `python -m tests.test_system` and query `/api/evidence/TATAMOTORS`.

---

### 3. Parallel Specialized Multi-Agent System
- **PS-01 Mandate**: At least THREE specialized agents executing in parallel, each with a defined role and structured output contract, consumed by a synthesis layer.
- **Implementation**: 4 distinct specialized agents executed concurrently via Python's `ThreadPoolExecutor(max_workers=4)`:
  1. **Market Spider**: Technical, momentum, volume anomaly, and oscillator analysis.
  2. **Fundamental Web**: SEC/SEBI corporate filing semantic RAG and balance sheet health.
  3. **Sentiment Spider**: Institutional FII net order flow vs Retail Option FOMO chasing.
  4. **Risk Guardian**: Herfindahl-Hirschman Index (HHI) portfolio concentration and position sizing.
  - **The Spider Mind Orchestrator** consumes all 4 structured outputs to generate the master verdict.
- **Relevant Source Files**:
  - `agents/market_spider.py`
  - `agents/fundamental_web.py`
  - `agents/sentiment_spider.py`
  - `agents/risk_guardian.py`
  - `agents/web_mind.py` (`WebMindOrchestrator.run_pipeline()`)
  - `agents/base.py` (`AgentOutput`, `SynthesisOutput`)
- **Automated Test**: `tests/test_system.py::test_agent_structured_output_contract`, `tests/test_system.py::test_parallel_orchestration_speed`
- **UI Location**: *Cockpit & 4 Agents* grid (4 individual cards with live badges, signal scores, and latency readouts).
- **Verification Method**: Run `python -m tests.test_system`.

---

### 4. User Profiling & Demonstrable Personalization Divergence
- **PS-01 Mandate**: User profiling modifying outputs according to stored risk parameters and demonstrably producing different outputs for different profiles on identical market inputs.
- **Implementation**: Onboarding profiler captures capital, risk tolerance, horizon, and portfolio allocation. Evaluates identical market input (e.g. `TATAMOTORS` breakout):
  - **Conservative Profile**: Outputs "GRADUAL STAGGERED ACCUMULATION" with strict 5% sector cap to preserve cash buffer.
  - **Aggressive Profile**: Outputs "MOMENTUM SWING ACCUMULATION" with 2.0% trailing stop-loss for maximum upside.
- **Relevant Source Files**:
  - `profiler/profiles.py` (`get_profile()`, `register_custom_profile()`)
  - `agents/risk_guardian.py` (`analyze()`)
  - `agents/web_mind.py` (`_resolve_conflicts_and_personalize()`)
- **Automated Test**: `tests/test_system.py::test_user_profile_personalization_divergence`
- **UI Location**: User Profile Chip (top right) + Tailored Personalization Note card in Master Synthesis.
- **Verification Method**: Run `python -m tests.test_system` and toggle profile via UI or `/api/profile/custom`.

---

### 5. Live Interactive Interface
- **PS-01 Mandate**: Live interface showing current market signals, classification labels, synthesized agent output, source attribution, and portfolio/watchlist state.
- **Implementation**: Single-page fintech cockpit built with Tailwind CSS and Chart.js:
  - Continuously moving real-time tick chart with 20 EMA overlay.
  - Watchlist carousel with multi-currency dynamic formatting ($ vs ₹) and regional filter pills (All, NSE, US/Global).
  - 4 specialized agent cards with signal meters.
  - Compare 2 Stocks head-to-head investment duel.
  - Stress testing workbench for retail traps and data failures.
- **Relevant Source Files**:
  - `static/index.html`
  - `app/main.py` (`/`)
- **Automated Test**: `tests/test_system.py::test_api_route_semantics`, `tests/test_end_to_end.py`
- **UI Location**: Entire single-page interface served at `http://localhost:8000/`.
- **Verification Method**: Start server (`python run.py`) and inspect in browser.

---

### 6. Performance Logging & Measurable Telemetry
- **PS-01 Mandate**: Performance logging with at least THREE measurable metrics.
- **Implementation**: SQLite session persistence tracking 4 distinct quantitative metrics per pipeline execution:
  1. `total_pipeline_latency_ms`: Real runtime roundtrip latency measured at execution time.
  2. `rag_retrieval_latency_ms`: Semantic corpus search latency.
  3. `portfolio_risk_concentration`: Mathematical Herfindahl-Hirschman Index (HHI, 0 - 10000).
  4. `signal_agreement_score_pct`: Multi-agent consensus percentage.
- **Relevant Source Files**:
  - `telemetry/logger.py` (`TelemetryLogger.log_session()`)
  - `agents/base.py` (`TelemetryMetrics`)
  - `app/main.py` (`GET /api/telemetry`)
- **Automated Test**: `tests/test_system.py::test_portfolio_concentration_hhi`, `tests/test_end_to_end.py`
- **UI Location**: Latency badge in header + Telemetry Session Drawer (`GET /api/telemetry`).
- **Verification Method**: Run `python -m tests.test_end_to_end` and inspect `GET /api/telemetry`.

---

### 7. End-to-End Reasoning Pipeline
- **PS-01 Mandate**: At least one complete end-to-end flow from raw data through specialized agents to synthesized user-facing recommendation with visible reasoning.
- **Implementation**: 8-stage sequential pipeline:
  `Raw Quote Ingestion` -> `Sanity Validation` -> `Parallel 4-Agent Execution` -> `RAG Corpus Retrieval` -> `Portfolio HHI Conditioning` -> `Cross-Agent Conflict Detection` -> `Spider Mind Master Synthesis` -> `User Verdict`.
- **Relevant Source Files**:
  - `market_data/provider.py`
  - `agents/web_mind.py`
  - `app/main.py` (`POST /api/analyze`)
- **Automated Test**: `tests/test_end_to_end.py::test_end_to_end_full_pipeline`
- **UI Location**: Central Cockpit Master Verdict Card.
- **Verification Method**: Run `python -m tests.test_end_to_end`.

---

### 8. Graceful Degraded-Data Handling & Anti-Hallucination
- **PS-01 Mandate**: Graceful degraded-data handling without pipeline failure or uncited output.
- **Implementation**:
  - **Feed Disconnect**: Marks status as `WARNING / DEGRADED`, falls back to cached offline snapshot, penalizes confidence by 40%, and inserts explicit warning.
  - **Missing SEBI/SEC Filing**: RAG engine returns `[]`, Fundamental Web marks status as `DATA_UNAVAILABLE`, caps confidence at <= 55%, and changes verdict to `WAIT / DATA DEGRADATION SAFEGUARD`.
  - **Signal Conflict (Retail Trap)**: Resolves technical vs institutional flow contradiction, discounts momentum, and enforces a mandatory 2.0% stop-loss.
  - **Zero Fabrication**: Refuses to invent filings or numbers when data is absent.
- **Relevant Source Files**:
  - `market_data/provider.py` (`validate_quote()`)
  - `agents/market_spider.py`
  - `agents/fundamental_web.py`
  - `agents/web_mind.py` (`_resolve_conflicts_and_personalize()`)
- **Automated Test**: `tests/test_system.py::test_degraded_data_handling_missing_filing`, `tests/test_system.py::test_stale_data_handling`, `tests/test_system.py::test_agent_conflict_detection_and_resolution`
- **UI Location**: *Stress Testing* Tab (Interactive buttons for Normal, Conflict, Missing Filing, Feed Failure).
- **Verification Method**: Run `python -m tests.test_system`.

---

## Audit Verification Summary
| # | PS-01 Mandate | Automated Test | Status |
|---|---|---|---|
| 1 | Signal Classification across >= 3 Dimensions | `tests/test_system.py::test_signal_classification_three_dimensions` | **PASS (100%)** |
| 2 | RAG Grounding & Source Attribution | `tests/test_system.py::test_rag_semantic_retrieval_and_citations` | **PASS (100%)** |
| 3 | >= 3 Parallel Specialized Agents | `tests/test_system.py::test_agent_structured_output_contract`, `test_parallel_orchestration_speed` | **PASS (100%)** |
| 4 | Personalization Divergence on Identical Input | `tests/test_system.py::test_user_profile_personalization_divergence` | **PASS (100%)** |
| 5 | Live Cockpit Interface | `tests/test_system.py::test_api_route_semantics` | **PASS (100%)** |
| 6 | Performance Logging with >= 3 Metrics | `tests/test_system.py::test_portfolio_concentration_hhi`, `test_hhi_edge_cases` | **PASS (100%)** |
| 7 | Complete End-to-End Pipeline | `tests/test_end_to_end.py::test_end_to_end_full_pipeline` | **PASS (100%)** |
| 8 | Degraded-Data Handling & Anti-Hallucination | `tests/test_system.py::test_degraded_data_handling_missing_filing`, `test_stale_data_handling` | **PASS (100%)** |
