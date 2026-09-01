"""
SPIDER-SENSE: Autonomous Financial Intelligence System for Retail Investors
Typed Contracts and Data Models
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class DataSourceState(str, Enum):
    LIVE_DATA = "LIVE DATA"
    DEMO_DATA = "DEMO DATA"
    DATA_UNAVAILABLE = "DATA UNAVAILABLE"


class DataQualityWarning(BaseModel):
    field: str
    message: str
    severity: str = "WARNING"  # INFO, WARNING, CRITICAL


class SignalClassification(str, Enum):
    STRONG_BULLISH = "STRONG_BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    STRONG_BEARISH = "STRONG_BEARISH"
    CONFLICTING = "CONFLICTING"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"


class RiskTolerance(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"


class InvestmentHorizon(str, Enum):
    SHORT_TERM = "SHORT_TERM"   # Days - Weeks (Swing/Momentum)
    MEDIUM_TERM = "MEDIUM_TERM" # 1 - 6 Months (Positional)
    LONG_TERM = "LONG_TERM"     # 1+ Years (Wealth Accumulation)


class AgentEvidence(BaseModel):
    source: str = Field(..., description="Document source title, e.g., 'Q2 FY26 Earnings Disclosure'")
    section: str = Field(..., description="Section or page reference, e.g., 'Page 4, Management Discussion'")
    excerpt: str = Field(..., description="Direct factual text snippet extracted from filing/source")
    relevance_score: float = Field(..., description="Semantic retrieval similarity score (0.0 to 1.0)")
    retrieval_reason: str = Field(..., description="Why this evidence was retrieved for query")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentSignal(BaseModel):
    dimension: str = Field(..., description="Dimension: e.g. Price Momentum, Volume Anomaly, Sentiment, Volatility")
    classification: SignalClassification
    score: float = Field(..., description="Normalized score from -100 (Strong Bearish) to +100 (Strong Bullish)")
    confidence: float = Field(..., description="Confidence percentage (0.0 to 100.0)")
    evidence_reasoning: str = Field(..., description="Inspectable factual reasoning explaining this signal")


class AgentOutput(BaseModel):
    agent_name: str
    role: str
    status: str = Field(default="SUCCESS", description="SUCCESS, WARNING, or DATA_UNAVAILABLE")
    signal: SignalClassification
    score: float = Field(..., description="Overall agent score (-100 to +100)")
    confidence: float = Field(..., description="Overall confidence (0.0 to 100.0)")
    signals: List[AgentSignal] = Field(default_factory=list)
    reasoning: List[str] = Field(default_factory=list)
    evidence: List[AgentEvidence] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    data_source_state: DataSourceState = DataSourceState.DEMO_DATA
    data_quality_warnings: List[DataQualityWarning] = Field(default_factory=list)
    execution_time_ms: float = Field(default=0.0)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Holding(BaseModel):
    ticker: str
    company_name: str
    shares: int
    avg_price: float
    current_price: float
    current_value: float
    allocation_pct: float
    sector: str


class PortfolioState(BaseModel):
    total_portfolio_value: float
    cash_balance: float
    daily_pnl_inr: float
    daily_pnl_pct: float
    holdings: List[Holding]
    sector_allocations: Dict[str, float]
    concentration_hhi: float = Field(..., description="Herfindahl-Hirschman Index for portfolio risk (0-10000)")


class UserProfile(BaseModel):
    user_id: str
    name: str
    risk_tolerance: RiskTolerance
    investment_horizon: InvestmentHorizon
    capital_inr: float
    portfolio: PortfolioState
    watchlist: List[str]
    behavioral_traits: List[str] = Field(default_factory=list)
    loss_aversion_score: float = Field(default=50.0, description="0 (indifferent) to 100 (extreme loss aversion)")


class DegradedModeConfig(BaseModel):
    simulate_feed_failure: bool = False
    simulate_missing_filing: bool = False
    simulate_signal_conflict: bool = False


class AgentDisagreement(BaseModel):
    agent_a: str
    agent_a_signal: str
    agent_b: str
    agent_b_signal: str
    conflict_nature: str
    resolution_applied: str


class TelemetryMetrics(BaseModel):
    agent_response_latency_ms: float
    rag_retrieval_latency_ms: float
    total_pipeline_latency_ms: float
    signal_confidence_pct: float
    portfolio_risk_concentration: float
    signal_agreement_score_pct: float
    evidence_sources_count: int
    agent_disagreements_count: int


class SynthesisOutput(BaseModel):
    ticker: str
    company_name: str
    current_price: float
    timestamp: str
    user_profile_name: str
    user_risk_tolerance: str
    overall_recommendation: str  # e.g., "ACCUMULATE / CONTROLLED MOMENTUM BUY", "WAIT / HIGH VOLATILITY RISK"
    overall_signal: SignalClassification
    confidence_pct: float
    risk_level: str              # LOW, MODERATE, ELEVATED, HIGH
    telemetry: TelemetryMetrics
    what_conclusion: str         # The clear synthesized conclusion
    why_reasoning: List[str]     # Major contributing factors
    personalization_note: str    # Why this conclusion is tailored specifically for this investor profile
    evidence_chain: List[AgentEvidence]
    uncertainty_disclosure: str  # Explicit disclosure of missing data or market unknowns
    conflicts_detected: List[AgentDisagreement]
    agent_outputs: Dict[str, AgentOutput]
    anti_hallucination_audit: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "facts": [],
            "inferences": [],
            "personalized_interpretations": []
        }
    )
    five_questions: Dict[str, str] = Field(
        default_factory=lambda: {
            "what_is_happening": "",
            "why_is_it_happening": "",
            "what_evidence_supports_it": "",
            "how_confident_is_system": "",
            "what_does_it_mean_for_investor": ""
        }
    )
    data_source_state: DataSourceState = DataSourceState.DEMO_DATA
    data_quality_warnings: List[DataQualityWarning] = Field(default_factory=list)
    disclaimer: str = "This product provides AI-generated financial intelligence for informational and educational purposes and is not financial advice."
