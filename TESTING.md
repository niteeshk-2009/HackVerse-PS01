# SPY THE MARKET — Automated Testing & Verification Suite

---

## 1. Overview
The **SPY THE MARKET** test suite (`tests/test_system.py`) verifies all 7 core HackVerse PS-01 minimum requirements plus data integrity, five core questions, and HTTP semantics.

---

## 2. Test Execution Command

Run the complete test suite from the repository root:

```powershell
python tests/test_system.py
```

---

## 3. Test Cases & Verification Matrix

| # | Test Function | Verified Requirement | Status |
|---|---|---|---|
| **1** | `test_signal_classification_three_dimensions` | Evaluates Price Momentum, Volume Anomaly, and Volatility/Oscillators across normalized scales with stated confidence & cited reasoning. | **PASS** |
| **2** | `test_rag_semantic_retrieval_and_citations` | Validates semantic vector retrieval across SEBI filings, page/section excerpts, and cosine similarity scoring. | **PASS** |
| **3** | `test_agent_structured_output_contract` | Verifies that Market Spider, Fundamental Web, and Sentiment Spider strictly conform to typed Pydantic contracts. | **PASS** |
| **4** | `test_user_profile_personalization_divergence` | **Demonstrable Personalization**: Verifies that identical market data produces divergent advice for Conservative vs. Aggressive profiles. | **PASS** |
| **5** | `test_agent_conflict_detection_and_resolution` | Detects cross-agent disagreement (e.g. Bullish momentum vs Institutional distribution) and verifies resolution logic. | **PASS** |
| **6** | `test_degraded_data_handling_missing_filing` | Validates zero-hallucination safeguard when filings are unavailable (`DATA_UNAVAILABLE` status, confidence penalty). | **PASS** |
| **7** | `test_portfolio_concentration_hhi` | Verifies mathematical accuracy of the Herfindahl-Hirschman Index ($HHI = \sum w_i^2$) for portfolio risk. | **PASS** |
| **8** | `test_data_state_validation_and_quality` | Enforces strict 3-state data labeling (`DEMO DATA` vs `LIVE DATA`) and data quality validation flags. | **PASS** |
| **9** | `test_five_questions_completeness` | Ensures the five essential investor questions (What, Why, Evidence, Confidence, Investor Impact) are populated. | **PASS** |
| **10** | `test_api_route_semantics` | Validates HTTP semantics: returns HTTP 200 on valid requests and HTTP 404 on unknown tickers/profiles. | **PASS** |

---

## 4. Test Suite Execution Output
```text
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

ALL 10 ACCEPTANCE & QUALITY TESTS PASSED SUCCESSFULLY!
```
