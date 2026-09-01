"""
SPIDER-SENSE: Agent 1 — MARKET SPIDER
Role: Technical & Market Momentum Intelligence
Evaluates market data across at least three independent dimensions:
1. Price Momentum (EMA 20/50/200, MACD histogram)
2. Volume Anomaly (Volume surge multiplier vs 20-day baseline, delivery %)
3. Volatility & Oscillators (RSI-14, ATR, Beta)
"""

import time
from typing import Dict, Any, List
from spidersense.agents.base import (
    AgentOutput, AgentSignal, SignalClassification, DegradedModeConfig
)


class MarketSpiderAgent:
    def __init__(self):
        self.name = "Market Spider"
        self.role = "Technical & Market Momentum Analyst"

    def analyze(self, quote: Dict[str, Any], config: DegradedModeConfig) -> AgentOutput:
        start_time = time.perf_counter()
        signals: List[AgentSignal] = []
        reasoning: List[str] = []
        risks: List[str] = []
        
        is_degraded = quote.get("is_degraded", False) or config.simulate_feed_failure
        status = "WARNING" if is_degraded else "SUCCESS"

        # -------------------------------------------------------------
        # DIMENSION 1: PRICE MOMENTUM
        # -------------------------------------------------------------
        price = quote["price"]
        ema_20 = quote["ema_20"]
        ema_50 = quote["ema_50"]
        ema_200 = quote["ema_200"]
        macd_hist = quote["macd_histogram"]

        if price > ema_20 > ema_50 > ema_200 and macd_hist > 0:
            p_class = SignalClassification.STRONG_BULLISH
            p_score = 85.0
            p_conf = 88.0
            p_reason = f"Golden alignment: Price (INR {price}) is trading above 20 EMA ({ema_20}), 50 EMA ({ema_50}), and 200 EMA ({ema_200}) with positive MACD histogram (+{macd_hist})."
        elif price > ema_20 and macd_hist >= 0:
            p_class = SignalClassification.BULLISH
            p_score = 65.0
            p_conf = 78.0
            p_reason = f"Short-term momentum positive: Price (INR {price}) holds above 20-day EMA with expanding MACD histogram."
        elif price < ema_20 and price < ema_50:
            p_class = SignalClassification.BEARISH
            p_score = -60.0
            p_conf = 75.0
            p_reason = f"Breakdown below moving average cluster: Price trades below 20 EMA and 50 EMA."
        else:
            p_class = SignalClassification.NEUTRAL
            p_score = 10.0
            p_conf = 65.0
            p_reason = f"Consolidation range: Price is oscillating between 20 EMA ({ema_20}) and 50 EMA ({ema_50})."

        signals.append(AgentSignal(
            dimension="Price Momentum",
            classification=p_class,
            score=p_score,
            confidence=p_conf,
            evidence_reasoning=p_reason
        ))
        reasoning.append(p_reason)

        # -------------------------------------------------------------
        # DIMENSION 2: VOLUME ANOMALY
        # -------------------------------------------------------------
        vol_multiplier = quote["volume_multiplier"]
        delivery_pct = quote["delivery_pct"]

        if vol_multiplier >= 1.5 and delivery_pct >= 45.0:
            v_class = SignalClassification.STRONG_BULLISH
            v_score = 80.0
            v_conf = 84.0
            v_reason = f"Institutional accumulation anomaly: Trading volume is {vol_multiplier:.2f}x the 20-day average with {delivery_pct:.1f}% delivery-backed absorption."
        elif vol_multiplier >= 1.5 and delivery_pct < 40.0:
            v_class = SignalClassification.BULLISH
            v_score = 45.0
            v_conf = 70.0
            v_reason = f"Speculative volume spike ({vol_multiplier:.2f}x avg) with low delivery ({delivery_pct:.1f}%), indicating high intraday speculative churning."
            risks.append("Intraday speculative churn dominates volume without high delivery backing.")
        elif vol_multiplier < 0.8:
            v_class = SignalClassification.NEUTRAL
            v_score = -10.0
            v_conf = 68.0
            v_reason = f"Subdued trading volume ({vol_multiplier:.2f}x avg) indicates lack of institutional participation."
        else:
            v_class = SignalClassification.BULLISH if quote["change_pct"] > 0 else SignalClassification.NEUTRAL
            v_score = 30.0 if quote["change_pct"] > 0 else 0.0
            v_conf = 72.0
            v_reason = f"Steady liquidity: Volume is consistent with historical norms ({vol_multiplier:.2f}x) and {delivery_pct:.1f}% delivery."

        signals.append(AgentSignal(
            dimension="Volume Anomaly",
            classification=v_class,
            score=v_score,
            confidence=v_conf,
            evidence_reasoning=v_reason
        ))
        reasoning.append(v_reason)

        # -------------------------------------------------------------
        # DIMENSION 3: VOLATILITY & OSCILLATORS
        # -------------------------------------------------------------
        rsi = quote["rsi_14"]
        beta = quote["beta"]

        if rsi > 72.0:
            osc_class = SignalClassification.BEARISH
            osc_score = -35.0
            osc_conf = 76.0
            osc_reason = f"Overbought warning: 14-day RSI has reached {rsi:.1f}. Mean-reversion or cooling pullback expected."
            risks.append(f"RSI oscillator ({rsi:.1f}) in overbought exhaustion territory.")
        elif rsi < 32.0:
            osc_class = SignalClassification.BULLISH
            osc_score = 55.0
            osc_conf = 74.0
            osc_reason = f"Oversold bounce setup: RSI at {rsi:.1f} indicates deep exhaustion among sellers."
        else:
            osc_class = SignalClassification.BULLISH if rsi > 50 else SignalClassification.NEUTRAL
            osc_score = 25.0 if rsi > 50 else 0.0
            osc_conf = 70.0
            osc_reason = f"Constructive oscillator band: RSI is balanced at {rsi:.1f} with beta of {beta:.2f}."

        signals.append(AgentSignal(
            dimension="Volatility & Oscillators",
            classification=osc_class,
            score=osc_score,
            confidence=osc_conf,
            evidence_reasoning=osc_reason
        ))
        reasoning.append(osc_reason)

        # -------------------------------------------------------------
        # AGENT AGGREGATION & DEGRADED PENALTY
        # -------------------------------------------------------------
        overall_score = round((p_score * 0.45) + (v_score * 0.35) + (osc_score * 0.20), 1)
        base_confidence = round(sum(s.confidence for s in signals) / len(signals), 1)

        if is_degraded:
            # Drop confidence significantly and add explicit degradation reason
            overall_confidence = round(base_confidence * 0.60, 1)  # Penalize by 40%
            reasoning.insert(0, f"⚠ DEGRADED DATA MODE: Live feed unavailable. Fallback to cached snapshot. Confidence penalized from {base_confidence}% to {overall_confidence}%.")
            risks.append("Real-time tick data disconnected; technical breakouts cannot be certified in real time.")
        else:
            overall_confidence = base_confidence

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
            status=status,
            signal=overall_signal,
            score=overall_score,
            confidence=overall_confidence,
            signals=signals,
            reasoning=reasoning,
            evidence=[],  # Market spider relies on raw market tick feed, not text RAG
            risks=risks,
            metrics={
                "rsi_14": rsi,
                "volume_multiplier": vol_multiplier,
                "beta": beta,
                "price": price,
                "is_feed_live": not is_degraded
            },
            execution_time_ms=execution_ms,
            data_source_state=quote.get("data_source_state", "DEMO DATA")
        )
