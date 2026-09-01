# SPY THE MARKET — Data Sources & Integrity Specification

> *"Strict 3-State Data Policy: LIVE DATA · DEMO DATA · DATA UNAVAILABLE"*

---

## 1. The 3-State Data Policy

SPY THE MARKET enforces strict semantic honesty regarding all data displayed to users:

| State | Definition | UI Visual Label | System Behavior |
|---|---|---|---|
| **LIVE DATA** | Real-time stream originating from an active, verified exchange or broker API. | `● LIVE DATA` (Green beacon) | Full real-time depth and real-time tick analysis. |
| **DEMO DATA** | Deterministic, realistic simulation of Indian equities market data. | `● DEMO DATA (Deterministic NSE)` (Amber badge) | Internally consistent, historical metrics, realistic 1D/1W/1M/1Y series. Never labeled as LIVE. |
| **DATA UNAVAILABLE** | Feed interruption, missing filing, or unconfigured provider. | `⚠ DATA UNAVAILABLE` (Purple/Red badge) | Pipeline gracefully continues, confidence penalized, zero synthetic hallucination. |

---

## 2. Tracked Indian Equities (NSE Universe)

The demo universe covers 5 leading listed Indian enterprises across distinct market caps, sectors, and volatility regimes:

1. **Tata Motors Ltd (`TATAMOTORS`)**
   - Sector: Automobile
   - Exchange: NSE
   - Beta: 1.45 (High Volatility / Growth)
   - Volume Surge Multiplier: 1.61x
   - Delivery %: 48.2%

2. **Reliance Industries Ltd (`RELIANCE`)**
   - Sector: Energy & Conglomerate
   - Exchange: NSE
   - Beta: 0.85 (Defensive / Benchmark Heavyweight)
   - Volume Surge Multiplier: 0.96x
   - Delivery %: 59.4%

3. **HDFC Bank Limited (`HDFCBANK`)**
   - Sector: Banking & Financials
   - Exchange: NSE
   - Beta: 0.95 (Core Large Cap)
   - Volume Surge Multiplier: 1.25x
   - Delivery %: 63.8%

4. **Zomato Ltd / Eternal (`ZOMATO`)**
   - Sector: Consumer Tech / E-Commerce
   - Exchange: NSE
   - Beta: 1.85 (High Beta / Momentum)
   - Volume Surge Multiplier: 1.75x
   - Delivery %: 36.4%

5. **Infosys Limited (`INFY`)**
   - Sector: Information Technology
   - Exchange: NSE
   - Beta: 1.02 (Export / Dollar Hedge)
   - Volume Surge Multiplier: 0.94x
   - Delivery %: 58.1%

---

## 3. Data Quality & Anomaly Validation

Before market data is processed by the agent pipeline, it passes through `validate_quote()`:
- **Price Sanity**: Must be positive real number ($P > 0$).
- **Volume Non-Negativity**: Trade volume must be $\ge 0$.
- **Intraday Boundary Check**: Validates $\text{Low} \le P \le \text{High}$.
- **Delivery Boundary**: Delivery percentage must reside within $[0.0, 100.0]$.
- **Staleness Tracking**: Emits warnings when feeds are degraded or timestamps exceed maximum allowable latency.

---

## 4. Live Provider Integration Architecture

To connect a live market feed in production:
1. Implement the `MarketDataProvider` abstract class in `market_data/provider.py`.
2. Connect websockets to NSE SMART API / Upstox / Kite Connect / AlphaVantage.
3. Configure `DATA_MODE=LIVE` in environment variables or toggle via the Settings panel.
