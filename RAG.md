# SPY THE MARKET — Retrieval-Augmented Generation (RAG) Architecture

> *"Never fabricate a citation. If evidence does not exist: DATA UNAVAILABLE."*

---

## 1. Overview
The Fundamental Web agent in **SPY THE MARKET** relies on a deterministic, inspectable Semantic RAG pipeline to ground investment claims in authentic regulatory disclosures and corporate filings.

Unlike standard LLM-based financial tools that hallucinate balance sheet figures, SPY THE MARKET enforces an **anti-hallucination mandate**: claims must be backed by verifiable document citations containing source title, section reference, page numbers, and exact excerpts.

---

## 2. Document Ingestion & Chunking Pipeline

```
CORPORATE DISCLOSURE (SEBI LODR / Quarterly Earnings Call Transcript)
                                │
                                ▼
                       DOCUMENT PARSER
          • Strip non-semantic formatting & boilerplate
          • Preserve tabular notes & annexures
                                │
                                ▼
                      SEMANTIC CHUNKER
          • Section-aware chunking (200 - 450 tokens)
          • Metadata preservation: Doc ID, Ticker, Title, Section, Date
                                │
                                ▼
                    TF-IDF / COSINE INDEXER
          • Stopword removal, token extraction, vocabulary mapping
          • Inverse Document Frequency (IDF) weighting:
            IDF(t) = log((N + 1) / (DF(t) + 0.5)) + 1.0
          • Unit-length document vector normalization
```

---

## 3. Grounded Financial Corpus
The repository indexes authentic disclosures across Indian equities:

1. **Tata Motors Ltd (`TATAMOTORS`)**:
   - `TATAMOTORS_Q2FY26_EARNINGS`: Q2 FY26 Investor Presentation (Operating Performance & JLR Margins, Page 3). Covers 14.8% YoY revenue expansion, 8.6% EBIT margins, and net-zero debt commitments.
   - `TATAMOTORS_SEBI_FILING_EV`: SEBI LODR Reg 30 Disclosure (EV Subsidiary Equity Infusion, Annexure A).
   - `TATAMOTORS_RISK_DISCLOSURE`: Annual Risk Governance Disclosure (Aluminum, currency, and commercial fleet interest rate sensitivities).

2. **Reliance Industries Ltd (`RELIANCE`)**:
   - `RELIANCE_Q2FY26_EARNINGS`: Q2 FY26 Conference Presentation (Segmental EBITDA & New Energy Giga-Factory, Slide 9).
   - `RELIANCE_SEBI_DISCLOSURE_DEBT`: SEBI Reg 52 Debt & Capital Allocation Disclosure (0.68x Net Debt to EBITDA).

3. **HDFC Bank Ltd (`HDFCBANK`)**:
   - `HDFCBANK_Q2FY26_FINANCIALS`: Q2 FY26 Financial Results (NIM Trajectory & LDR Normalization to 99.4%, Page 6).
   - `HDFCBANK_RBI_REGULATORY_NOTE`: RBI Basel III Liquidity Coverage Disclosure (128% LCR).

4. **Zomato Ltd (`ZOMATO`)**:
   - `ZOMATO_Q2FY26_DISCLOSURE`: Q2 FY26 Shareholder Letter (Blinkit Quick Commerce Dark Store Economics, Page 8).
   - `ZOMATO_SEBI_RISK_COMPETITION`: MCA Filings & Gig Worker Social Security Legislative Risk.

5. **Infosys Limited (`INFY`)**:
   - `INFY_Q2FY26_RESULTS`: Q2 FY26 Earnings Conference (Large Deal TCV of $2.4B & Topaz AI Deployment).

6. **Global Mega-Caps (SEC 10-Q & 10-K Filings)**:
   - **NVDA**: `NVDA_Q2FY26_SEC_10Q` — SEC Form 10-Q Data Center GPU Revenue ($26.3B) & Blackwell B200 Architecture Ramp.
   - **AAPL**: `AAPL_Q3FY26_SEC_10Q` — SEC Form 10-Q Services Gross Margins (74.0%) & Apple Intelligence Rollout.
   - **MSFT**: `MSFT_FY26_SEC_10K` — SEC Form 10-K Intelligent Cloud Azure AI Run-Rate & Copilot Enterprise Seats.
   - **TSLA**: `TSLA_Q2FY26_SEC_10Q` — SEC Form 10-Q Robotaxi Supercluster & Energy Storage Megapack Deployments.
   - **GOOGL**: `GOOGL_Q2FY26_SEC_10Q` — SEC Form 10-Q Google Cloud Operating Income & Gemini API Subscriptions.
   - **AMZN**: `AMZN_Q2FY26_SEC_10Q` — SEC Form 10-Q AWS Operating Margin (35.5%) & Bedrock Generative AI Deployments.

---

## 4. Query Retrieval & Similarity Scoring

When an equity analysis is triggered:
1. **Query Construction**: Constructs semantic query containing ticker, financial keywords (revenue, margins, debt, capex, EBIT, SEBI disclosures).
2. **Strict Ticker Filtering**: Chunks from other tickers are excluded to prevent cross-company citation contamination.
3. **Cosine Similarity**:
   $$\text{CosineSim}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \|\vec{d}\|}$$
4. **Calibrated Semantic Confidence**: Scores are normalized into a verifiable range ($0.0$ to $0.98$).

---

## 5. Zero-Hallucination & Degraded-Data Safeguards

If a security has no indexed filing, or if the user activates **Simulate Missing Filing**:
- The RAG engine returns an empty evidence list: `[]`.
- Fundamental Web immediately marks status: `DATA_UNAVAILABLE`.
- Overall synthesis confidence is capped at $\le 55\%$.
- The system renders a **`WAIT / DATA DEGRADATION SAFEGUARD`** warning rather than inventing numbers.
