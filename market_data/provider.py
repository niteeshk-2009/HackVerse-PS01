"""
SPY THE MARKET: Market Data Provider Layer
Production-grade financial data provider with strict 3-state data integrity:
- LIVE DATA
- DEMO DATA
- DATA UNAVAILABLE

Includes data quality validation, real market depth, technical indicators,
and clean provider interfaces.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random

from spidersense.agents.base import DataSourceState, DataQualityWarning


class MarketDataProvider(ABC):
    """Abstract Base Class for all equity market data providers."""
    
    @property
    @abstractmethod
    def data_state(self) -> DataSourceState:
        """Returns whether this provider supplies LIVE DATA, DEMO DATA, or DATA UNAVAILABLE."""
        pass

    @abstractmethod
    def get_quote(self, ticker: str, simulate_failure: bool = False) -> Dict[str, Any]:
        """Returns standard equity quote payload."""
        pass

    @abstractmethod
    def get_watchlist(self) -> List[Dict[str, Any]]:
        """Returns list of tracked equity quotes."""
        pass

    @abstractmethod
    def get_chart_data(self, ticker: str, timeframe: str = "1D") -> Dict[str, Any]:
        """Returns historical or intraday time-series data."""
        pass

    @abstractmethod
    def get_market_depth(self, ticker: str) -> Dict[str, Any]:
        """Returns order book Top 5 Bids and Asks."""
        pass

    def validate_quote(self, data: Dict[str, Any]) -> List[DataQualityWarning]:
        """Validates market data integrity and identifies anomalies."""
        warnings: List[DataQualityWarning] = []
        price = data.get("price", 0.0)
        volume = data.get("volume", 0)

        if price <= 0:
            warnings.append(DataQualityWarning(
                field="price",
                message=f"Invalid market price ({price}). Expected positive real value.",
                severity="CRITICAL"
            ))

        if volume < 0:
            warnings.append(DataQualityWarning(
                field="volume",
                message=f"Negative trade volume detected ({volume}).",
                severity="CRITICAL"
            ))

        high = data.get("high", 0.0)
        low = data.get("low", 0.0)
        if high > 0 and low > 0 and low > high:
            warnings.append(DataQualityWarning(
                field="intraday_range",
                message=f"Day low ({low}) exceeds day high ({high}). Malformed feed.",
                severity="CRITICAL"
            ))

        deliv = data.get("delivery_pct", 50.0)
        if deliv < 0.0 or deliv > 100.0:
            warnings.append(DataQualityWarning(
                field="delivery_pct",
                message=f"Delivery percentage out of bounds [0-100]: {deliv}%.",
                severity="WARNING"
            ))

        if data.get("is_degraded", False):
            warnings.append(DataQualityWarning(
                field="staleness",
                message=data.get("staleness_warning", "Market feed is degraded. Latency penalty active."),
                severity="WARNING"
            ))

        return warnings


class DemoMarketProvider(MarketDataProvider):
    """
    Deterministic Indian Equities (NSE) Demo Provider.
    Explicitly labeled as DEMO DATA. Never misrepresents synthetic feeds as live.
    Provides realistic, internally consistent numbers for technical momentum,
    volume surge, moving averages, and order book depth.
    """
    def __init__(self):
        self._state = DataSourceState.DEMO_DATA
        self._stocks: Dict[str, Dict[str, Any]] = {
            "TATAMOTORS": {
                "ticker": "TATAMOTORS",
                "company_name": "Tata Motors Limited",
                "exchange": "NSE",
                "sector": "Automobile",
                "price": 1048.50,
                "change_inr": 24.30,
                "change_pct": 2.37,
                "open": 1028.00,
                "high": 1056.20,
                "low": 1025.50,
                "previous_close": 1024.20,
                "volume": 14850000,
                "avg_volume_20d": 9200000,
                "volume_multiplier": 1.61,
                "delivery_pct": 48.2,
                "rsi_14": 68.4,
                "ema_20": 1012.40,
                "ema_50": 982.10,
                "ema_200": 914.80,
                "macd_line": 14.8,
                "macd_signal": 11.2,
                "macd_histogram": 3.6,
                "atr_14": 22.40,
                "beta": 1.45,
                "market_cap_crores": 386400.0,
                "pe_ratio": 16.8,
                "pb_ratio": 3.8,
                "roe_pct": 24.6,
                "dividend_yield_pct": 0.57,
                "debt_to_equity": 0.42,
                "week_52_high": 1179.00,
                "week_52_low": 605.00,
                "upper_circuit": 1126.60,
                "lower_circuit": 921.80,
                "sentiment_score": 72.0,
                "fii_flow_crores": 340.0,
                "retail_chase_indicator": 78.0
            },
            "RELIANCE": {
                "ticker": "RELIANCE",
                "company_name": "Reliance Industries Ltd",
                "exchange": "NSE",
                "sector": "Energy & Conglomerate",
                "price": 3024.00,
                "change_inr": -12.50,
                "change_pct": -0.41,
                "open": 3040.00,
                "high": 3052.00,
                "low": 3015.00,
                "previous_close": 3036.50,
                "volume": 6800000,
                "avg_volume_20d": 7100000,
                "volume_multiplier": 0.96,
                "delivery_pct": 59.4,
                "rsi_14": 52.1,
                "ema_20": 3010.00,
                "ema_50": 2980.00,
                "ema_200": 2860.00,
                "macd_line": 4.2,
                "macd_signal": 3.8,
                "macd_histogram": 0.4,
                "atr_14": 38.00,
                "beta": 0.85,
                "market_cap_crores": 2045000.0,
                "pe_ratio": 26.2,
                "pb_ratio": 2.1,
                "roe_pct": 9.4,
                "dividend_yield_pct": 0.33,
                "debt_to_equity": 0.38,
                "week_52_high": 3217.00,
                "week_52_low": 2220.00,
                "upper_circuit": 3340.00,
                "lower_circuit": 2732.00,
                "sentiment_score": 64.0,
                "fii_flow_crores": 180.0,
                "retail_chase_indicator": 35.0
            },
            "HDFCBANK": {
                "ticker": "HDFCBANK",
                "company_name": "HDFC Bank Limited",
                "exchange": "NSE",
                "sector": "Banking & Financials",
                "price": 1692.00,
                "change_inr": 18.20,
                "change_pct": 1.09,
                "open": 1675.00,
                "high": 1698.00,
                "low": 1672.00,
                "previous_close": 1673.80,
                "volume": 19200000,
                "avg_volume_20d": 15400000,
                "volume_multiplier": 1.25,
                "delivery_pct": 63.8,
                "rsi_14": 58.6,
                "ema_20": 1658.00,
                "ema_50": 1640.00,
                "ema_200": 1590.00,
                "macd_line": 9.4,
                "macd_signal": 6.8,
                "macd_histogram": 2.6,
                "atr_14": 21.00,
                "beta": 0.95,
                "market_cap_crores": 1285000.0,
                "pe_ratio": 18.4,
                "pb_ratio": 2.6,
                "roe_pct": 16.8,
                "dividend_yield_pct": 1.15,
                "debt_to_equity": 1.05,
                "week_52_high": 1794.00,
                "week_52_low": 1363.00,
                "upper_circuit": 1841.00,
                "lower_circuit": 1506.00,
                "sentiment_score": 68.0,
                "fii_flow_crores": 520.0,
                "retail_chase_indicator": 42.0
            },
            "ZOMATO": {
                "ticker": "ZOMATO",
                "company_name": "Zomato Ltd (Eternal)",
                "exchange": "NSE",
                "sector": "Consumer Tech / E-Commerce",
                "price": 284.50,
                "change_inr": 8.70,
                "change_pct": 3.15,
                "open": 277.00,
                "high": 288.40,
                "low": 275.20,
                "previous_close": 275.80,
                "volume": 42000000,
                "avg_volume_20d": 24000000,
                "volume_multiplier": 1.75,
                "delivery_pct": 36.4,
                "rsi_14": 74.2,
                "ema_20": 264.00,
                "ema_50": 242.00,
                "ema_200": 195.00,
                "macd_line": 8.2,
                "macd_signal": 5.4,
                "macd_histogram": 2.8,
                "atr_14": 11.20,
                "beta": 1.85,
                "market_cap_crores": 252000.0,
                "pe_ratio": 114.0,
                "pb_ratio": 9.4,
                "roe_pct": 6.8,
                "dividend_yield_pct": 0.0,
                "debt_to_equity": 0.02,
                "week_52_high": 298.00,
                "week_52_low": 98.00,
                "upper_circuit": 330.00,
                "lower_circuit": 220.00,
                "sentiment_score": 82.0,
                "fii_flow_crores": -45.0,
                "retail_chase_indicator": 92.0
            },
            "INFY": {
                "ticker": "INFY",
                "company_name": "Infosys Limited",
                "exchange": "NSE",
                "sector": "Information Technology",
                "price": 1895.00,
                "change_inr": -6.50,
                "change_pct": -0.34,
                "open": 1902.00,
                "high": 1914.00,
                "low": 1888.00,
                "previous_close": 1901.50,
                "volume": 5100000,
                "avg_volume_20d": 5400000,
                "volume_multiplier": 0.94,
                "delivery_pct": 58.1,
                "rsi_14": 56.4,
                "ema_20": 1880.00,
                "ema_50": 1845.00,
                "ema_200": 1690.00,
                "macd_line": 5.8,
                "macd_signal": 5.1,
                "macd_histogram": 0.7,
                "atr_14": 28.50,
                "beta": 1.02,
                "market_cap_crores": 788000.0,
                "pe_ratio": 28.5,
                "pb_ratio": 7.4,
                "roe_pct": 31.8,
                "dividend_yield_pct": 2.20,
                "debt_to_equity": 0.08,
                "week_52_high": 1991.00,
                "week_52_low": 1358.00,
                "upper_circuit": 2091.00,
                "lower_circuit": 1711.00,
                "sentiment_score": 61.0,
                "fii_flow_crores": 95.0,
                "retail_chase_indicator": 40.0
            },
            "TCS": {
                "ticker": "TCS",
                "company_name": "Tata Consultancy Services Ltd",
                "exchange": "NSE",
                "sector": "Information Technology",
                "price": 4218.00,
                "change_inr": 36.40,
                "change_pct": 0.87,
                "open": 4190.00,
                "high": 4235.00,
                "low": 4182.00,
                "previous_close": 4181.60,
                "volume": 2400000,
                "avg_volume_20d": 2100000,
                "volume_multiplier": 1.14,
                "delivery_pct": 68.4,
                "rsi_14": 62.1,
                "ema_20": 4165.00,
                "ema_50": 4080.00,
                "ema_200": 3890.00,
                "macd_line": 18.2,
                "macd_signal": 14.1,
                "macd_histogram": 4.1,
                "atr_14": 52.00,
                "beta": 0.78,
                "market_cap_crores": 1526000.0,
                "pe_ratio": 31.4,
                "pb_ratio": 13.8,
                "roe_pct": 51.2,
                "dividend_yield_pct": 2.70,
                "debt_to_equity": 0.0,
                "week_52_high": 4585.00,
                "week_52_low": 3313.00,
                "upper_circuit": 4643.00,
                "lower_circuit": 3799.00,
                "sentiment_score": 75.0,
                "fii_flow_crores": 280.0,
                "retail_chase_indicator": 32.0
            },
            "ICICIBANK": {
                "ticker": "ICICIBANK",
                "company_name": "ICICI Bank Limited",
                "exchange": "NSE",
                "sector": "Banking & Financials",
                "price": 1245.00,
                "change_inr": 14.20,
                "change_pct": 1.15,
                "open": 1235.00,
                "high": 1252.00,
                "low": 1231.00,
                "previous_close": 1230.80,
                "volume": 14500000,
                "avg_volume_20d": 12800000,
                "volume_multiplier": 1.13,
                "delivery_pct": 61.2,
                "rsi_14": 65.4,
                "ema_20": 1224.00,
                "ema_50": 1195.00,
                "ema_200": 1120.00,
                "macd_line": 8.1,
                "macd_signal": 6.2,
                "macd_histogram": 1.9,
                "atr_14": 18.00,
                "beta": 0.92,
                "market_cap_crores": 876000.0,
                "pe_ratio": 18.9,
                "pb_ratio": 3.1,
                "roe_pct": 18.6,
                "dividend_yield_pct": 0.88,
                "debt_to_equity": 0.95,
                "week_52_high": 1310.00,
                "week_52_low": 985.00,
                "upper_circuit": 1369.00,
                "lower_circuit": 1120.00,
                "sentiment_score": 74.0,
                "fii_flow_crores": 410.0,
                "retail_chase_indicator": 38.0
            },
            "SBIN": {
                "ticker": "SBIN",
                "company_name": "State Bank of India",
                "exchange": "NSE",
                "sector": "PSU Banking",
                "price": 815.00,
                "change_inr": 6.80,
                "change_pct": 0.84,
                "open": 810.00,
                "high": 822.00,
                "low": 808.00,
                "previous_close": 808.20,
                "volume": 22000000,
                "avg_volume_20d": 18000000,
                "volume_multiplier": 1.22,
                "delivery_pct": 46.5,
                "rsi_14": 57.8,
                "ema_20": 804.00,
                "ema_50": 788.00,
                "ema_200": 725.00,
                "macd_line": 4.5,
                "macd_signal": 3.6,
                "macd_histogram": 0.9,
                "atr_14": 14.50,
                "beta": 1.18,
                "market_cap_crores": 728000.0,
                "pe_ratio": 10.8,
                "pb_ratio": 1.7,
                "roe_pct": 17.2,
                "dividend_yield_pct": 1.70,
                "debt_to_equity": 1.45,
                "week_52_high": 912.00,
                "week_52_low": 585.00,
                "upper_circuit": 896.00,
                "lower_circuit": 734.00,
                "sentiment_score": 67.0,
                "fii_flow_crores": 150.0,
                "retail_chase_indicator": 48.0
            },
            "BHARTIARTL": {
                "ticker": "BHARTIARTL",
                "company_name": "Bharti Airtel Limited",
                "exchange": "NSE",
                "sector": "Telecommunications",
                "price": 1645.00,
                "change_inr": 28.50,
                "change_pct": 1.76,
                "open": 1622.00,
                "high": 1655.00,
                "low": 1618.00,
                "previous_close": 1616.50,
                "volume": 7800000,
                "avg_volume_20d": 6200000,
                "volume_multiplier": 1.26,
                "delivery_pct": 54.8,
                "rsi_14": 71.2,
                "ema_20": 1605.00,
                "ema_50": 1550.00,
                "ema_200": 1410.00,
                "macd_line": 12.4,
                "macd_signal": 9.1,
                "macd_histogram": 3.3,
                "atr_14": 26.00,
                "beta": 0.82,
                "market_cap_crores": 985000.0,
                "pe_ratio": 54.0,
                "pb_ratio": 7.8,
                "roe_pct": 19.4,
                "dividend_yield_pct": 0.48,
                "debt_to_equity": 1.65,
                "week_52_high": 1720.00,
                "week_52_low": 915.00,
                "upper_circuit": 1795.00,
                "lower_circuit": 1470.00,
                "sentiment_score": 78.0,
                "fii_flow_crores": 390.0,
                "retail_chase_indicator": 52.0
            },
            "ITC": {
                "ticker": "ITC",
                "company_name": "ITC Limited",
                "exchange": "NSE",
                "sector": "FMCG & Conglomerate",
                "price": 492.00,
                "change_inr": -1.80,
                "change_pct": -0.36,
                "open": 494.00,
                "high": 497.00,
                "low": 490.50,
                "previous_close": 493.80,
                "volume": 12000000,
                "avg_volume_20d": 11500000,
                "volume_multiplier": 1.04,
                "delivery_pct": 69.5,
                "rsi_14": 49.5,
                "ema_20": 495.00,
                "ema_50": 488.00,
                "ema_200": 465.00,
                "macd_line": 1.2,
                "macd_signal": 1.5,
                "macd_histogram": -0.3,
                "atr_14": 6.80,
                "beta": 0.62,
                "market_cap_crores": 615000.0,
                "pe_ratio": 29.5,
                "pb_ratio": 8.4,
                "roe_pct": 28.5,
                "dividend_yield_pct": 3.10,
                "debt_to_equity": 0.0,
                "week_52_high": 528.00,
                "week_52_low": 399.00,
                "upper_circuit": 542.00,
                "lower_circuit": 444.00,
                "sentiment_score": 58.0,
                "fii_flow_crores": 45.0,
                "retail_chase_indicator": 24.0
            },
            "BAJFINANCE": {
                "ticker": "BAJFINANCE",
                "company_name": "Bajaj Finance Limited",
                "exchange": "NSE",
                "sector": "Financial Services / NBFC",
                "price": 7240.00,
                "change_inr": 85.00,
                "change_pct": 1.19,
                "open": 7180.00,
                "high": 7290.00,
                "low": 7160.00,
                "previous_close": 7155.00,
                "volume": 1400000,
                "avg_volume_20d": 1250000,
                "volume_multiplier": 1.12,
                "delivery_pct": 52.1,
                "rsi_14": 63.8,
                "ema_20": 7110.00,
                "ema_50": 6980.00,
                "ema_200": 6780.00,
                "macd_line": 32.0,
                "macd_signal": 24.0,
                "macd_histogram": 8.0,
                "atr_14": 115.00,
                "beta": 1.35,
                "market_cap_crores": 448000.0,
                "pe_ratio": 29.2,
                "pb_ratio": 5.4,
                "roe_pct": 21.8,
                "dividend_yield_pct": 0.50,
                "debt_to_equity": 3.80,
                "week_52_high": 8192.00,
                "week_52_low": 6375.00,
                "upper_circuit": 7940.00,
                "lower_circuit": 6500.00,
                "sentiment_score": 71.0,
                "fii_flow_crores": 210.0,
                "retail_chase_indicator": 44.0
            },
            "LT": {
                "ticker": "LT",
                "company_name": "Larsen & Toubro Ltd",
                "exchange": "NSE",
                "sector": "Capital Goods & Infrastructure",
                "price": 3680.00,
                "change_inr": 42.00,
                "change_pct": 1.15,
                "open": 3650.00,
                "high": 3710.00,
                "low": 3640.00,
                "previous_close": 3638.00,
                "volume": 2800000,
                "avg_volume_20d": 2400000,
                "volume_multiplier": 1.17,
                "delivery_pct": 58.6,
                "rsi_14": 66.2,
                "ema_20": 3620.00,
                "ema_50": 3540.00,
                "ema_200": 3320.00,
                "macd_line": 21.0,
                "macd_signal": 16.5,
                "macd_histogram": 4.5,
                "atr_14": 48.00,
                "beta": 1.05,
                "market_cap_crores": 506000.0,
                "pe_ratio": 36.8,
                "pb_ratio": 5.2,
                "roe_pct": 15.4,
                "dividend_yield_pct": 0.92,
                "debt_to_equity": 1.12,
                "week_52_high": 3919.00,
                "week_52_low": 2980.00,
                "upper_circuit": 4045.00,
                "lower_circuit": 3310.00,
                "sentiment_score": 76.0,
                "fii_flow_crores": 310.0,
                "retail_chase_indicator": 36.0
            },
            "MARUTI": {
                "ticker": "MARUTI",
                "company_name": "Maruti Suzuki India Ltd",
                "exchange": "NSE",
                "sector": "Automobile",
                "price": 12480.00,
                "change_inr": -45.00,
                "change_pct": -0.36,
                "open": 12550.00,
                "high": 12620.00,
                "low": 12440.00,
                "previous_close": 12525.00,
                "volume": 650000,
                "avg_volume_20d": 580000,
                "volume_multiplier": 1.12,
                "delivery_pct": 62.4,
                "rsi_14": 54.1,
                "ema_20": 12410.00,
                "ema_50": 12280.00,
                "ema_200": 11450.00,
                "macd_line": 38.0,
                "macd_signal": 35.0,
                "macd_histogram": 3.0,
                "atr_14": 160.00,
                "beta": 0.88,
                "market_cap_crores": 392000.0,
                "pe_ratio": 27.5,
                "pb_ratio": 4.6,
                "roe_pct": 16.8,
                "dividend_yield_pct": 1.00,
                "debt_to_equity": 0.01,
                "week_52_high": 13680.00,
                "week_52_low": 9735.00,
                "upper_circuit": 13730.00,
                "lower_circuit": 11230.00,
                "sentiment_score": 62.0,
                "fii_flow_crores": 85.0,
                "retail_chase_indicator": 29.0
            },
            "SUNPHARMA": {
                "ticker": "SUNPHARMA",
                "company_name": "Sun Pharmaceutical Industries",
                "exchange": "NSE",
                "sector": "Healthcare & Pharma",
                "price": 1820.00,
                "change_inr": 22.50,
                "change_pct": 1.25,
                "open": 1802.00,
                "high": 1832.00,
                "low": 1798.00,
                "previous_close": 1797.50,
                "volume": 3200000,
                "avg_volume_20d": 2900000,
                "volume_multiplier": 1.10,
                "delivery_pct": 65.2,
                "rsi_14": 68.5,
                "ema_20": 1790.00,
                "ema_50": 1735.00,
                "ema_200": 1580.00,
                "macd_line": 14.2,
                "macd_signal": 10.5,
                "macd_histogram": 3.7,
                "atr_14": 24.00,
                "beta": 0.58,
                "market_cap_crores": 436000.0,
                "pe_ratio": 38.2,
                "pb_ratio": 6.1,
                "roe_pct": 17.5,
                "dividend_yield_pct": 0.75,
                "debt_to_equity": 0.08,
                "week_52_high": 1940.00,
                "week_52_low": 1110.00,
                "upper_circuit": 1990.00,
                "lower_circuit": 1630.00,
                "sentiment_score": 77.0,
                "fii_flow_crores": 290.0,
                "retail_chase_indicator": 31.0,
                "currency": "INR",
                "region": "IN"
            },
            # =========================================================
            # GLOBAL / US FOREIGN EQUITIES (NASDAQ / NYSE)
            # =========================================================
            "NVDA": {
                "ticker": "NVDA",
                "company_name": "NVIDIA Corporation",
                "exchange": "NASDAQ",
                "sector": "AI Semiconductors & Accelerated Computing",
                "price": 128.40,
                "change_inr": 3.80,  # change in local currency ($3.80)
                "change_pct": 3.05,
                "open": 125.10,
                "high": 129.80,
                "low": 124.60,
                "previous_close": 124.60,
                "volume": 68000000,
                "avg_volume_20d": 52000000,
                "volume_multiplier": 1.31,
                "delivery_pct": 52.4,
                "rsi_14": 71.8,
                "ema_20": 122.50,
                "ema_50": 116.80,
                "ema_200": 98.40,
                "macd_line": 3.4,
                "macd_signal": 2.6,
                "macd_histogram": 0.8,
                "atr_14": 4.20,
                "beta": 1.72,
                "market_cap_crores": 26500000.0,  # Approx $3.15 Trillion
                "pe_ratio": 64.2,
                "pb_ratio": 38.5,
                "roe_pct": 115.4,
                "dividend_yield_pct": 0.03,
                "debt_to_equity": 0.18,
                "week_52_high": 140.76,
                "week_52_low": 45.00,
                "upper_circuit": 154.00,
                "lower_circuit": 102.00,
                "sentiment_score": 88.0,
                "fii_flow_crores": 1450.0,
                "retail_chase_indicator": 82.0,
                "currency": "USD",
                "region": "US"
            },
            "AAPL": {
                "ticker": "AAPL",
                "company_name": "Apple Inc.",
                "exchange": "NASDAQ",
                "sector": "Consumer Electronics & Digital Services",
                "price": 226.50,
                "change_inr": 1.90,
                "change_pct": 0.85,
                "open": 224.80,
                "high": 227.40,
                "low": 224.10,
                "previous_close": 224.60,
                "volume": 48000000,
                "avg_volume_20d": 45000000,
                "volume_multiplier": 1.07,
                "delivery_pct": 64.1,
                "rsi_14": 61.4,
                "ema_20": 223.10,
                "ema_50": 218.40,
                "ema_200": 198.50,
                "macd_line": 2.1,
                "macd_signal": 1.7,
                "macd_histogram": 0.4,
                "atr_14": 3.80,
                "beta": 0.94,
                "market_cap_crores": 29100000.0,  # Approx $3.45 Trillion
                "pe_ratio": 34.1,
                "pb_ratio": 48.2,
                "roe_pct": 147.2,
                "dividend_yield_pct": 0.44,
                "debt_to_equity": 1.45,
                "week_52_high": 237.23,
                "week_52_low": 164.08,
                "upper_circuit": 260.00,
                "lower_circuit": 190.00,
                "sentiment_score": 75.0,
                "fii_flow_crores": 620.0,
                "retail_chase_indicator": 46.0,
                "currency": "USD",
                "region": "US"
            },
            "MSFT": {
                "ticker": "MSFT",
                "company_name": "Microsoft Corporation",
                "exchange": "NASDAQ",
                "sector": "Enterprise Software & Cloud AI",
                "price": 448.20,
                "change_inr": 4.10,
                "change_pct": 0.92,
                "open": 445.00,
                "high": 451.00,
                "low": 443.80,
                "previous_close": 444.10,
                "volume": 21000000,
                "avg_volume_20d": 19500000,
                "volume_multiplier": 1.08,
                "delivery_pct": 69.4,
                "rsi_14": 63.8,
                "ema_20": 442.00,
                "ema_50": 434.50,
                "ema_200": 402.00,
                "macd_line": 4.8,
                "macd_signal": 3.9,
                "macd_histogram": 0.9,
                "atr_14": 6.40,
                "beta": 0.89,
                "market_cap_crores": 28200000.0,  # Approx $3.33 Trillion
                "pe_ratio": 36.8,
                "pb_ratio": 12.4,
                "roe_pct": 38.4,
                "dividend_yield_pct": 0.67,
                "debt_to_equity": 0.38,
                "week_52_high": 468.35,
                "week_52_low": 309.45,
                "upper_circuit": 500.00,
                "lower_circuit": 395.00,
                "sentiment_score": 82.0,
                "fii_flow_crores": 840.0,
                "retail_chase_indicator": 38.0,
                "currency": "USD",
                "region": "US"
            },
            "TSLA": {
                "ticker": "TSLA",
                "company_name": "Tesla, Inc.",
                "exchange": "NASDAQ",
                "sector": "Electric Vehicles & AI Robotics",
                "price": 218.80,
                "change_inr": -3.40,
                "change_pct": -1.53,
                "open": 223.00,
                "high": 225.40,
                "low": 216.50,
                "previous_close": 222.20,
                "volume": 72000000,
                "avg_volume_20d": 64000000,
                "volume_multiplier": 1.13,
                "delivery_pct": 39.8,
                "rsi_14": 52.4,
                "ema_20": 221.40,
                "ema_50": 212.00,
                "ema_200": 204.00,
                "macd_line": 1.4,
                "macd_signal": 1.8,
                "macd_histogram": -0.4,
                "atr_14": 9.20,
                "beta": 2.15,
                "market_cap_crores": 6980000.0,  # Approx $700 Billion
                "pe_ratio": 72.5,
                "pb_ratio": 10.8,
                "roe_pct": 14.8,
                "dividend_yield_pct": 0.0,
                "debt_to_equity": 0.08,
                "week_52_high": 271.00,
                "week_52_low": 138.80,
                "upper_circuit": 265.00,
                "lower_circuit": 170.00,
                "sentiment_score": 68.0,
                "fii_flow_crores": -120.0,
                "retail_chase_indicator": 84.0,
                "currency": "USD",
                "region": "US"
            },
            "GOOGL": {
                "ticker": "GOOGL",
                "company_name": "Alphabet Inc.",
                "exchange": "NASDAQ",
                "sector": "Internet Platforms & Cloud AI",
                "price": 165.20,
                "change_inr": 1.80,
                "change_pct": 1.10,
                "open": 163.50,
                "high": 166.40,
                "low": 163.10,
                "previous_close": 163.40,
                "volume": 28000000,
                "avg_volume_20d": 26000000,
                "volume_multiplier": 1.08,
                "delivery_pct": 65.2,
                "rsi_14": 59.8,
                "ema_20": 163.80,
                "ema_50": 160.20,
                "ema_200": 147.00,
                "macd_line": 1.8,
                "macd_signal": 1.4,
                "macd_histogram": 0.4,
                "atr_14": 3.10,
                "beta": 1.05,
                "market_cap_crores": 17400000.0,  # Approx $2.05 Trillion
                "pe_ratio": 24.2,
                "pb_ratio": 6.8,
                "roe_pct": 29.8,
                "dividend_yield_pct": 0.48,
                "debt_to_equity": 0.10,
                "week_52_high": 191.75,
                "week_52_low": 120.21,
                "upper_circuit": 188.00,
                "lower_circuit": 142.00,
                "sentiment_score": 79.0,
                "fii_flow_crores": 450.0,
                "retail_chase_indicator": 35.0,
                "currency": "USD",
                "region": "US"
            },
            "AMZN": {
                "ticker": "AMZN",
                "company_name": "Amazon.com, Inc.",
                "exchange": "NASDAQ",
                "sector": "Global E-Commerce & AWS Cloud",
                "price": 184.60,
                "change_inr": 2.40,
                "change_pct": 1.32,
                "open": 182.50,
                "high": 185.80,
                "low": 181.90,
                "previous_close": 182.20,
                "volume": 36000000,
                "avg_volume_20d": 34000000,
                "volume_multiplier": 1.06,
                "delivery_pct": 61.8,
                "rsi_14": 64.2,
                "ema_20": 181.50,
                "ema_50": 176.80,
                "ema_200": 158.00,
                "macd_line": 2.6,
                "macd_signal": 2.0,
                "macd_histogram": 0.6,
                "atr_14": 3.90,
                "beta": 1.15,
                "market_cap_crores": 16400000.0,  # Approx $1.93 Trillion
                "pe_ratio": 42.1,
                "pb_ratio": 8.1,
                "roe_pct": 21.4,
                "dividend_yield_pct": 0.0,
                "debt_to_equity": 0.58,
                "week_52_high": 201.20,
                "week_52_low": 118.35,
                "upper_circuit": 212.00,
                "lower_circuit": 156.00,
                "sentiment_score": 81.0,
                "fii_flow_crores": 510.0,
                "retail_chase_indicator": 42.0,
                "currency": "USD",
                "region": "US"
            }
        }
        self._cached_snapshots = {k: v.copy() for k, v in self._stocks.items()}

    @property
    def data_state(self) -> DataSourceState:
        return self._state

    def get_quote(self, ticker: str, simulate_failure: bool = False) -> Dict[str, Any]:
        ticker = ticker.upper()
        if simulate_failure:
            cached = self._cached_snapshots.get(ticker, self._stocks["TATAMOTORS"]).copy()
            cached["data_source_state"] = DataSourceState.DATA_UNAVAILABLE.value
            cached["data_source_label"] = "DATA UNAVAILABLE (Simulated Disconnect)"
            cached["is_live"] = False
            cached["is_demo"] = True
            cached["is_degraded"] = True
            cached["staleness_warning"] = "FEED DISCONNECTED: Using cached snapshot from 2 hours prior. Technical latency confidence penalised."
            cached["timestamp"] = "CACHED_OFFLINE_SNAPSHOT"
            return cached

        if ticker not in self._stocks:
            raise KeyError(f"Ticker '{ticker}' not found in market universe.")

        data = self._stocks[ticker].copy()
        exchange = data.get("exchange", "NSE")
        data.setdefault("currency", "INR")
        data.setdefault("region", "IN")
        data["data_source_state"] = DataSourceState.DEMO_DATA.value
        data["data_source_label"] = f"DEMO DATA (Deterministic {exchange} Simulation)"
        data["is_live"] = False
        data["is_demo"] = True
        data["is_degraded"] = False
        data["timestamp"] = datetime.utcnow().isoformat()
        return data

    def get_watchlist(self) -> List[Dict[str, Any]]:
        results = []
        for stock in self._stocks.values():
            s = stock.copy()
            exchange = s.get("exchange", "NSE")
            s.setdefault("currency", "INR")
            s.setdefault("region", "IN")
            s["data_source_state"] = DataSourceState.DEMO_DATA.value
            s["data_source_label"] = f"DEMO DATA (Deterministic {exchange} Simulation)"
            s["is_live"] = False
            s["is_demo"] = True
            results.append(s)
        return results

    def get_chart_data(self, ticker: str, timeframe: str = "1D") -> Dict[str, Any]:
        quote = self.get_quote(ticker)
        current_price = quote["price"]
        prev_close = quote["previous_close"]
        timeframe = timeframe.upper()

        labels: List[str] = []
        prices: List[float] = []
        ema_series: List[float] = []

        if timeframe == "1D":
            base = prev_close
            now = datetime.now()
            start_t = now.replace(hour=9, minute=15, second=0, microsecond=0)
            if now < start_t:
                end_t = now.replace(hour=15, minute=30, second=0, microsecond=0)
            else:
                end_t = min(now, now.replace(hour=15, minute=30, second=0, microsecond=0))

            intervals = []
            curr = start_t
            while curr <= end_t:
                intervals.append(curr)
                curr += timedelta(minutes=15)
            
            if len(intervals) < 6:
                intervals = [start_t + timedelta(minutes=15 * i) for i in range(12)]
            
            steps = len(intervals)
            total_delta = current_price - base
            
            random.seed(hash(ticker) + 101)
            for i, interval_time in enumerate(intervals):
                labels.append(interval_time.strftime("%H:%M"))
                target_prog = (i + 1) / steps
                expected = base + (total_delta * target_prog)
                noise = (random.random() - 0.48) * (quote["atr_14"] * 0.25)
                price_val = current_price if i == steps - 1 else round(expected + noise, 2)
                prices.append(price_val)
                ema_series.append(round(price_val * 0.995, 2))

        elif timeframe == "1W":
            labels = ["Mon 10:00", "Mon 14:00", "Tue 10:00", "Tue 14:00", "Wed 10:00", "Wed 14:00", "Thu 10:00", "Thu 14:00", "Fri 10:00", "Fri 14:00"]
            start_p = round(current_price * 0.97, 2)
            prices = [
                start_p,
                round(start_p * 1.008, 2),
                round(start_p * 1.014, 2),
                round(start_p * 1.009, 2),
                round(start_p * 1.018, 2),
                round(start_p * 1.025, 2),
                round(start_p * 1.020, 2),
                round(start_p * 1.028, 2),
                round(start_p * 1.022, 2),
                current_price
            ]
            ema_series = [round(p * 0.992, 2) for p in prices]

        elif timeframe == "1M":
            start_p = round(current_price * 0.92, 2)
            random.seed(hash(ticker) + 202)
            for d in range(1, 31):
                labels.append(f"Day {d}")
                frac = d / 30.0
                p = round(start_p + ((current_price - start_p) * frac) + (random.uniform(-1, 1) * quote['atr_14'] * 0.3), 2)
                if d == 30: p = current_price
                prices.append(p)
                ema_series.append(round(p * 0.988, 2))

        else:  # 1Y
            months = ["Sep 25", "Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26", "Apr 26", "May 26", "Jun 26", "Jul 26", "Aug 26"]
            start_p = round(quote["week_52_low"] * 1.15, 2)
            labels = months
            prices = [
                start_p,
                round(start_p * 1.08, 2),
                round(start_p * 1.14, 2),
                round(start_p * 1.12, 2),
                round(start_p * 1.25, 2),
                round(start_p * 1.34, 2),
                round(start_p * 1.40, 2),
                round(start_p * 1.36, 2),
                round(start_p * 1.48, 2),
                round(start_p * 1.55, 2),
                round(start_p * 1.58, 2),
                current_price
            ]
            ema_series = [round(p * 0.975, 2) for p in prices]

        return {
            "ticker": ticker,
            "timeframe": timeframe,
            "labels": labels,
            "prices": prices,
            "ema_20": ema_series,
            "current_price": current_price,
            "change_pct": quote["change_pct"],
            "is_positive": quote["change_pct"] >= 0,
            "data_source_state": DataSourceState.DEMO_DATA.value
        }

    def get_market_depth(self, ticker: str) -> Dict[str, Any]:
        """Calculates Top 5 Bids (Buyers) and Asks (Sellers) order book depth."""
        q = self.get_quote(ticker)
        p = q["price"]

        bids = [
            {"orders": 142, "qty": 8500, "price": round(p - 0.10, 2)},
            {"orders": 98, "qty": 14200, "price": round(p - 0.25, 2)},
            {"orders": 215, "qty": 32000, "price": round(p - 0.50, 2)},
            {"orders": 74, "qty": 9800, "price": round(p - 0.75, 2)},
            {"orders": 189, "qty": 27400, "price": round(p - 1.00, 2)},
        ]
        asks = [
            {"orders": 118, "qty": 7200, "price": round(p + 0.10, 2)},
            {"orders": 164, "qty": 18400, "price": round(p + 0.25, 2)},
            {"orders": 85, "qty": 11500, "price": round(p + 0.50, 2)},
            {"orders": 240, "qty": 38900, "price": round(p + 0.75, 2)},
            {"orders": 92, "qty": 14600, "price": round(p + 1.00, 2)},
        ]

        total_buy_qty = sum(b["qty"] for b in bids)
        total_sell_qty = sum(a["qty"] for a in asks)
        buy_pct = round((total_buy_qty / (total_buy_qty + total_sell_qty)) * 100, 1)

        return {
            "ticker": ticker,
            "bids": bids,
            "asks": asks,
            "total_buy_qty": total_buy_qty,
            "total_sell_qty": total_sell_qty,
            "buy_pct": buy_pct,
            "sell_pct": round(100.0 - buy_pct, 1),
            "data_source_state": DataSourceState.DEMO_DATA.value
        }


class LiveMarketProvider(MarketDataProvider):
    """
    Live Market Data Provider Adapter.
    Configured for live external APIs (e.g. NSE / Yahoo Finance / AlphaVantage).
    If credentials/connectivity are unavailable, gracefully reports DATA UNAVAILABLE.
    """
    def __init__(self, fallback_provider: Optional[MarketDataProvider] = None):
        self._state = DataSourceState.LIVE_DATA
        self._fallback = fallback_provider or DemoMarketProvider()
        self._is_connected = False  # Set to True when live API credentials are authenticated

    @property
    def data_state(self) -> DataSourceState:
        return self._state if self._is_connected else DataSourceState.DATA_UNAVAILABLE

    def get_quote(self, ticker: str, simulate_failure: bool = False) -> Dict[str, Any]:
        if not self._is_connected or simulate_failure:
            fallback_quote = self._fallback.get_quote(ticker, simulate_failure=simulate_failure)
            fallback_quote["data_source_state"] = DataSourceState.DATA_UNAVAILABLE.value
            fallback_quote["data_source_label"] = "LIVE FEED OFFLINE · FALLBACK SNAPSHOT ACTIVATED"
            fallback_quote["is_live"] = False
            fallback_quote["is_degraded"] = True
            fallback_quote["staleness_warning"] = "Live exchange stream unconfigured or unreachable. Using offline fallback snapshot."
            return fallback_quote
        raise NotImplementedError("Live websocket connection handler required for live streaming.")

    def get_watchlist(self) -> List[Dict[str, Any]]:
        return self._fallback.get_watchlist()

    def get_chart_data(self, ticker: str, timeframe: str = "1D") -> Dict[str, Any]:
        return self._fallback.get_chart_data(ticker, timeframe=timeframe)

    def get_market_depth(self, ticker: str) -> Dict[str, Any]:
        return self._fallback.get_market_depth(ticker)


class MarketProviderManager:
    """Singleton manager allowing runtime toggling between DEMO and LIVE modes."""
    def __init__(self):
        self._demo_provider = DemoMarketProvider()
        self._live_provider = LiveMarketProvider(fallback_provider=self._demo_provider)
        self._current_mode = "DEMO"  # "DEMO" or "LIVE"

    def get_provider(self) -> MarketDataProvider:
        if self._current_mode == "LIVE":
            return self._live_provider
        return self._demo_provider

    def set_mode(self, mode: str) -> str:
        mode = mode.upper()
        if mode not in ["DEMO", "LIVE"]:
            raise ValueError("Mode must be either 'DEMO' or 'LIVE'")
        self._current_mode = mode
        return self._current_mode

    @property
    def current_mode(self) -> str:
        return self._current_mode


# Global singleton provider instance
provider_manager = MarketProviderManager()
market_provider = provider_manager.get_provider()
