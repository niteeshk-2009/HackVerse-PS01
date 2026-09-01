"""
End-to-End Pipeline Acceptance Test for SPIDER-SENSE
Verifies the complete sequential chain specified in PS-01:
RAW INPUT -> DATA VALIDATION -> PARALLEL AGENTS -> RAG/EVIDENCE -> RISK/PERSONALIZATION -> CONFLICT ANALYSIS -> THE WEB MIND -> USER-FACING RESULT
"""

import sys
import os

_current_dir = os.path.dirname(os.path.abspath(__file__))
_repo_dir = os.path.dirname(_current_dir)
_parent_dir = os.path.dirname(_repo_dir)
sys.path.insert(0, _parent_dir)
sys.path.insert(0, _repo_dir)

from spidersense.market_data.provider import market_provider
from spidersense.agents.base import DegradedModeConfig, DataSourceState, RiskTolerance
from spidersense.profiler.profiles import get_profile
from spidersense.agents.web_mind import web_mind
from spidersense.telemetry.logger import telemetry_logger


def test_end_to_end_full_pipeline():
    """
    Executes full pipeline across all 8 stages and validates contract integrity.
    """
    # 1. RAW INPUT INGESTION
    ticker = "TATAMOTORS"
    raw_quote = market_provider.get_quote(ticker)
    assert raw_quote is not None
    assert raw_quote["ticker"] == "TATAMOTORS"
    assert raw_quote["price"] > 0
    assert market_provider.data_state == DataSourceState.DEMO_DATA

    # 2. DATA VALIDATION
    warnings = market_provider.validate_quote(raw_quote)
    assert isinstance(warnings, list)
    assert not any(w.severity == "CRITICAL" for w in warnings)

    # 3. PERSONALIZATION PROFILE SELECTION
    profile = get_profile("conservative")
    assert "CONSERVATIVE" in profile.user_id
    assert profile.risk_tolerance == RiskTolerance.CONSERVATIVE

    # 4. PARALLEL AGENTS & RAG EXECUTION (ORCHESTRATION VIA WEB MIND)
    config = DegradedModeConfig()
    synthesis = web_mind.run_pipeline(quote=raw_quote, profile=profile, config=config)

    # 5. VERIFY 4 SPECIALIZED AGENTS OUTPUT
    assert "market_spider" in synthesis.agent_outputs
    assert "fundamental_web" in synthesis.agent_outputs
    assert "sentiment_spider" in synthesis.agent_outputs
    assert "risk_guardian" in synthesis.agent_outputs

    # Check signal dimensions for Market Spider
    market_out = synthesis.agent_outputs["market_spider"]
    assert len(market_out.signals) >= 3
    valid_dims = ["Price Momentum", "Volume Anomaly", "Volatility & Oscillators", "FII / DII Institutional Flow"]
    for s in market_out.signals:
        assert s.dimension in valid_dims
        assert 0.0 <= s.confidence <= 100.0
        assert len(s.evidence_reasoning) > 0

    # 6. RAG EVIDENCE ATTRIBUTION
    assert len(synthesis.evidence_chain) >= 1
    primary_evidence = synthesis.evidence_chain[0]
    assert primary_evidence.source is not None
    assert primary_evidence.section is not None
    assert primary_evidence.excerpt is not None
    assert primary_evidence.relevance_score > 0.5

    # 7. CONFLICT RESOLUTION
    assert isinstance(synthesis.conflicts_detected, list)

    # 8. THE WEB MIND MASTER SYNTHESIS
    assert synthesis.overall_recommendation is not None
    assert 0.0 <= synthesis.confidence_pct <= 100.0
    assert len(synthesis.what_conclusion) > 0
    assert len(synthesis.why_reasoning) > 0
    assert len(synthesis.personalization_note) > 0

    # 9. TELEMETRY & LATENCY
    telemetry_logger.log_session(synthesis)
    assert synthesis.telemetry.total_pipeline_latency_ms > 0
    assert synthesis.telemetry.portfolio_risk_concentration > 0

    print("[PASS] End-to-end multi-agent pipeline verified successfully!")


if __name__ == "__main__":
    test_end_to_end_full_pipeline()
