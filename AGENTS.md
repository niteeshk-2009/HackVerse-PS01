# SPY THE MARKET — Agent Specification & Output Contracts

All agents in **SPY THE MARKET** implement strictly typed Pydantic contracts, ensuring that agents communicate structured signals rather than unstructured prose.

---

## 1. Global Typed Contract Definitions

```python
class DataSourceState(str, Enum):
    LIVE_DATA = "LIVE DATA"
    DEMO_DATA = "DEMO DATA"
    DATA_UNAVAILABLE = "DATA UNAVAILABLE"

class SignalClassification(str, Enum):
    STRONG_BULLISH = "STRONG_BULLISH"
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    STRONG_BEARISH = "STRONG_BEARISH"
    CONFLICTING = "CONFLICTING"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"

class AgentSignal(BaseModel):
    dimension: str              # e.g., 'Price Momentum', 'Volume Anomaly', 'Oscillators'
    classification: SignalClassification
    score: float                # -100 to +100
    confidence: float           # 0.0 to 100.0%
    evidence_reasoning: str     # Inspectable reasoning statement

class AgentOutput(BaseModel):
    agent_name: str
    role: str
    status: str                 # 'SUCCESS', 'WARNING', 'DATA_UNAVAILABLE'
    signal: SignalClassification
    score: float                # Normalized score (-100 to +100)
    confidence: float           # Confidence percentage (0 to 100%)
    signals: List[AgentSignal]  # Dimension-level breakdown
    reasoning: List[str]        # Causal bullet points
    evidence: List[AgentEvidence]# Retrieved RAG evidence chunks
    risks: List[str]            # Highlighted risk factors
    metrics: Dict[str, Any]     # Numerical telemetry
    data_source_state: DataSourceState
    execution_time_ms: float
    timestamp: str
```

---

## 2. Agent 1: Market Spider
- **Role**: Technical & Market Momentum Analyst
- **Input**: Current quote, moving averages (EMA 20/50/200), volume multiplier, delivery percentage, RSI-14, MACD, ATR, Beta.
- **Evaluation Dimensions**:
  1. *Price Momentum*: Tests exponential moving average alignment and MACD histogram slope.
  2. *Volume Anomaly*: Evaluates volume surge factor against the 20-day baseline and checks delivery percentage to separate real institutional accumulation from speculative churning.
  3. *Volatility & Oscillators*: Inspects RSI-14 for overbought/oversold boundaries and beta sensitivity.
- **Failure Behavior**: If tick feeds are interrupted, falls back to the last cached snapshot, downgrades status to `WARNING`, and discounts technical confidence by 40%.

---

## 3. Agent 2: Fundamental Web
- **Role**: Fundamental & Regulatory Intelligence Analyst
- **Input**: Ticker symbol, financial metrics (P/E, Debt-to-Equity, P/B), and RAG vector search corpus.
- **Semantic RAG Grounding**:
  - Executes semantic similarity retrieval across SEBI LODR disclosures and quarterly earnings transcripts.
  - Extracts the top matching chunks and embeds citations with source title, section, page, and excerpt.
- **Failure Behavior**: If corporate disclosures are missing or unindexed, sets status to `DATA_UNAVAILABLE`, confidence to 42%, and refuses to generate fabricated assertions.

---

## 4. Agent 3: Sentiment Spider
- **Role**: Sentiment & Flow Intelligence Analyst
- **Input**: FII/DII net flows (Crores), public news sentiment index (0-100), retail options chase indicator (0-100).
- **Retail Trap Detection**:
  - Flags classic retail trap divergences where retail call buying is in euphoria (>80/100) while institutional FIIs are liquidating (-INR 400+ Cr).
- **Failure Behavior**: Defaults to neutral baseline with conservative weighting if external social APIs fail.

---

## 5. Agent 4: Risk Guardian
- **Role**: Personalized Portfolio & Behavioral Risk Intelligence
- **Input**: Full `UserProfile`, including portfolio holdings, cash balance, sector allocations, loss aversion index, and risk tolerance (`CONSERVATIVE`, `MODERATE`, `AGGRESSIVE`).
- **Mathematical Models**:
  - Computes Herfindahl-Hirschman Index (HHI) for concentration risk.
  - Compares asset beta against investor risk tolerance.
  - Calculates cash reserve cushion percentage.
