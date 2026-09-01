"""
SPIDER-SENSE: Agent 3 — SENTIMENT SPIDER
Role: Sentiment & Flow Intelligence Analyst
Evaluates institutional flows (FII/DII net flows), news sentiment indicators,
and retail FOMO chasing patterns to expose retail traps and smart money divergences.
"""

import time
from typing import Dict, Any, List
from spidersense.agents.base import (
    AgentOutput, AgentSignal, SignalClassification, DegradedModeConfig
)


class SentimentSpiderAgent:
    def __init__(self):
        self.name = "Sentiment Spider"
        self.role = "Sentiment & Flow Intelligence Analyst"

    def analyze(self, quote: Dict[str, Any], config: DegradedModeConfig) -> AgentOutput:
        start_time = time.perf_counter()
        signals: List[AgentSignal] = []
        reasoning: List[str] = []
        risks: List[str] = []

        sentiment_score = quote.get("sentiment_score", 50.0)
        fii_flow = quote.get("fii_flow_crores", 0.0)
        retail_chase = quote.get("retail_chase_indicator", 50.0)

        # Injected conflict scenario for demo
        if config.simulate_signal_conflict:
            # Force bearish institutional sentiment to test conflict resolution against bullish technicals
            fii_flow = -480.0
            sentiment_score = 30.0
            retail_chase = 95.0

        # -------------------------------------------------------------
        # 1. INSTITUTIONAL FLOWS (FII / DII)
        # -------------------------------------------------------------
        if fii_flow > 200.0:
            flow_class = SignalClassification.STRONG_BULLISH
            flow_score = 80.0
            flow_conf = 85.0
            flow_reason = f"Institutional accumulation: Foreign Institutional Investors (FII) recorded net inflow of +INR {fii_flow:.1f} Crores in latest session."
        elif fii_flow < -100.0:
            flow_class = SignalClassification.BEARISH
            flow_score = -70.0
            flow_conf = 82.0
            flow_reason = f"Institutional distribution: FIIs offloaded -INR {abs(fii_flow):.1f} Crores, distributing into retail liquidity."
            risks.append(f"Institutional selling pressure: FIIs net sold INR {abs(fii_flow):.1f} Cr.")
        else:
            flow_class = SignalClassification.NEUTRAL
            flow_score = 10.0
            flow_conf = 70.0
            flow_reason = f"Neutral institutional participation: Net FII flows balanced at INR {fii_flow:.1f} Crores."

        signals.append(AgentSignal(
            dimension="Institutional Smart Money Flow",
            classification=flow_class,
            score=flow_score,
            confidence=flow_conf,
            evidence_reasoning=flow_reason
        ))
        reasoning.append(flow_reason)

        # -------------------------------------------------------------
        # 2. RETAIL SENTIMENT VS SMART MONEY DIVERGENCE
        # -------------------------------------------------------------
        if retail_chase > 80.0 and fii_flow < 0:
            # DIVERGENCE: Classic retail trap (SEBI F&O 89% loss warning)
            sent_class = SignalClassification.STRONG_BEARISH
            sent_score = -75.0
            sent_conf = 88.0
            sent_reason = f"⚡ RETAIL TRAP DIVERGENCE DETECTED: Retail call-buying euphoria ({retail_chase:.1f}/100) coincides with institutional liquidation (-INR {abs(fii_flow):.1f} Cr). High probability of distribution exhaustion."
            risks.append("Retail FOMO divergence: Retail traders chasing momentum while smart money unwinds.")
        elif sentiment_score >= 70.0:
            sent_class = SignalClassification.BULLISH
            sent_score = 70.0
            sent_conf = 78.0
            sent_reason = f"Broad market sentiment is positive ({sentiment_score:.1f}/100) supported by sectoral tailwinds and healthy breadth."
        elif sentiment_score <= 40.0:
            sent_class = SignalClassification.BEARISH
            sent_score = -55.0
            sent_conf = 75.0
            sent_reason = f"Deteriorating news sentiment ({sentiment_score:.1f}/100) reflecting macro caution and earnings multiple compression."
        else:
            sent_class = SignalClassification.NEUTRAL
            sent_score = 5.0
            sent_conf = 68.0
            sent_reason = f"Balanced sentiment: Public media & broker consensus is neutral ({sentiment_score:.1f}/100)."

        signals.append(AgentSignal(
            dimension="Sentiment & Divergence",
            classification=sent_class,
            score=sent_score,
            confidence=sent_conf,
            evidence_reasoning=sent_reason
        ))
        reasoning.append(sent_reason)

        overall_score = round((flow_score * 0.6) + (sent_score * 0.4), 1)
        overall_confidence = round((flow_conf + sent_conf) / 2.0, 1)

        if overall_score >= 50:
            overall_signal = SignalClassification.STRONG_BULLISH if overall_score >= 70 else SignalClassification.BULLISH
        elif overall_score <= -40:
            overall_signal = SignalClassification.STRONG_BEARISH if overall_score <= -65 else SignalClassification.BEARISH
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
                "sentiment_score": sentiment_score,
                "fii_flow_crores": fii_flow,
                "retail_chase_indicator": retail_chase,
                "divergence_flagged": (retail_chase > 80 and fii_flow < 0)
            },
            execution_time_ms=execution_ms,
            data_source_state=quote.get("data_source_state", "DEMO DATA")
        )
