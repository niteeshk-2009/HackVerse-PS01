# SPIDER SENSE — Architectural Decisions & Trade-Offs

> Engineering rationale and decision record for the Multi-Agent Autonomous Financial Intelligence System.

---

## 1. Decision 1: Parallel ThreadPool vs Sequential Agent Execution
- **Context**: Real-time retail decision requirements demand high-throughput multi-agent synthesis with minimal round-trip latency.
- **Decision**: Implemented `ThreadPoolExecutor(max_workers=4)` inside `WebMindOrchestrator` to execute Market Spider, Fundamental Web (RAG), Sentiment Spider, and Risk Guardian concurrently.
- **Outcome**: Designed for low-latency interactive analysis with per-agent execution telemetry, executing concurrent sub-second analysis.

---

## 2. Decision 2: Semantic Vector TF-IDF RAG with Ticker Isolation
- **Context**: LLM-based RAG pipelines frequently suffer from cross-document hallucination and high API token latency.
- **Decision**: Built an in-memory TF-IDF / Cosine Vector engine with strict ticker isolation. Documents are chunked, tokenized, and indexed by equity ticker.
- **Outcome**: Deterministic, zero-dependency RAG execution with verifiable page and section citations.

---

## 3. Decision 3: Herfindahl-Hirschman Index (HHI) for Concentration Risk
- **Context**: Retail portfolios often fail due to hidden single-sector concentration.
- **Decision**: Enforced standard antitrust/portfolio HHI math:
  $$HHI = \sum_{i=1}^N \left(\frac{\text{Value}_i}{\text{Total}}\right)^2 \times 10,000$$
- **Outcome**: Portfolios with $HHI > 2500$ automatically trigger concentration warnings in Risk Guardian, dynamically altering position suitability.

---

## 4. Decision 4: The Anti-Hallucination Triad (Fact / Inference / Interpretation)
- **Context**: Black-box financial advice causes retail distrust and regulatory non-compliance.
- **Decision**: Enforced an explicit tripartite data contract on all synthesized outputs:
  1. **Facts**: Verifiable citations from SEBI filings, price feeds, or portfolio records.
  2. **Inferences**: Algorithmic calculations (moving average slopes, RSI-14, volume surge multipliers).
  3. **Personalized Interpretations**: Tailored position caps and risk suitability conditioned on user risk tolerance.
- **Outcome**: Complete transparency and explainability for judges and retail users alike.

---

## 5. Decision 5: Strict 3-State Data Policy (LIVE / DEMO / UNAVAILABLE)
- **Context**: Hackathons often masquerade synthetic data as "LIVE", destroying credibility.
- **Decision**: Codified a strict 3-state enum (`DataSourceState`): `LIVE DATA`, `DEMO DATA`, and `DATA UNAVAILABLE`. Demo data is always explicitly labeled DEMO.
- **Outcome**: Authentic engineering standards that respect user trust and real-world compliance.
