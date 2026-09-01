"""
SPIDER-SENSE: Agent 4 — RISK GUARDIAN
Role: Personalized Portfolio & Behavioral Risk Intelligence
Evaluates user's individual risk tolerance, investment horizon, existing sector concentration,
and enforces disciplined capital protection constraints tailored to the individual retail investor.
"""

import time
from typing import Dict, Any, List
from spidersense.agents.base import (
    AgentOutput, AgentSignal, SignalClassification, UserProfile,
    RiskTolerance, InvestmentHorizon, DegradedModeConfig
)


class RiskGuardianAgent:
    def __init__(self):
        self.name = "Risk Guardian"
        self.role = "Personalized Portfolio & Risk Intelligence"

    def analyze(self, quote: Dict[str, Any], profile: UserProfile, config: DegradedModeConfig) -> AgentOutput:
        start_time = time.perf_counter()
        ticker = quote["ticker"]
        sector = quote.get("sector", "General")
        beta = quote.get("beta", 1.0)
        hhi = profile.portfolio.concentration_hhi

        signals: List[AgentSignal] = []
        reasoning: List[str] = []
        risks: List[str] = []

        # Check existing exposure to this ticker or sector
        existing_holding = next((h for h in profile.portfolio.holdings if h.ticker == ticker), None)
        current_ticker_alloc = existing_holding.allocation_pct if existing_holding else 0.0
        current_sector_alloc = profile.portfolio.sector_allocations.get(sector, 0.0)

        # -------------------------------------------------------------
        # 1. CONCENTRATION & SECTOR EXPOSURE
        # -------------------------------------------------------------
        if current_sector_alloc > 35.0 or current_ticker_alloc > 25.0:
            conc_class = SignalClassification.BEARISH
            conc_score = -65.0
            conc_conf = 92.0
            conc_reason = f"Elevated concentration hazard: Portfolio already holds {current_sector_alloc:.1f}% in {sector} (HHI: {hhi:.0f}). Adding {ticker} compounds single-sector drawdown vulnerability."
            risks.append(f"Sector over-exposure: {sector} accounts for {current_sector_alloc:.1f}% of current assets.")
        elif current_sector_alloc > 20.0:
            conc_class = SignalClassification.NEUTRAL
            conc_score = -20.0
            conc_conf = 85.0
            conc_reason = f"Moderate sector exposure ({current_sector_alloc:.1f}%). Additional exposure should be tightly capped."
        else:
            conc_class = SignalClassification.BULLISH
            conc_score = 70.0
            conc_conf = 88.0
            conc_reason = f"Diversification benefit: Low existing exposure to {sector} ({current_sector_alloc:.1f}%). Enhances portfolio diversification."

        signals.append(AgentSignal(
            dimension="Portfolio Concentration & HHI",
            classification=conc_class,
            score=conc_score,
            confidence=conc_conf,
            evidence_reasoning=conc_reason
        ))
        reasoning.append(conc_reason)

        # -------------------------------------------------------------
        # 2. RISK TOLERANCE & VOLATILITY FIT
        # -------------------------------------------------------------
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
            if beta > 1.25:
                tol_class = SignalClassification.BEARISH
                tol_score = -70.0
                tol_conf = 90.0
                tol_reason = f"Mismatch with Conservative profile: {ticker} beta is {beta:.2f} (high volatility). Capital preservation mandate prioritizes low-beta defensive assets."
                risks.append(f"Beta risk ({beta:.2f}x benchmark) violates conservative risk threshold.")
            else:
                tol_class = SignalClassification.BULLISH
                tol_score = 60.0
                tol_conf = 85.0
                tol_reason = f"Asset beta ({beta:.2f}) aligns with conservative preservation guidelines."
        elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE:
            if beta > 1.25:
                tol_class = SignalClassification.STRONG_BULLISH
                tol_score = 80.0
                tol_conf = 88.0
                tol_reason = f"High-beta profile fit: Beta of {beta:.2f} matches aggressive growth profile. Momentum and swing opportunities are prioritized."
            else:
                tol_class = SignalClassification.NEUTRAL
                tol_score = 40.0
                tol_conf = 80.0
                tol_reason = f"Lower beta ({beta:.2f}) provides steady base but offers limited swing momentum for aggressive targets."
        else: # MODERATE
            tol_class = SignalClassification.BULLISH if beta < 1.3 else SignalClassification.NEUTRAL
            tol_score = 45.0 if beta < 1.3 else 10.0
            tol_conf = 82.0
            tol_reason = f"Balanced profile fit: Beta of {beta:.2f} within moderate risk tolerance limits."

        signals.append(AgentSignal(
            dimension="Risk Profile & Volatility Fit",
            classification=tol_class,
            score=tol_score,
            confidence=tol_conf,
            evidence_reasoning=tol_reason
        ))
        reasoning.append(tol_reason)

        # -------------------------------------------------------------
        # 3. BEHAVIORAL LOSS AVERSION & CASH SUFFICIENCY
        # -------------------------------------------------------------
        cash_pct = (profile.portfolio.cash_balance / profile.portfolio.total_portfolio_value) * 100.0
        if cash_pct < 10.0:
            beh_class = SignalClassification.BEARISH
            beh_score = -50.0
            beh_conf = 84.0
            beh_reason = f"Cash liquidity squeeze: Available cash is only {cash_pct:.1f}%. Capital should be conserved for margin cushions."
            risks.append("Low cash buffer limits flexibility in adverse volatility.")
        else:
            beh_class = SignalClassification.BULLISH
            beh_score = 65.0
            beh_conf = 86.0
            beh_reason = f"Adequate liquidity: Cash reserves stand at {cash_pct:.1f}% (INR {profile.portfolio.cash_balance:,.0f})."

        signals.append(AgentSignal(
            dimension="Liquidity & Behavioral Guardrails",
            classification=beh_class,
            score=beh_score,
            confidence=beh_conf,
            evidence_reasoning=beh_reason
        ))
        reasoning.append(beh_reason)

        overall_score = round((conc_score * 0.40) + (tol_score * 0.40) + (beh_score * 0.20), 1)
        overall_confidence = round(sum(s.confidence for s in signals) / len(signals), 1)

        if overall_score >= 40:
            overall_signal = SignalClassification.BULLISH if overall_score < 70 else SignalClassification.STRONG_BULLISH
        elif overall_score <= -30:
            overall_signal = SignalClassification.BEARISH if overall_score > -60 else SignalClassification.STRONG_BEARISH
        else:
            overall_signal = SignalClassification.NEUTRAL

        execution_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        return AgentOutput(
            agent_name=self.name,
            role=self.role,
            status="SUCCESS",
            signal=overall_signal,
            score=overall_score,
            confidence=overall_confidence,
            signals=signals,
            reasoning=reasoning,
            evidence=[],
            risks=risks,
            metrics={
                "portfolio_hhi": hhi,
                "current_ticker_allocation_pct": current_ticker_alloc,
                "current_sector_allocation_pct": current_sector_alloc,
                "cash_reserve_pct": round(cash_pct, 1),
                "user_risk_tolerance": profile.risk_tolerance.value
            },
            execution_time_ms=execution_ms,
            data_source_state=quote.get("data_source_state", "DEMO DATA")
        )
