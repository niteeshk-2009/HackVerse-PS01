"""
SPIDER-SENSE: Agent 2 — FUNDAMENTAL WEB
Role: Fundamental & Regulatory Intelligence Analyst
Analyzes financial disclosures, debt covenants, margins, valuation multiples,
and retrieves verifiable evidence using Semantic RAG from the financial disclosure corpus.
"""

import time
from typing import Dict, Any, List
from spidersense.agents.base import (
    AgentOutput, AgentSignal, SignalClassification, DegradedModeConfig
)
from spidersense.rag.engine import rag_engine


class FundamentalWebAgent:
    def __init__(self):
        self.name = "Fundamental Web"
        self.role = "Fundamental & Regulatory Intelligence Analyst"

    def analyze(self, quote: Dict[str, Any], config: DegradedModeConfig) -> AgentOutput:
        start_time = time.perf_counter()
        ticker = quote["ticker"]
        pe = quote.get("pe_ratio", 25.0)
        debt_equity = quote.get("debt_to_equity", 0.5)

        signals: List[AgentSignal] = []
        reasoning: List[str] = []
        risks: List[str] = []

        # -------------------------------------------------------------
        # 1. RAG SEMANTIC RETRIEVAL
        # -------------------------------------------------------------
        query_str = f"{ticker} quarterly revenue margins debt capex earnings SEBI regulatory disclosures"
        evidence_list, rag_latency = rag_engine.query(
            ticker=ticker,
            query_text=query_str,
            top_k=2,
            simulate_missing=config.simulate_missing_filing
        )

        is_filing_missing = (len(evidence_list) == 0) or config.simulate_missing_filing
        status = "DATA_UNAVAILABLE" if is_filing_missing else "SUCCESS"

        if is_filing_missing:
            # Degraded scenario: Missing corporate disclosures / filing unavailable
            overall_signal = SignalClassification.DATA_UNAVAILABLE
            overall_score = 0.0
            overall_confidence = 42.0
            reasoning.append("⚠ REGULATORY FILING UNAVAILABLE: SEBI disclosure or quarterly earnings transcript could not be retrieved from document repository.")
            reasoning.append("Per anti-hallucination mandate, the agent refuses to synthesize unverified corporate assertions.")
            risks.append("Unverified regulatory status: Pending formal disclosure verification.")
            
            signals.append(AgentSignal(
                dimension="Regulatory Governance",
                classification=SignalClassification.DATA_UNAVAILABLE,
                score=0.0,
                confidence=30.0,
                evidence_reasoning="Filing absent from document corpus. Degradation mode triggered."
            ))
        else:
            # -------------------------------------------------------------
            # 2. EVALUATE FINANCIAL QUALITY & CITATION
            # -------------------------------------------------------------
            primary_evidence = evidence_list[0]
            excerpt_lower = primary_evidence.excerpt.lower()

            # Analyze valuation & leverage
            if debt_equity < 0.5 and pe < 30.0:
                fund_class = SignalClassification.STRONG_BULLISH
                fund_score = 80.0
                fund_conf = 88.0
                fund_reason = f"Robust balance sheet: Low debt-to-equity ratio ({debt_equity:.2f}x) and attractive P/E valuation ({pe:.1f}x) provide strong margin of safety."
            elif pe > 75.0:
                fund_class = SignalClassification.NEUTRAL
                fund_score = 25.0
                fund_conf = 78.0
                fund_reason = f"High growth premium: P/E multiple is elevated at {pe:.1f}x, requiring sustained 30%+ earnings CAGR to justify valuation."
                risks.append(f"Valuation sensitivity: Elevated P/E multiple ({pe:.1f}x) leaves little room for earnings execution slippage.")
            else:
                fund_class = SignalClassification.BULLISH
                fund_score = 60.0
                fund_conf = 80.0
                fund_reason = f"Sound operating fundamentals: P/E ({pe:.1f}x) and leverage ({debt_equity:.2f}x) reflect stable financial positioning."

            signals.append(AgentSignal(
                dimension="Valuation & Leverage",
                classification=fund_class,
                score=fund_score,
                confidence=fund_conf,
                evidence_reasoning=fund_reason
            ))
            reasoning.append(fund_reason)

            # Analyze retrieved RAG filing evidence
            rag_reason = f"RAG Grounding [{primary_evidence.source} - {primary_evidence.section}]: {primary_evidence.excerpt[:160]}..."
            reasoning.append(rag_reason)

            signals.append(AgentSignal(
                dimension="Retrieved Disclosures",
                classification=SignalClassification.BULLISH if "expansion" in excerpt_lower or "growth" in excerpt_lower or "ebitda" in excerpt_lower else SignalClassification.NEUTRAL,
                score=75.0,
                confidence=round(primary_evidence.relevance_score * 100.0, 1),
                evidence_reasoning=f"Verified through filing: {primary_evidence.section}. Semantic match {primary_evidence.relevance_score*100:.1f}%."
            ))

            overall_score = round((fund_score * 0.5) + (75.0 * 0.5), 1)
            overall_confidence = round((fund_conf + (primary_evidence.relevance_score * 100.0)) / 2.0, 1)
            overall_signal = SignalClassification.STRONG_BULLISH if overall_score >= 70 else SignalClassification.BULLISH

        execution_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        return AgentOutput(
            agent_name=self.name,
            role=self.role,
            status=status,
            signal=overall_signal,
            score=overall_score,
            confidence=overall_confidence,
            signals=signals,
            reasoning=reasoning,
            evidence=evidence_list,
            risks=risks,
            metrics={
                "pe_ratio": pe,
                "debt_to_equity": debt_equity,
                "rag_latency_ms": rag_latency,
                "retrieved_chunks_count": len(evidence_list)
            },
            execution_time_ms=execution_ms,
            data_source_state=quote.get("data_source_state", "DEMO DATA")
        )
