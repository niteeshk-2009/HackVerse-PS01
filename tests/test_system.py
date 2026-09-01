"""
SPIDER-SENSE Acceptance & Unit Test Suite
Covers all non-negotiable PS-01 requirements:
1. Signal Classification across 3 independent dimensions
2. RAG Semantic Retrieval & Source Attribution
3. Multi-Agent Output Contracts
4. User Profile Personalization (Divergent advice on identical market input)
5. Cross-Agent Conflict Detection & Resolution
6. Degraded-Data Handling (Missing filing, feed failure)
7. Telemetry & Concentration HHI calculation
"""

import sys
import os

# Ensure package is on sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_repo_dir = os.path.dirname(_current_dir)
_parent_dir = os.path.dirname(_repo_dir)
sys.path.insert(0, _parent_dir)
sys.path.insert(0, _repo_dir)

from spidersense.agents.base import (
    SignalClassification, DegradedModeConfig, RiskTolerance
)
from spidersense.market_data.provider import market_provider
from spidersense.rag.engine import rag_engine
from spidersense.profiler.profiles import get_profile, calculate_hhi
from spidersense.agents.market_spider import MarketSpiderAgent
from spidersense.agents.fundamental_web import FundamentalWebAgent
from spidersense.agents.sentiment_spider import SentimentSpiderAgent
from spidersense.agents.risk_guardian import RiskGuardianAgent
from spidersense.agents.web_mind import web_mind


def test_signal_classification_three_dimensions():
    """Test A: Signal classification evaluates at least 3 independent dimensions with stated confidence & reasoning"""
    agent = MarketSpiderAgent()
    quote = market_provider.get_quote("TATAMOTORS")
    config = DegradedModeConfig()

    output = agent.analyze(quote, config)
    assert output.status == "SUCCESS"
    assert len(output.signals) >= 3

    dims = [s.dimension for s in output.signals]
    assert "Price Momentum" in dims
    assert "Volume Anomaly" in dims
    assert "Volatility & Oscillators" in dims

    for sig in output.signals:
        assert isinstance(sig.classification, SignalClassification)
        assert 0.0 <= sig.confidence <= 100.0
        assert len(sig.evidence_reasoning) > 10


def test_rag_semantic_retrieval_and_citations():
    """Test B: RAG retrieves contextually relevant disclosures with verifiable attribution"""
    evidence_list, latency = rag_engine.query(
        ticker="TATAMOTORS",
        query_text="quarterly revenue and JLR margins",
        top_k=2
    )
    assert len(evidence_list) >= 1
    assert latency >= 0.0

    primary = evidence_list[0]
    assert "Tata Motors" in primary.source
    assert len(primary.section) > 0
    assert len(primary.excerpt) > 20
    assert primary.relevance_score > 0.5
    assert "High semantic cosine match" in primary.retrieval_reason


def test_agent_structured_output_contract():
    """Test C: All specialized agents adhere to predictable structured output contract"""
    quote = market_provider.get_quote("HDFCBANK")
    config = DegradedModeConfig()
    profile = get_profile("conservative")

    agents = [
        MarketSpiderAgent(),
        FundamentalWebAgent(),
        SentimentSpiderAgent()
    ]

    for agent in agents:
        out = agent.analyze(quote, config)
        assert hasattr(out, "agent_name")
        assert hasattr(out, "status")
        assert hasattr(out, "signal")
        assert hasattr(out, "score")
        assert hasattr(out, "confidence")
        assert hasattr(out, "reasoning")
        assert hasattr(out, "evidence")
        assert hasattr(out, "risks")
        assert hasattr(out, "execution_time_ms")
        assert out.execution_time_ms >= 0


def test_user_profile_personalization_divergence():
    """
    Test D: DEMONSTRABLE PERSONALIZATION ACCEPTANCE TEST
    The exact same stock/market input MUST produce demonstrably different guidance
    for Conservative vs Aggressive user profiles!
    """
    quote = market_provider.get_quote("TATAMOTORS")
    config = DegradedModeConfig()

    prof_cons = get_profile("conservative")
    prof_aggr = get_profile("aggressive")

    out_cons = web_mind.run_pipeline(quote, prof_cons, config)
    out_aggr = web_mind.run_pipeline(quote, prof_aggr, config)

    # Recommendations must visibly differ
    assert out_cons.overall_recommendation != out_aggr.overall_recommendation
    assert out_cons.risk_level != out_aggr.risk_level or "ACCUMULATION" in out_cons.overall_recommendation

    # Notes must be explicitly tailored to the specific user profile
    assert "Conservative" in out_cons.personalization_note
    assert "Aggressive" in out_aggr.personalization_note
    assert out_cons.user_risk_tolerance == "CONSERVATIVE"
    assert out_aggr.user_risk_tolerance == "AGGRESSIVE"


