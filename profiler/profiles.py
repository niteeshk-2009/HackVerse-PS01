"""
SPIDER-SENSE: User Profiling & Behavioral Intelligence Engine
Captures risk tolerance, portfolio composition, behavioral tendencies (FOMO chasing, loss aversion),
supports dynamic custom user onboarding, and computes real portfolio concentration metrics (HHI).
"""

from typing import Dict, List, Optional
from spidersense.agents.base import (
    UserProfile, PortfolioState, Holding, RiskTolerance, InvestmentHorizon
)


def calculate_hhi(holdings: List[Holding], cash_pct: float) -> float:
    """Calculates Herfindahl-Hirschman Index (0 - 10000) for portfolio concentration risk"""
    weights = [h.allocation_pct for h in holdings]
    if cash_pct > 0:
        weights.append(cash_pct)
    hhi = sum((w ** 2) for w in weights)
    return round(hhi, 1)


PROFILE_CONSERVATIVE = UserProfile(
    user_id="USER_CONSERVATIVE_01",
    name="Conservative Investor (Capital Preservation)",
    risk_tolerance=RiskTolerance.CONSERVATIVE,
    investment_horizon=InvestmentHorizon.LONG_TERM,
    capital_inr=1500000.0,
    watchlist=["HDFCBANK", "RELIANCE", "INFY", "TATAMOTORS"],
    behavioral_traits=[
        "High Loss Aversion",
        "Avoids Derivative / F&O Exposure",
        "Values Dividend Yield & Clean Balance Sheets",
        "Dislikes Overvalued High-Beta Stocks"
    ],
    loss_aversion_score=85.0,
    portfolio=PortfolioState(
        total_portfolio_value=1500000.0,
        cash_balance=375000.0,  # 25% cash
        daily_pnl_inr=5400.0,
        daily_pnl_pct=0.36,
        holdings=[
            Holding(
                ticker="HDFCBANK",
                company_name="HDFC Bank Ltd",
                shares=400,
                avg_price=1620.0,
                current_price=1692.0,
                current_value=676800.0,
                allocation_pct=45.12,
                sector="Banking & Financials"
            ),
            Holding(
                ticker="RELIANCE",
                company_name="Reliance Industries Ltd",
                shares=148,
                avg_price=2980.0,
                current_price=3024.0,
                current_value=447552.0,
                allocation_pct=29.84,
                sector="Energy & Conglomerate"
            )
        ],
        sector_allocations={
            "Banking & Financials": 45.12,
            "Energy & Conglomerate": 29.84,
            "Cash Reserve": 25.04
        },
        concentration_hhi=calculate_hhi([
            Holding(ticker="HDFCBANK", company_name="HDFC Bank", shares=400, avg_price=1620.0, current_price=1692.0, current_value=676800.0, allocation_pct=45.12, sector="Banking"),
            Holding(ticker="RELIANCE", company_name="Reliance", shares=148, avg_price=2980.0, current_price=3024.0, current_value=447552.0, allocation_pct=29.84, sector="Energy")
        ], 25.04)
    )
)

PROFILE_AGGRESSIVE = UserProfile(
    user_id="USER_AGGRESSIVE_02",
    name="Aggressive Investor (Growth & Momentum)",
    risk_tolerance=RiskTolerance.AGGRESSIVE,
    investment_horizon=InvestmentHorizon.SHORT_TERM,
    capital_inr=350000.0,
    watchlist=["ZOMATO", "TATAMOTORS", "HDFCBANK"],
    behavioral_traits=[
        "High Volatility Tolerance",
        "Seeks Momentum Breakouts & Volume Surges",
        "Vulnerable to Retail Options / FOMO Traps",
        "Requires Disciplined Stop-Loss Guardrails"
    ],
    loss_aversion_score=25.0,
    portfolio=PortfolioState(
        total_portfolio_value=350000.0,
        cash_balance=70000.0,   # 20% cash
        daily_pnl_inr=8950.0,
        daily_pnl_pct=2.56,
        holdings=[
            Holding(
                ticker="ZOMATO",
                company_name="Zomato Ltd (Eternal)",
                shares=615,
                avg_price=260.0,
                current_price=284.50,
                current_value=174967.5,
                allocation_pct=49.99,
                sector="Consumer Tech"
            ),
            Holding(
                ticker="TATAMOTORS",
                company_name="Tata Motors Ltd",
                shares=100,
                avg_price=990.0,
                current_price=1048.50,
                current_value=104850.0,
                allocation_pct=29.96,
                sector="Automobile"
            )
        ],
        sector_allocations={
            "Consumer Tech": 49.99,
            "Automobile": 29.96,
            "Cash Reserve": 20.05
        },
        concentration_hhi=calculate_hhi([
            Holding(ticker="ZOMATO", company_name="Zomato", shares=615, avg_price=260.0, current_price=284.5, current_value=174967.5, allocation_pct=49.99, sector="Tech"),
            Holding(ticker="TATAMOTORS", company_name="Tata Motors", shares=100, avg_price=990.0, current_price=1048.5, current_value=104850.0, allocation_pct=29.96, sector="Auto")
        ], 20.05)
    )
)

