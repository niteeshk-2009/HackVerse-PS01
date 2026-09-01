"""
SPY THE MARKET: AI-Powered Financial Intelligence
FastAPI Main Application & REST API Endpoints with strict HTTP semantics.
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from spidersense.agents.base import DegradedModeConfig
from spidersense.market_data.provider import provider_manager
from spidersense.profiler.profiles import get_profile, register_custom_profile, USER_PROFILES
from spidersense.agents.web_mind import web_mind
from spidersense.rag.engine import rag_engine
from spidersense.telemetry.logger import telemetry_logger

app = FastAPI(
    title="SPY THE MARKET: AI-Powered Financial Intelligence",
    description="Autonomous Multi-Agent Financial Intelligence Platform for Retail Investors (PS-01)",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AnalysisRequest(BaseModel):
    ticker: str = Field(default="TATAMOTORS", description="Equity ticker symbol (e.g. TATAMOTORS, RELIANCE)")
    profile_id: str = Field(default="conservative", description="User profile ID (conservative, aggressive, custom)")
    simulate_feed_failure: bool = False
    simulate_missing_filing: bool = False
    simulate_signal_conflict: bool = False


class CustomProfileRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(default=28, ge=18, le=100)
    risk_tolerance: str = Field(default="Moderate")
    investment_horizon: str = Field(default="Medium-Term (1-3 Years)")
    capital_inr: float = Field(default=500000.0, gt=0)
    primary_goal: str = Field(default="Wealth Creation")


class ModeChangeRequest(BaseModel):
    mode: str = Field(..., description="'DEMO' or 'LIVE'")


@app.get("/api/health", status_code=status.HTTP_200_OK)
def health_check():
    provider = provider_manager.get_provider()
    return {
        "status": "healthy",
        "product": "SPY THE MARKET",
        "subtitle": "AI-Powered Financial Intelligence",
        "system": "Multi-Agent Synthesis Engine",
        "agents_active": 4,
        "rag_status": "READY",
        "data_mode": provider_manager.current_mode,
        "data_state": provider.data_state.value
    }


@app.get("/api/settings", status_code=status.HTTP_200_OK)
def get_settings():
    provider = provider_manager.get_provider()
    return {
        "product_name": "SPY THE MARKET",
        "subtitle": "AI-Powered Financial Intelligence",
        "data_mode": provider_manager.current_mode,
        "data_state": provider.data_state.value,
        "active_universe": ["TATAMOTORS", "RELIANCE", "HDFCBANK", "ZOMATO", "INFY"],
        "disclaimer": "This product provides AI-generated financial intelligence for informational and educational purposes and is not financial advice."
    }


@app.post("/api/settings/mode", status_code=status.HTTP_200_OK)
def set_data_mode(req: ModeChangeRequest):
    try:
        updated_mode = provider_manager.set_mode(req.mode)
        provider = provider_manager.get_provider()
        return {
            "mode": updated_mode,
            "data_state": provider.data_state.value,
            "message": f"Data mode successfully set to {updated_mode}."
        }
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@app.get("/api/watchlist", status_code=status.HTTP_200_OK)
def get_watchlist():
    """Returns quotes for all tracked equities."""
    provider = provider_manager.get_provider()
    return provider.get_watchlist()


@app.get("/api/quote/{ticker}", status_code=status.HTTP_200_OK)
def get_quote(ticker: str):
    """Returns quote for a specific ticker with 404 on unknown symbol."""
    provider = provider_manager.get_provider()
    try:
        return provider.get_quote(ticker)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security '{ticker}' not found in active market universe."
        )


@app.get("/api/chart/{ticker}", status_code=status.HTTP_200_OK)
def get_chart(ticker: str, timeframe: str = Query("1D", pattern="^(1D|1W|1M|1Y)$")):
    """Returns time-series chart data (1D, 1W, 1M, 1Y)."""
    provider = provider_manager.get_provider()
    try:
        return provider.get_chart_data(ticker, timeframe=timeframe)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security '{ticker}' not found in active market universe."
        )


@app.get("/api/depth/{ticker}", status_code=status.HTTP_200_OK)
def get_depth(ticker: str):
    """Returns Top 5 Bids and Asks order-book depth."""
    provider = provider_manager.get_provider()
    try:
        return provider.get_market_depth(ticker)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security '{ticker}' not found in active market universe."
        )


@app.get("/api/profiles", status_code=status.HTTP_200_OK)
def get_profiles():
    """Returns list of investor behavioral profiles."""
    return {
        key: {
            "id": p.user_id,
            "name": p.name,
            "risk_tolerance": p.risk_tolerance.value,
            "investment_horizon": p.investment_horizon.value,
            "capital_inr": p.capital_inr,
            "concentration_hhi": p.portfolio.concentration_hhi,
            "behavioral_traits": p.behavioral_traits,
            "loss_aversion_score": p.loss_aversion_score
        }
        for key, p in USER_PROFILES.items()
    }


@app.get("/api/profile/{profile_id}", status_code=status.HTTP_200_OK)
def get_profile_detail(profile_id: str):
    """Returns detailed portfolio and risk state for a specific profile with 404 check."""
    clean_id = profile_id.lower().strip()
    if clean_id not in USER_PROFILES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investor profile '{profile_id}' not found."
        )
    return get_profile(clean_id)


@app.post("/api/profile/custom", status_code=status.HTTP_200_OK)
def create_custom_profile(req: CustomProfileRequest):
    """Registers a personalized user profile from onboarding inputs."""
    profile = register_custom_profile(
        name=req.name,
        age=req.age,
        risk_tolerance=req.risk_tolerance,
        investment_horizon=req.investment_horizon,
        capital_inr=req.capital_inr,
        primary_goal=req.primary_goal
    )
    return profile


@app.post("/api/analyze", status_code=status.HTTP_200_OK)
def run_analysis(req: AnalysisRequest):
    """
    Executes the full parallel multi-agent synthesis pipeline:
    Market Spider + Fundamental Web (RAG) + Sentiment Spider + Risk Guardian -> Spider Mind
    """
    provider = provider_manager.get_provider()
    try:
        quote = provider.get_quote(req.ticker, simulate_failure=req.simulate_feed_failure)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security '{req.ticker}' not found in active market universe."
        )

    clean_profile_id = req.profile_id.lower().strip()
    if clean_profile_id not in USER_PROFILES:
        clean_profile_id = "conservative"

    profile = get_profile(clean_profile_id)

    config = DegradedModeConfig(
        simulate_feed_failure=req.simulate_feed_failure,
        simulate_missing_filing=req.simulate_missing_filing,
        simulate_signal_conflict=req.simulate_signal_conflict
    )

    try:
        output = web_mind.run_pipeline(quote=quote, profile=profile, config=config)
        telemetry_logger.log_session(output)
        return output
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline synthesis error: {str(e)}"
        )


@app.post("/api/demo/compare_profiles", status_code=status.HTTP_200_OK)
def compare_profiles(ticker: str = "TATAMOTORS"):
    """
    Runs the exact same market input through both Conservative and Aggressive
    profiles simultaneously to demonstrate divergent personalized guidance.
    """
    provider = provider_manager.get_provider()
    try:
        quote = provider.get_quote(ticker)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Security '{ticker}' not found in active market universe."
        )

    config = DegradedModeConfig()
    prof_cons = get_profile("conservative")
    prof_aggr = get_profile("aggressive")

    out_cons = web_mind.run_pipeline(quote=quote, profile=prof_cons, config=config)
    out_aggr = web_mind.run_pipeline(quote=quote, profile=prof_aggr, config=config)

    return {
        "ticker": ticker,
        "company_name": quote["company_name"],
        "price": quote["price"],
        "conservative": out_cons,
        "aggressive": out_aggr
    }


@app.get("/api/compare", status_code=status.HTTP_200_OK)
def compare_investments(ticker_a: str = "TATAMOTORS", ticker_b: str = "RELIANCE", profile_id: str = "conservative"):
    """
    Head-to-head investment comparison between 2 securities evaluated through
    The Web Mind multi-agent synthesis conditioned on the user's risk profile.
    """
    provider = provider_manager.get_provider()
    try:
        quote_a = provider.get_quote(ticker_a)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Security '{ticker_a}' not found.")

    try:
        quote_b = provider.get_quote(ticker_b)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Security '{ticker_b}' not found.")

    profile = get_profile(profile_id)
    config = DegradedModeConfig()

    out_a = web_mind.run_pipeline(quote=quote_a, profile=profile, config=config)
    out_b = web_mind.run_pipeline(quote=quote_b, profile=profile, config=config)

    return {
        "stock_a": {
            "quote": quote_a,
            "synthesis": out_a
        },
        "stock_b": {
            "quote": quote_b,
            "synthesis": out_b
        },
        "user_profile": profile.name,
        "user_risk": profile.risk_tolerance.value
    }


@app.get("/api/evidence/{ticker}", status_code=status.HTTP_200_OK)
def get_evidence(ticker: str):
    """Returns RAG evidence chunks and regulatory citations for the Evidence Explorer."""
    evidence_list, latency = rag_engine.query(
        ticker=ticker,
        query_text=f"{ticker} quarterly revenue margins debt capex earnings SEBI regulatory disclosures",
        top_k=4
    )
    return {
        "ticker": ticker.upper(),
        "chunks_retrieved": len(evidence_list),
        "retrieval_latency_ms": latency,
        "evidence": evidence_list
    }


@app.get("/api/telemetry", status_code=status.HTTP_200_OK)
def get_telemetry():
    """Returns session telemetry metrics, latency tracking, and portfolio concentration logs."""
    return {
        "recent_sessions": telemetry_logger.get_recent_sessions(limit=8),
        "aggregate_stats": telemetry_logger.get_aggregate_stats()
    }


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the SPY THE MARKET interactive fintech cockpit."""
    html_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>SPY THE MARKET Dashboard Loading...</h1>")
