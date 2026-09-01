# SPY THE MARKET — 60-Second Judge Demonstration Playbook

This guide outlines the optimal demonstration flow for hackathon judges to verify all core capabilities of **SPY THE MARKET (PS-01)** in under 60 seconds.

---

## 🕒 The 60-Second Judge Flow

```
[00:00 - 00:15] Hook & Problem Context (The SEBI 89% Retail Loss Asymmetry)
       ↓
[00:15 - 00:30] Live Multi-Agent Cockpit (Moving Tick Chart + 4 Independent Agents + RAG)
       ↓
[00:30 - 00:45] Head-to-Head Investment Duel (Side-by-Side 2 Stocks Comparison)
       ↓
[00:45 - 00:60] System Resilience & Degraded Data (Zero-Hallucination & Retail Traps)
```

---

## Step 1: Hook the Judges (00:00 - 00:15)
**Say this:**
> *"Judges, official SEBI study reveals that 89% of retail F&O traders in India lose money. The failure isn't lack of data — NSE ticks, corporate filings, and institutional flows are public. It's an infrastructure gap: hedge funds have parallel multi-analyst teams synthesizing petabytes in seconds, while retail investors get Telegram tips and a price chart.*  
> *We built **SPY THE MARKET**: an autonomous multi-agent financial intelligence system that brings hedge-fund multi-perspective reasoning to retail investors in real time."*

---

## Step 2: The End-to-End Multi-Agent Cockpit (00:15 - 00:30)
**Action:**
Show the live **Cockpit & 4 Agents** view.

**Point to the screen:**
1. **Live Moving Tick Chart**:
   - Continuously streaming NSE ticks with overlaid 20-day EMA strictly bound to real-time timestamps (no future hours).
2. **The Web Mind Master Synthesis**:
   - Synthesized recommendation: **"GRADUAL STAGGERED ACCUMULATION (SIP)"**.
   - Execution latency: **~29 milliseconds** (measured runtime latency, beating the 60s requirement).
   - Tailored decision rationale answering the 5 core investor questions.
3. **The 4 Specialized Agents Executing in Parallel**:
   - **Market Spider**: 3 independent dimensions (Price Momentum, Volume Surge 1.61x, Oscillators).
   - **Fundamental Web**: Semantic Vector RAG over Q2 FY26 SEBI corporate filings with exact quote citations.
   - **Sentiment Spider**: Institutional FII net flow vs Retail Option FOMO Chase Index.
   - **Risk Guardian**: Herfindahl-Hirschman Index (HHI) concentration score and maximum safe position cap.

---

## Step 3: Head-to-Head Investment Duel (00:30 - 00:45)
**Action:**
Click the **"Compare 2 Stocks"** tab in the top navigation.
Select **Asset A** (e.g. `TATAMOTORS`) and **Asset B** (e.g. `RELIANCE`), then click **"Compare Now"**.

**Point to the screen:**
> *"Here is our comparative intelligence engine: We evaluate both securities simultaneously through all 4 specialized agents conditioned on your personal risk appetite."*
- Side-by-side analysis cards comparing live price, P/E, Beta, ROE %, and 4 agent scores.
- **Comparative Decision Winner**: Explicitly declares which asset delivers superior risk-adjusted return tailored to this specific user's capital and portfolio allocation state.

---

## Step 4: System Resilience & Degraded-Data Stress Testing (00:45 - 00:60)
**Action:**
Click the **"Stress Testing"** tab and click **⚡ Conflict (Retail Trap)** or **⚠ Missing SEBI Filing**.

**Point to the screen:**
- **Conflict (Retail Trap)**:
  - Technicals are Bullish (+74) but Sentiment detects heavy institutional distribution (-₹480 Cr).
  - The Web Mind detects divergence, discounts momentum weight by 40%, and triggers a mandatory 2.0% stop-loss guardrail.
- **Missing SEBI Filing**:
  - Fundamental Web reports `DATA_UNAVAILABLE`.
  - The system refuses to hallucinate unverified financial statements, activates Anti-Hallucination Safe Mode, and changes recommendation to **`WAIT / DATA DEGRADATION SAFEGUARD`**.
- **Real-Time Telemetry Log**:
  - Point to the SQLite session performance telemetry table below, showing real-time latency and HHI tracking.

---

## Mandatory Compliance Disclaimer
*This product provides AI-generated financial intelligence for informational and educational purposes and is not financial advice.*