USER_PROFILES: Dict[str, UserProfile] = {
    "conservative": PROFILE_CONSERVATIVE,
    "aggressive": PROFILE_AGGRESSIVE
}


def register_custom_profile(
    name: str,
    age: int,
    risk_tolerance: str,
    investment_horizon: str,
    capital_inr: float,
    primary_goal: str = "Wealth Creation"
) -> UserProfile:
    """Dynamically creates and registers a real-world user investor profile from onboarding inputs"""
    risk_enum = RiskTolerance.CONSERVATIVE
    if "aggress" in risk_tolerance.lower():
        risk_enum = RiskTolerance.AGGRESSIVE
    elif "moderat" in risk_tolerance.lower():
        risk_enum = RiskTolerance.MODERATE

    horizon_enum = InvestmentHorizon.LONG_TERM
    if "short" in investment_horizon.lower():
        horizon_enum = InvestmentHorizon.SHORT_TERM
    elif "med" in investment_horizon.lower():
        horizon_enum = InvestmentHorizon.MEDIUM_TERM

    # Allocate realistic demo portfolio based on user risk
    cash_ratio = 0.30 if risk_enum == RiskTolerance.CONSERVATIVE else 0.15
    cash_val = capital_inr * cash_ratio
    invested = capital_inr - cash_val

    if risk_enum == RiskTolerance.CONSERVATIVE:
        holdings = [
            Holding(ticker="HDFCBANK", company_name="HDFC Bank Ltd", shares=max(1, int((invested * 0.6) / 1692)), avg_price=1620.0, current_price=1692.0, current_value=invested*0.6, allocation_pct=60.0 * (1 - cash_ratio), sector="Banking & Financials"),
            Holding(ticker="RELIANCE", company_name="Reliance Industries", shares=max(1, int((invested * 0.4) / 3024)), avg_price=2980.0, current_price=3024.0, current_value=invested*0.4, allocation_pct=40.0 * (1 - cash_ratio), sector="Energy & Conglomerate")
        ]
        sectors = {"Banking & Financials": round(60.0 * (1 - cash_ratio), 1), "Energy & Conglomerate": round(40.0 * (1 - cash_ratio), 1), "Cash": round(cash_ratio * 100, 1)}
        traits = [f"Goal: {primary_goal}", "Prefers Bluechip Moats", "Low Volatility Target", "Guarded Allocation"]
        loss_score = 80.0
    else:
        holdings = [
            Holding(ticker="ZOMATO", company_name="Zomato Ltd", shares=max(1, int((invested * 0.6) / 284.5)), avg_price=260.0, current_price=284.5, current_value=invested*0.6, allocation_pct=60.0 * (1 - cash_ratio), sector="Consumer Tech"),
            Holding(ticker="TATAMOTORS", company_name="Tata Motors Ltd", shares=max(1, int((invested * 0.4) / 1048.5)), avg_price=990.0, current_price=1048.5, current_value=invested*0.4, allocation_pct=40.0 * (1 - cash_ratio), sector="Automobile")
        ]
        sectors = {"Consumer Tech": round(60.0 * (1 - cash_ratio), 1), "Automobile": round(40.0 * (1 - cash_ratio), 1), "Cash": round(cash_ratio * 100, 1)}
        traits = [f"Goal: {primary_goal}", "Active Momentum Seeker", "Accepts Beta Volatility", "Stop-Loss Mandated"]
        loss_score = 30.0

    hhi = calculate_hhi(holdings, cash_ratio * 100)

    profile = UserProfile(
        user_id="USER_CUSTOM_01",
        name=name.strip() if name else "Personal Investor",
        risk_tolerance=risk_enum,
        investment_horizon=horizon_enum,
        capital_inr=capital_inr,
        watchlist=["TATAMOTORS", "RELIANCE", "HDFCBANK", "ZOMATO", "INFY"],
        behavioral_traits=traits,
        loss_aversion_score=loss_score,
        portfolio=PortfolioState(
            total_portfolio_value=capital_inr,
            cash_balance=cash_val,
            daily_pnl_inr=round(capital_inr * 0.012, 2),
            daily_pnl_pct=1.2,
            holdings=holdings,
            sector_allocations=sectors,
            concentration_hhi=hhi
        )
    )

    USER_PROFILES["custom"] = profile
    return profile


def get_profile(profile_id: str = "conservative") -> UserProfile:
    return USER_PROFILES.get(profile_id.lower(), USER_PROFILES.get("custom", PROFILE_CONSERVATIVE))
