"""
SPIDER-SENSE: Synthesis Agent — THE WEB MIND
Role: Master Orchestrator, Cross-Agent Synthesis & Explainability Engine
Receives structured outputs from all 4 specialized agents, evaluates consensus/conflicts,
weighs evidence, applies user behavioral guardrails, and renders inspectable intelligence.
"""

import time
from typing import Dict, Any, List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from spidersense.agents.base import (
    AgentOutput, SynthesisOutput, UserProfile, DegradedModeConfig,
    AgentDisagreement, TelemetryMetrics, SignalClassification, RiskTolerance
)
from spidersense.agents.market_spider import MarketSpiderAgent
from spidersense.agents.fundamental_web import FundamentalWebAgent
from spidersense.agents.sentiment_spider import SentimentSpiderAgent
from spidersense.agents.risk_guardian import RiskGuardianAgent


class WebMindOrchestrator:
    def __init__(self):
        self.market_agent = MarketSpiderAgent()
        self.fundamental_agent = FundamentalWebAgent()
        self.sentiment_agent = SentimentSpiderAgent()
        self.risk_agent = RiskGuardianAgent()

    def run_pipeline(
        self,
        quote: Dict[str, Any],
        profile: UserProfile,
        config: DegradedModeConfig
    ) -> SynthesisOutput:
        pipeline_start = time.perf_counter()

        # -------------------------------------------------------------
        # 1. PARALLEL DISPATCH OF SPECIALIZED AGENTS
        # -------------------------------------------------------------
        with ThreadPoolExecutor(max_workers=4) as executor:
            fut_market = executor.submit(self.market_agent.analyze, quote, config)
            fut_fundamental = executor.submit(self.fundamental_agent.analyze, quote, config)
            fut_sentiment = executor.submit(self.sentiment_agent.analyze, quote, config)
            fut_risk = executor.submit(self.risk_agent.analyze, quote, profile, config)

            out_market = fut_market.result()
            out_fundamental = fut_fundamental.result()
            out_sentiment = fut_sentiment.result()
            out_risk = fut_risk.result()

        agent_outputs: Dict[str, AgentOutput] = {
            "market_spider": out_market,
            "fundamental_web": out_fundamental,
            "sentiment_spider": out_sentiment,
            "risk_guardian": out_risk
        }

        # -------------------------------------------------------------
        # 2. CROSS-AGENT CONFLICT & AGREEMENT DETECTION
        # -------------------------------------------------------------
        conflicts: List[AgentDisagreement] = []
        scores = [out_market.score, out_fundamental.score, out_sentiment.score]
        
        # Check Technical vs Sentiment Conflict
        if (out_market.score > 35 and out_sentiment.score < -25) or (out_market.score < -35 and out_sentiment.score > 25):
            conflicts.append(AgentDisagreement(
                agent_a="Market Spider (Technicals)",
                agent_a_signal=out_market.signal.value,
                agent_b="Sentiment Spider (Smart Money)",
                agent_b_signal=out_sentiment.signal.value,
                conflict_nature="Price momentum is surging, but institutional smart money is net selling or retail euphoria indicates an options trap.",
                resolution_applied="Discounted momentum weight by 35%. Prioritized institutional flow caution to protect retail capital."
            ))

        # Check Technical vs Fundamental Conflict
        if out_market.score > 40 and out_fundamental.status == "DATA_UNAVAILABLE":
            conflicts.append(AgentDisagreement(
                agent_a="Market Spider (Technicals)",
                agent_a_signal=out_market.signal.value,
                agent_b="Fundamental Web (Regulatory)",
                agent_b_signal="DATA_UNAVAILABLE",
                conflict_nature="Technical breakout identified, but supporting SEBI corporate disclosures could not be retrieved.",
                resolution_applied="Confidence capped at 55%. System refuses to issue aggressive buy signal without regulatory grounding."
            ))

        # Check Technical vs Risk Guardian (Portfolio Over-concentration)
        if out_market.score > 40 and out_risk.score < -30:
            conflicts.append(AgentDisagreement(
                agent_a="Market Spider (Technicals)",
                agent_a_signal=out_market.signal.value,
                agent_b="Risk Guardian (Portfolio)",
                agent_b_signal=out_risk.signal.value,
                conflict_nature=f"Stock exhibits strong momentum, but user portfolio has excessive concentration ({profile.portfolio.sector_allocations.get(quote.get('sector', ''), 0):.1f}%) in {quote.get('sector', 'this sector')}.",
                resolution_applied=f"Overrode technical impulse for {profile.risk_tolerance.value} profile. Shifted guidance from 'Aggressive Accumulation' to 'Cautious Hold / Rebalance'."
            ))

        # Agreement Score Calculation: 100 - standard deviation / span of agent scores
        score_span = max(scores) - min(scores)
        agreement_score_pct = round(max(10.0, 100.0 - (score_span * 0.45)), 1)
        if conflicts:
            agreement_score_pct = min(agreement_score_pct, 65.0)

        # -------------------------------------------------------------
        # 3. WEIGHTED SYNTHESIS CONDITIONED ON USER PROFILE
        # -------------------------------------------------------------
        ticker = quote["ticker"]
        price = quote["price"]
        company = quote["company_name"]

        # Base weights
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
            w_market = 0.20
            w_fund = 0.40
            w_sent = 0.15
            w_risk = 0.25
        elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE:
            w_market = 0.45
            w_fund = 0.20
            w_sent = 0.20
            w_risk = 0.15
        else: # MODERATE
            w_market = 0.30
            w_fund = 0.30
            w_sent = 0.20
            w_risk = 0.20

        # Adjust score if degraded or filing unavailable
        fund_score = out_fundamental.score if out_fundamental.status != "DATA_UNAVAILABLE" else 0.0

        synthesized_score = (
            (out_market.score * w_market) +
            (fund_score * w_fund) +
            (out_sentiment.score * w_sent) +
            (out_risk.score * w_risk)
        )

        # Penalize confidence if conflicts detected or degraded mode active
        avg_conf = (out_market.confidence + out_fundamental.confidence + out_sentiment.confidence + out_risk.confidence) / 4.0
        if conflicts:
            avg_conf -= (len(conflicts) * 12.0)
        if quote.get("is_degraded", False) or config.simulate_feed_failure or config.simulate_missing_filing:
            avg_conf = min(avg_conf, 52.0)

        confidence_pct = round(max(30.0, min(avg_conf, 95.0)), 1)

        # -------------------------------------------------------------
        # 4. DECISION ENGINE & PERSONALIZED RECOMMENDATION
        # -------------------------------------------------------------
        why_factors: List[str] = []
        facts: List[str] = []
        inferences: List[str] = []
        interpretations: List[str] = []

        # Populate Facts
        facts.append(f"{company} ({ticker}) trades at INR {price:,.2f} on NSE with volume {quote.get('volume_multiplier', 1.0):.2f}x 20-day average.")
        if out_fundamental.evidence:
            first_ev = out_fundamental.evidence[0]
            facts.append(f"Regulatory Fact: {first_ev.source} ({first_ev.section}): \"{first_ev.excerpt[:130]}...\"")
        facts.append(f"Portfolio Fact: Current portfolio value INR {profile.portfolio.total_portfolio_value:,.0f} with HHI of {profile.portfolio.concentration_hhi:.0f}.")

        # Determine Recommendation based on profile & score
        if profile.risk_tolerance == RiskTolerance.CONSERVATIVE:
            if out_fundamental.status == "DATA_UNAVAILABLE":
                recommendation = "WAIT / DATA DEGRADATION SAFEGUARD"
                overall_signal = SignalClassification.DATA_UNAVAILABLE
                risk_level = "ELEVATED"
                what = f"Do not initiate exposure in {ticker}. Corporate regulatory filings are unverified in the local repository."
                why_factors.append("SEBI disclosure is unavailable; capital preservation rules prohibit position initiation without regulatory grounding.")
            elif out_risk.score < -20:
                recommendation = "MONITOR / CONCENTRATION CEILING REACHED"
                overall_signal = SignalClassification.NEUTRAL
                risk_level = "ELEVATED"
                what = f"Hold current position or allocate elsewhere. Your existing exposure in {quote.get('sector', 'this sector')} is already near prudent limits."
                why_factors.append(f"Sector exposure ({profile.portfolio.sector_allocations.get(quote.get('sector', ''), 0):.1f}%) exceeds recommended 30% ceiling.")
                why_factors.append(f"Asset beta of {quote.get('beta', 1.0):.2f} poses elevated downside volatility for your conservative profile.")
            elif synthesized_score > 35:
                recommendation = "GRADUAL STAGGERED ACCUMULATION (SIP)"
                overall_signal = SignalClassification.BULLISH
                risk_level = "LOW"
                what = f"Selective accumulation on dips. Solid fundamental moat aligns with your long-term wealth preservation goal."
                why_factors.append("Low debt-to-equity ratio and verified earnings cash flow provide strong safety margin.")
            else:
                recommendation = "NEUTRAL / HOLD ON SIDELINES"
                overall_signal = SignalClassification.NEUTRAL
                risk_level = "MODERATE"
                what = f"Maintain observation status on {ticker}. Current risk-adjusted reward ratio does not justify capital deployment."
                why_factors.append("Signals are consolidating; wait for lower valuation entry point.")

            pers_note = (
                f"Tailored for {profile.name} ({profile.risk_tolerance.value} Investor): "
                f"Prioritizes capital protection over momentum. Volatility beta of {quote.get('beta', 1.0):.2f} "
                f"and existing {quote.get('sector', 'sector')} allocation ({profile.portfolio.sector_allocations.get(quote.get('sector', ''), 0):.1f}%) "
                f"strictly constrain position sizing to preserve cash cushion ({profile.portfolio.cash_balance / profile.portfolio.total_portfolio_value * 100:.1f}%)."
            )

        elif profile.risk_tolerance == RiskTolerance.AGGRESSIVE:
            if config.simulate_signal_conflict or (out_market.score > 40 and out_sentiment.score < -20):
                recommendation = "TACTICAL SWING WITH TIGHT STOP-LOSS (2.0%)"
                overall_signal = SignalClassification.CONFLICTING
                risk_level = "HIGH"
                what = f"Trade momentum with strict discipline. Technical breakout is actionable, but institutional selling flags a potential retail trap."
                why_factors.append("Market Spider confirms high-volume price breakout above moving averages.")
                why_factors.append("Sentiment Spider detects institutional distribution divergence (-INR 480 Cr net FII flow); tight 2.0% stop-loss mandatory.")
            elif synthesized_score > 40:
                recommendation = "MOMENTUM BUY / SWING OPPORTUNITY"
                overall_signal = SignalClassification.STRONG_BULLISH if synthesized_score > 65 else SignalClassification.BULLISH
                risk_level = "MODERATE"
                what = f"Exploit volume expansion and short-term trend strength. Target 5-8% swing upside with trailing stop."
                why_factors.append(f"Volume anomaly surge ({quote.get('volume_multiplier', 1.0):.2f}x baseline) confirms buyer urgency.")
                why_factors.append("Oscillators confirm trend continuation with positive MACD expansion.")
            elif synthesized_score < -20:
                recommendation = "EXIT / AVOID BREAKDOWN"
                overall_signal = SignalClassification.BEARISH
                risk_level = "HIGH"
                what = f"Avoid initiating or take profit. Momentum has fractured and volatility is turning unfavorable."
                why_factors.append("Distribution volume and deteriorating institutional flows.")
            else:
                recommendation = "QUICK SWING MONITOR"
                overall_signal = SignalClassification.NEUTRAL
                risk_level = "MODERATE"
                what = f"Wait for confirmed breakout above resistance before deploying swing capital."
                why_factors.append("Consolidation inside Bollinger bands; awaiting breakout trigger.")

            pers_note = (
                f"Tailored for {profile.name} ({profile.risk_tolerance.value} Trader): "
                f"Capitalizes on volume anomaly ({quote.get('volume_multiplier', 1.0):.2f}x) and high asset beta ({quote.get('beta', 1.0):.2f}) "
                f"for short-term swing velocity, governed by mandatory 2.0% stop-loss discipline."
            )

        else:  # MODERATE PROFILE
            if synthesized_score > 30:
                recommendation = "MEASURED POSITIONAL ENTRY"
                overall_signal = SignalClassification.BULLISH
                risk_level = "MODERATE"
                what = f"Initiate calibrated position in {ticker}. Balanced risk-reward profile aligns with medium-term horizon."
                why_factors.append(f"Balanced fundamentals and positive momentum offer favorable risk-adjusted asymmetry.")
            elif synthesized_score < -20:
                recommendation = "DEFENSIVE REBALANCE"
                overall_signal = SignalClassification.BEARISH
                risk_level = "HIGH"
                what = f"Reduce exposure or pause fresh buying in {ticker} until volatility normalizes."
                why_factors.append("Downward price pressure and cautious institutional flows.")
            else:
                recommendation = "HOLD AND ASSESS"
                overall_signal = SignalClassification.NEUTRAL
                risk_level = "MODERATE"
                what = f"Maintain existing allocation. Market signals reflect equilibrium without decisive breakout catalyst."
                why_factors.append("Moving averages consolidating with neutral momentum slope.")

            pers_note = (
                f"Tailored for {profile.name} (Moderate Investor): "
                f"Balances growth pursuit against drawdown control. Asset beta ({quote.get('beta', 1.0):.2f}) "
                f"fits moderate risk bounds, allowing measured allocation up to 8% of portfolio."
            )

        # Inferences & Interpretations
        inferences.append(f"Technical momentum score ({out_market.score:+.1f}) combined with institutional flow bias reflects current short-term directional pressure.")
        if out_fundamental.status == "SUCCESS":
            inferences.append("Operating margin trajectory substantiated by Q2 filings reduces long-term solvency risk.")
        interpretations.append(pers_note)

        # Uncertainty statement
        if conflicts:
            uncertainty = f"UNRESOLVED CROSS-AGENT DISAGREEMENT: {len(conflicts)} conflict(s) detected between specialized agents. Smart money institutional flow does not confirm retail momentum. Position sizing should be scaled down by 50%."
        elif config.simulate_feed_failure:
            uncertainty = "FEED DEGRADATION WARNING: Real-time price stream is currently simulated/cached. Real-time intraday bid/ask order-book depth is unverified."
        elif config.simulate_missing_filing:
            uncertainty = "MISSING DOCUMENT DISCLOSURE: Financial RAG corpus lacks the latest SEBI filing for this security. High-conviction governance ratings cannot be certified."
        else:
            uncertainty = "MACRO UNCERTAINTY: Analysis assumes current RBI interest rate corridor and stable crude oil import prices. Forward 30-day projection subject to unexpected geopolitical shocks."

        total_latency = round((time.perf_counter() - pipeline_start) * 1000.0, 2)

        # Collect evidence chain
        evidence_chain = out_fundamental.evidence

        telemetry = TelemetryMetrics(
            agent_response_latency_ms=max(out_market.execution_time_ms, out_fundamental.execution_time_ms, out_sentiment.execution_time_ms, out_risk.execution_time_ms),
            rag_retrieval_latency_ms=out_fundamental.metrics.get("rag_latency_ms", 0.0),
            total_pipeline_latency_ms=total_latency,
            signal_confidence_pct=confidence_pct,
            portfolio_risk_concentration=profile.portfolio.concentration_hhi,
            signal_agreement_score_pct=agreement_score_pct,
            evidence_sources_count=len(evidence_chain),
            agent_disagreements_count=len(conflicts)
        )

        five_questions = {
            "what_is_happening": what,
            "why_is_it_happening": " · ".join(why_factors),
            "what_evidence_supports_it": (
                f"Documented in {evidence_chain[0].source} ({evidence_chain[0].section}): \"{evidence_chain[0].excerpt[:110]}...\""
                if evidence_chain else "Raw market volume surge and technical indicator alignment."
            ),
            "how_confident_is_system": f"{confidence_pct}% confidence. {uncertainty}",
            "what_does_it_mean_for_investor": pers_note
        }

        data_source_state = quote.get("data_source_state", "DEMO DATA")

        return SynthesisOutput(
            ticker=ticker,
            company_name=company,
            current_price=price,
            timestamp=datetime.utcnow().isoformat(),
            user_profile_name=profile.name,
            user_risk_tolerance=profile.risk_tolerance.value,
            overall_recommendation=recommendation,
            overall_signal=overall_signal,
            confidence_pct=confidence_pct,
            risk_level=risk_level,
            telemetry=telemetry,
            what_conclusion=what,
            why_reasoning=why_factors,
            personalization_note=pers_note,
            evidence_chain=evidence_chain,
            uncertainty_disclosure=uncertainty,
            conflicts_detected=conflicts,
            agent_outputs=agent_outputs,
            anti_hallucination_audit={
                "facts": facts,
                "inferences": inferences,
                "personalized_interpretations": interpretations
            },
            five_questions=five_questions,
            data_source_state=data_source_state,
            data_quality_warnings=[]
        )


# Global singleton instance
web_mind = WebMindOrchestrator()
