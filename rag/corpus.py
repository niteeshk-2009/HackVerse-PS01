"""
SPIDER-SENSE: Curated Financial Document Corpus
Authentic Indian equity regulatory disclosures, SEBI filings, earnings call transcripts,
and management commentary for semantic RAG grounding.
"""

from typing import List, Dict

FINANCIAL_CORPUS: List[Dict[str, str]] = [
    # --- TATA MOTORS (TATAMOTORS) ---
    {
        "doc_id": "TATAMOTORS_Q2FY26_EARNINGS",
        "ticker": "TATAMOTORS",
        "title": "Tata Motors Ltd - Q2 FY26 Investor Disclosure & Earnings Transcript",
        "section": "Operating Performance & JLR Margins (Page 3)",
        "date": "2026-08-14",
        "text": "Tata Motors reported a consolidated revenue expansion of 14.8% YoY driven by Jaguar Land Rover (JLR) commercial strength and premium Defender/Range Rover order books. Consolidated EBIT margins improved by 180 bps to 8.6%. Free cash flow generation in the automotive business reached INR 4,200 Crores, enabling management to reaffirm its net zero automotive debt target by end of FY26. Domestic commercial vehicle (CV) volume registered modest 3.2% growth amidst post-election infrastructure capex ramp-up.",
        "keywords": ["revenue", "jlr", "ebit", "debt", "cash flow", "margins", "commercial vehicle"]
    },
    {
        "doc_id": "TATAMOTORS_SEBI_FILING_EV",
        "ticker": "TATAMOTORS",
        "title": "Tata Motors Ltd - SEBI LODR Reg 30 Disclosure on EV Subsidiary Investment",
        "section": "Material Corporate Event (Annexure A)",
        "date": "2026-08-22",
        "text": "Pursuant to Regulation 30 of SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015, the Board of Directors approved an equity infusion of INR 2,500 Crores into its electric mobility arm (TPEML) to scale next-gen 'acti.ev' architecture and battery cell manufacturing localization. Management confirmed domestic electric passenger vehicle market share stands at 68.4%, though subsidy rationalization under FAME-III transition remains an operating margin headwind in the sub-15 lakh passenger segment.",
        "keywords": ["ev", "sebi", "investment", "tpeml", "subsidy", "market share", "electric"]
    },
    {
        "doc_id": "TATAMOTORS_RISK_DISCLOSURE",
        "ticker": "TATAMOTORS",
        "title": "Tata Motors Ltd - Annual Risk Governance Disclosure",
        "section": "Risk Factors & Supply Chain Sensitivities (Item 18)",
        "date": "2026-06-30",
        "text": "The company's commercial profitability remains exposed to global aluminum and rare-earth semiconductor component price volatility. British Pound (GBP) and Euro currency fluctuations directly impact JLR repatriation cash flows. Furthermore, domestic fleet operators cite elevated interest rates on commercial vehicle loans as a reason for postponed fleet replacement cycles.",
        "keywords": ["risk", "semiconductor", "currency", "gbp", "interest rates", "supply chain"]
    },

    # --- RELIANCE INDUSTRIES (RELIANCE) ---
    {
        "doc_id": "RELIANCE_Q2FY26_EARNINGS",
        "ticker": "RELIANCE",
        "title": "Reliance Industries Ltd - Q2 FY26 Earnings Conference Presentation",
        "section": "Segmental EBITDA & New Energy Giga-Factory (Slide 9)",
        "date": "2026-08-10",
        "text": "Reliance Industries recorded consolidated quarterly EBITDA of INR 44,800 Crores (+11.2% YoY). Jio Infocomm ARPU expanded to INR 194.5 following tariff adjustments and 5G subscriber monetization. Reliance Retail added 420 new stores with footfall increasing 18%. Jamnagar New Energy complex commenced trial production of solar PV modules, with management reiterating INR 75,000 Crore green energy capex milestone. Oil-to-Chemicals (O2C) segment faced regional refining margin compression offset by domestic downstream fuel demand.",
        "keywords": ["ebitda", "arpu", "jio", "retail", "new energy", "solar", "o2c", "margins"]
    },
    {
        "doc_id": "RELIANCE_SEBI_DISCLOSURE_DEBT",
        "ticker": "RELIANCE",
        "title": "Reliance Industries Ltd - SEBI Reg 52 Debt & Capital Allocation Disclosure",
        "section": "Balance Sheet Covenants (Note 7)",
        "date": "2026-07-28",
        "text": "Net debt to EBITDA ratio stood conservatively at 0.68x, well below credit covenant ceiling of 2.5x. Capital expenditure for the trailing 12 months moderated to INR 118,000 Crores as nationwide 5G rollout entered operating phase. No promoter shares are encumbered or pledged. Working capital facilities retain AAA domestic rating with stable outlook.",
        "keywords": ["debt", "capex", "ebitda", "pledge", "credit rating", "5g", "balance sheet"]
    },

    # --- HDFC BANK (HDFCBANK) ---
    {
        "doc_id": "HDFCBANK_Q2FY26_FINANCIALS",
        "ticker": "HDFCBANK",
        "title": "HDFC Bank Ltd - Q2 FY26 Financial Results & Pillar III Report",
        "section": "NIM Trajectory & Credit-to-Deposit Normalization (Page 6)",
        "date": "2026-08-18",
        "text": "HDFC Bank delivered net profit of INR 17,850 Crores, registering 15.6% YoY growth. Net Interest Margin (NIM) stabilized at 3.52% post-merger integration. The bank achieved significant progress on credit-to-deposit (LDR) ratio reduction, declining to 99.4% from 108% in previous quarters through deposit mobilization drives (deposits grew 16.2% YoY). Gross NPA remained pristine at 1.24% with provision coverage ratio (PCR) at 74.8%. Management indicated branch expansion will moderate to 500 branches in FY26 to prioritize operating leverage.",
        "keywords": ["nim", "npa", "deposits", "credit", "ldr", "merger", "profit", "hdfc"]
    },
    {
        "doc_id": "HDFCBANK_RBI_REGULATORY_NOTE",
        "ticker": "HDFCBANK",
        "title": "HDFC Bank Ltd - Regulatory Compliance & Liquidity Coverage Disclosure",
        "section": "Statutory Liquidity & RBI Basel III Guidelines",
        "date": "2026-08-01",
        "text": "Liquidity Coverage Ratio (LCR) averaged 128% during the quarter against regulatory requirement of 100%. Tier-1 Capital Adequacy Ratio stood robust at 17.2%. The bank confirmed complete closure of legacy HDFC Ltd regulatory transition tasks with zero penalties imposed by Reserve Bank of India. Unsecured retail lending growth was intentionally dialed back to 9% YoY following RBI risk-weight calibration on consumer credit.",
        "keywords": ["rbi", "lcr", "capital adequacy", "basel", "unsecured", "compliance"]
    },

    # --- ZOMATO (ZOMATO) ---
    {
        "doc_id": "ZOMATO_Q2FY26_DISCLOSURE",
        "ticker": "ZOMATO",
        "title": "Zomato Ltd (Eternal) - Q2 FY26 Shareholder Letter & Filings",
        "section": "Blinkit Quick Commerce Dark Store Economics (Page 8)",
        "date": "2026-08-25",
        "text": "Blinkit gross order value (GOV) surged 112% YoY, maintaining positive adjusted EBITDA at the dark store level. Quick commerce store count reached 1,150 across top 30 cities with average delivery time of 11.4 minutes. Food delivery GOV expanded 19% YoY with contribution margin holding steady at 7.4% of GOV. Cash and liquid investments stood at INR 11,800 Crores, providing ample liquidity for 'District' going-out app launch and logistics warehouse automation.",
        "keywords": ["blinkit", "quick commerce", "gov", "ebitda", "cash", "food delivery", "dark store"]
    },
    {
        "doc_id": "ZOMATO_SEBI_RISK_COMPETITION",
        "ticker": "ZOMATO",
        "title": "Zomato Ltd - Regulatory Risk Factor Disclosure & MCA Filings",
        "section": "Competitive Landscape & Gig Worker Welfare Compliance",
        "date": "2026-07-15",
        "text": "Intensifying competition in quick commerce from well-capitalized entrants (Zepto, Swiggy Instamart, and Flipkart Minutes) has elevated customer acquisition costs and warehouse lease rentals in Tier-1 micro-markets. Additionally, state legislative proposals regarding mandatory gig worker social security funds and accident cess may elevate delivery partner payout costs by 2.5-4.0% per order if enacted across Karnataka and Maharashtra.",
        "keywords": ["competition", "quick commerce", "gig worker", "regulation", "swiggy", "costs"]
    },

    # --- INFOSYS (INFY) ---
    {
        "doc_id": "INFOSYS_Q2FY26_TRANSCRIPT",
        "ticker": "INFY",
        "title": "Infosys Ltd - Q2 FY26 Earnings Call & Guidance Disclosure",
        "section": "Enterprise AI Topaz Pipeline & US Banking Tech Spending",
        "date": "2026-08-12",
        "text": "Infosys upwardly revised constant currency FY26 revenue guidance to 4.5%-5.5%. Large deal Total Contract Value (TCV) stood at $3.4 Billion with 54% net new deals. Enterprise generative AI suite 'Topaz' is currently embedded into 420+ active client engagements, driving productivity gains of 18-25% in application maintenance and cloud migration. Operating margins held firm at 21.2%. Attrition dropped to a comfortable 12.1%. Discretionary tech spending in European retail and manufacturing showed early signs of rebound.",
        "keywords": ["topaz", "ai", "revenue", "guidance", "tcv", "margin", "attrition", "cloud"]
    },

    # --- TATA CONSULTANCY SERVICES (TCS) ---
    {
        "doc_id": "TCS_Q2FY26_TRANSCRIPT",
        "ticker": "TCS",
        "title": "TCS Ltd - Q2 FY26 Earnings Conference & SEBI Disclosures",
        "section": "AI Transformation Pipeline & Order Book (Page 4)",
        "date": "2026-08-10",
        "text": "TCS recorded quarterly revenue of INR 64,250 Crores (+7.6% YoY) with operating margin expanding to 25.1%. The company's AI order pipeline doubled to $1.5 Billion, led by enterprise adoption of TCS AI WisdomNext. North American BFSI client budgets showed broad-based stabilization, while UK and European manufacturing contracts delivered record cash collections. Board declared interim dividend of INR 28 per share with net debt remaining zero.",
        "keywords": ["tcs", "revenue", "ai", "wisdomnext", "order book", "dividend", "margin", "bfsi"]
    },

    # --- ICICI BANK (ICICIBANK) ---
    {
        "doc_id": "ICICIBANK_Q2FY26_FINANCIALS",
        "ticker": "ICICIBANK",
        "title": "ICICI Bank Ltd - Q2 FY26 Financial Statement & Pillar III",
        "section": "Asset Quality, Core Operating Profit & NIM (Page 5)",
        "date": "2026-08-16",
        "text": "ICICI Bank reported standalone net profit of INR 11,740 Crores (+14.5% YoY). Net Interest Margin (NIM) stood resilient at 4.36%. Domestic loan portfolio grew 15.7% YoY driven by business banking and secured retail mortgages. Gross NPA declined 20 bps YoY to 2.15%, with net NPA dropping to 0.42%. Capital adequacy ratio (CAR) under Basel III stood at 16.8%, providing significant buffer for credit expansion.",
        "keywords": ["icici", "nim", "profit", "npa", "loan", "retail", "mortgages", "capital adequacy"]
    },

    # --- STATE BANK OF INDIA (SBIN) ---
    {
        "doc_id": "SBIN_Q2FY26_DISCLOSURE",
        "ticker": "SBIN",
        "title": "State Bank of India - Q2 FY26 Analyst Disclosure & Concall",
        "section": "Credit Growth & YONO Digital Ingestion (Page 7)",
        "date": "2026-08-08",
        "text": "State Bank of India achieved record quarterly net profit of INR 18,330 Crores. Gross Advances grew 14.8% YoY crossing INR 39 Lakh Crores, spearheaded by infrastructure and SME term lending. Corporate credit pipeline stood at INR 4.8 Lakh Crores. YONO digital platform onboarded 62% of new retail savings accounts. Gross NPA improved to 2.21% with provision coverage at 76.5%. Return on Equity (ROE) reached 17.2%.",
        "keywords": ["sbi", "sbin", "advances", "yono", "profit", "npa", "roe", "sme"]
    },

    # --- BHARTI AIRTEL (BHARTIARTL) ---
    {
        "doc_id": "BHARTIARTL_Q2FY26_FILING",
        "ticker": "BHARTIARTL",
        "title": "Bharti Airtel Ltd - SEBI Reg 30 Investor Presentation",
        "section": "ARPU Expansion & Airtel Business Enterprise Cloud",
        "date": "2026-08-05",
        "text": "Bharti Airtel India mobile ARPU surged to INR 233 from INR 203 following industry-wide tariff adjustments and 4G/5G customer upgrades. Free cash flow generation reached INR 12,400 Crores for the quarter. Airtel Business enterprise cloud and IoT revenues expanded 16.4% YoY. Net debt to EBITDA improved to 1.65x, with management accelerating debt prepayments for 5G spectrum obligations.",
        "keywords": ["airtel", "arpu", "telecom", "5g", "cash flow", "tariff", "debt"]
    },

    # --- ITC LIMITED (ITC) ---
    {
        "doc_id": "ITC_Q2FY26_DISCLOSURE",
        "ticker": "ITC",
        "title": "ITC Ltd - Q2 FY26 Corporate Filings & Hotel Demerger Update",
        "section": "FMCG-Others Scale & Agri Business Margins",
        "date": "2026-08-14",
        "text": "ITC reported gross revenue growth of 7.2% YoY with FMCG-Others revenue crossing INR 5,600 Crores for the quarter. Cigarette segment recorded stable volume growth (+4.2%) amidst favorable tax predictability. Demerger of the Hotels business into ITC Hotels Ltd reached final NCLT sanctioned stage for separate listing. Operating cash flow stood at INR 5,200 Crores with zero borrowings on balance sheet.",
        "keywords": ["itc", "fmcg", "cigarette", "hotel", "demerger", "cash flow", "dividend"]
    },

    # --- BAJAJ FINANCE (BAJFINANCE) ---
    {
        "doc_id": "BAJFINANCE_Q2FY26_FILING",
        "ticker": "BAJFINANCE",
        "title": "Bajaj Finance Ltd - SEBI LODR Quarterly Financial Disclosure",
        "section": "AUM Growth & Omnichannel Digital App Metrics",
        "date": "2026-08-20",
        "text": "Bajaj Finance Assets Under Management (AUM) expanded 29% YoY to INR 3,74,000 Crores. New customer acquisition during the quarter stood at 3.9 Million. Net Interest Margin normalized to 9.8%. The company’s digital payments and EMI card active base crossed 48 Million users. Gross NPA held at 0.98% while maintaining liquidity buffer of INR 14,500 Crores against short-term commercial paper redemptions.",
        "keywords": ["bajaj", "bajfinance", "aum", "nbfc", "lending", "emi", "npa", "margin"]
    },

    # --- LARSEN & TOUBRO (LT) ---
    {
        "doc_id": "LT_Q2FY26_ORDERBOOK",
        "ticker": "LT",
        "title": "Larsen & Toubro Ltd - Q2 FY26 Investor Factsheet & SEBI LODR",
        "section": "Infrastructure Order Inflows & Middle East Energy Transition",
        "date": "2026-08-15",
        "text": "L&T consolidated order book reached an all-time high of INR 5,10,000 Crores with international orders contributing 38%. Infrastructure and hydrocarbon segments delivered revenue expansion of 18.2% YoY. Working capital to revenue ratio improved to 12.2% from 15.4%. Management reaffirmed full-year order inflow guidance of 15% YoY growth, driven by domestic railways, high-speed rail, and Saudi Aramco renewable contracts.",
        "keywords": ["lt", "larsen", "infrastructure", "order book", "capex", "hydrocarbon", "saudi"]
    },

    # --- MARUTI SUZUKI (MARUTI) ---
    {
        "doc_id": "MARUTI_Q2FY26_DISCLOSURE",
        "ticker": "MARUTI",
        "title": "Maruti Suzuki India Ltd - Q2 FY26 Earnings Conference",
        "section": "SUV Market Share & Hybrid Powertrain Strategy",
        "date": "2026-08-11",
        "text": "Maruti Suzuki consolidated quarterly sales volume stood at 5,42,000 units with SUV segment market share rising to 24.8%. Strong hybrid powertrain variants accounted for 14% of Grand Vitara and Invicto sales. Raw material cost deflation in steel and precious metals supported operating margin expansion to 11.8%. Cash reserves and financial investments exceeded INR 52,000 Crores, funding the upcoming Kharkhoda 1-million unit plant capex.",
        "keywords": ["maruti", "suv", "hybrid", "auto", "volume", "margins", "cash"]
    },

    # --- SUN PHARMA (SUNPHARMA) ---
    {
        "doc_id": "SUNPHARMA_Q2FY26_FILING",
        "ticker": "SUNPHARMA",
        "title": "Sun Pharmaceutical Industries - Q2 FY26 Earnings Release",
        "section": "Global Specialty Portfolio & US FDA Approvals",
        "date": "2026-08-19",
        "text": "Sun Pharma global specialty revenues grew 19.2% YoY to $315 Million, driven by Ilumya, Cequa, and Winlevi dermatological adoption. India formulation sales expanded 11.4% YoY outpacing Indian Pharma Market (IPM) benchmark. R&D spending stood at 6.2% of sales dedicated to specialty clinical trials. Consolidated EBITDA margins reached 27.4% with zero long-term debt.",
        "keywords": ["sunpharma", "pharma", "specialty", "ilumya", "usfda", "ebitda", "r&d", "formulation"]
    }
]