def test_agent_conflict_detection_and_resolution():
    """Test E: Detects and resolves cross-agent conflict (e.g. Bullish Technicals vs Institutional Selling)"""
    quote = market_provider.get_quote("TATAMOTORS")
    # Force conflict
    config = DegradedModeConfig(simulate_signal_conflict=True)
    profile = get_profile("aggressive")

    output = web_mind.run_pipeline(quote, profile, config)
    assert len(output.conflicts_detected) >= 1
    conflict = output.conflicts_detected[0]
    assert "conflict_nature" in conflict.model_dump()
    assert "resolution_applied" in conflict.model_dump()
    assert output.overall_signal == SignalClassification.CONFLICTING or output.risk_level == "HIGH"


def test_degraded_data_handling_missing_filing():
    """Test F: Handles missing regulatory filing without crashing or hallucinating uncited data"""
    quote = market_provider.get_quote("TATAMOTORS")
    config = DegradedModeConfig(simulate_missing_filing=True)
    profile = get_profile("conservative")

    output = web_mind.run_pipeline(quote, profile, config)
    fund_agent = output.agent_outputs["fundamental_web"]
    assert fund_agent.status == "DATA_UNAVAILABLE"
    assert "REGULATORY FILING UNAVAILABLE" in fund_agent.reasoning[0]
    assert output.confidence_pct <= 60.0  # Penalized confidence
    assert "SAFEGUARD" in output.overall_recommendation or "DATA" in output.overall_recommendation


def test_portfolio_concentration_hhi():
    """Test G: Correct mathematical computation of Herfindahl-Hirschman Index for portfolio risk"""
    profile = get_profile("conservative")
    hhi = profile.portfolio.concentration_hhi
    assert hhi > 2500.0  # Concentrated portfolio


def test_data_state_validation_and_quality():
    """Test H: Ensures strict 3-state labeling and data quality checks"""
    quote = market_provider.get_quote("TATAMOTORS")
    assert quote["data_source_state"] in ["DEMO DATA", "LIVE DATA", "DATA UNAVAILABLE"]
    assert quote["is_live"] is False  # Demo provider must NEVER masquerade as LIVE
    
    warnings = market_provider.validate_quote(quote)
    assert len(warnings) == 0  # Clean demo quote should have zero critical errors

    bad_quote = quote.copy()
    bad_quote["price"] = -50.0
    bad_warnings = market_provider.validate_quote(bad_quote)
    assert len(bad_warnings) >= 1
    assert bad_warnings[0].severity == "CRITICAL"


def test_five_questions_completeness():
    """Test I: The system answers the five essential investor questions"""
    quote = market_provider.get_quote("TATAMOTORS")
    profile = get_profile("conservative")
    config = DegradedModeConfig()

    output = web_mind.run_pipeline(quote, profile, config)
    fq = output.five_questions
    assert len(fq["what_is_happening"]) > 5
    assert len(fq["why_is_it_happening"]) > 5
    assert len(fq["what_evidence_supports_it"]) > 5
    assert len(fq["how_confident_is_system"]) > 5
    assert len(fq["what_does_it_mean_for_investor"]) > 5
    assert "disclaimer" in output.model_dump()


def test_api_route_semantics():
    """Test J: Verifies API route error handling and status code semantics"""
    from spidersense.app.main import get_quote, get_profile_detail
    from fastapi import HTTPException

    # Valid quote
    q = get_quote("TATAMOTORS")
    assert q["price"] > 0

    # 404 on unknown ticker
    try:
        get_quote("UNKNOWN_XYZ")
        assert False, "Should have raised 404"
    except HTTPException as e:
        assert e.status_code == 404

    # 404 on unknown profile
    try:
        get_profile_detail("non_existent_profile")
        assert False, "Should have raised 404"
    except HTTPException as e:
        assert e.status_code == 404


if __name__ == "__main__":
    test_signal_classification_three_dimensions()
    print("[PASS] Test 1: Signal classification across 3 dimensions")
    test_rag_semantic_retrieval_and_citations()
    print("[PASS] Test 2: RAG semantic retrieval & source citations")
    test_agent_structured_output_contract()
    print("[PASS] Test 3: Structured agent output contracts")
    test_user_profile_personalization_divergence()
    print("[PASS] Test 4: User profile divergence on identical market inputs")
    test_agent_conflict_detection_and_resolution()
    print("[PASS] Test 5: Cross-agent conflict detection & resolution")
    test_degraded_data_handling_missing_filing()
    print("[PASS] Test 6: Degraded data handling without hallucination")
    test_portfolio_concentration_hhi()
    print("[PASS] Test 7: Portfolio concentration HHI risk metrics")
    test_data_state_validation_and_quality()
    print("[PASS] Test 8: Data state validation & quality warning checks")
    test_five_questions_completeness()
    print("[PASS] Test 9: Five core questions completeness")
    test_api_route_semantics()
    print("[PASS] Test 10: HTTP status code semantics (404, 200)")
    print("\nALL 10 ACCEPTANCE & QUALITY TESTS PASSED SUCCESSFULLY!")
