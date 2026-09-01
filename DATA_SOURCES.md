# SPIDER SENSE — Data Sources & Integrity Specification

> *"Strict 3-State Data Policy: LIVE DATA · DEMO DATA · DATA UNAVAILABLE"*

---

## 1. The 3-State Data Policy

SPIDER SENSE enforces strict semantic honesty regarding all data displayed to users:

| State | Definition | UI Visual Label | System Behavior |
|---|---|---|---|
| **LIVE DATA** | Real-time stream originating from an active, verified exchange or broker API. | `● LIVE DATA` (Green beacon) | Full real-time depth and real-time tick analysis. |
| **DEMO DATA** | Deterministic, realistic simulation of Indian equities market data. | `● DEMO DATA (Deterministic NSE)` (Amber badge) | Internally consistent, historical metrics, realistic 1D/1W/1M/1Y series. Never labeled as LIVE. |
| **DATA UNAVAILABLE** | Feed interruption, missing filing, or unconfigured provider. | `⚠ DATA UNAVAILABLE` (Purple/Red badge) | Pipeline gracefully continues, confidence penalized, zero synthetic hallucination. |

---

## 2. Tracked Indian Equities (NSE Universe)

The universe covers leading listed enterprises across Indian (NSE) and US Global (NASDAQ) markets:

### A. Indian Equities (NSE Universe)
- **TATAMOTORS**: Tata Motors Ltd (Automobile, Beta: 1.45, High Momentum)
- **RELIANCE**: Reliance Industries Ltd (Energy & Conglomerate, Beta: 0.85, Core Bluechip)
- **HDFCBANK**: HDFC Bank Ltd (Banking & Financials, Beta: 0.95)
- **ICICIBANK**: ICICI Bank Ltd (Private Banking, Beta: 1.05)
- **INFY**: Infosys Ltd (Information Technology, Beta: 1.02)
- **TCS**: Tata Consultancy Services (IT Services, Beta: 0.82)
- **ZOMATO**: Zomato Ltd (Consumer Tech / Quick Commerce, Beta: 1.85)
- **SBIN**: State Bank of India (PSU Banking, Beta: 1.15)
- **BHARTIARTL**: Bharti Airtel Ltd (Telecom & Cloud, Beta: 0.78)
- **ITC**: ITC Ltd (FMCG & Diversified, Beta: 0.65)
- **BAJFINANCE**: Bajaj Finance Ltd (NBFC / Lending, Beta: 1.35)
- **LT**: Larsen & Toubro Ltd (Infrastructure & Defense, Beta: 1.10)
- **MARUTI**: Maruti Suzuki India Ltd (Passenger Vehicles, Beta: 0.88)
- **SUNPHARMA**: Sun Pharmaceutical Industries (Healthcare & Pharma, Beta: 0.58)

### B. Foreign / US Mega-Cap Equities (NASDAQ Universe)
- **NVDA**: NVIDIA Corporation (AI Semiconductors & GPU Compute, Beta: 1.72, Currency: USD)
- **AAPL**: Apple Inc. (Consumer Devices & Ecosystem Services, Beta: 0.94, Currency: USD)
- **MSFT**: Microsoft Corporation (Enterprise Cloud AI & Copilot, Beta: 0.89, Currency: USD)
- **TSLA**: Tesla, Inc. (Electric Vehicles & AI Robotics, Beta: 2.15, Currency: USD)
- **GOOGL**: Alphabet Inc. (Search & Cloud Infrastructure, Beta: 1.05, Currency: USD)
- **AMZN**: Amazon.com, Inc. (Global E-Commerce & AWS Cloud, Beta: 1.15, Currency: USD)

---

## 3. Multi-Currency Support (INR & USD)
- **Indian Equities**: Denominated in Indian Rupees (`INR` / `₹`).
- **US Equities**: Denominated in US Dollars (`USD` / `$`).
- **Cross-Market Comparison**: Users can evaluate domestic and international investments side-by-side conditioned on their risk profile.

---

## 4. Data Quality & Anomaly Validation

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
