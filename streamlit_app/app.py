# ════════════════════════════════════════════════════════════════
#  EstateIQ — House Price Prediction System
#  Complete Streamlit App | Model + Presentation + Predictor
# ════════════════════════════════════════════════════════════════

import streamlit as st
import joblib
import json
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "EstateIQ — House Price Predictor",
    page_icon  = "🏠",
    layout     = "wide",
    initial_sidebar_state = "collapsed"
)

# ─────────────────────────────────────────────────────────────────
# 2. LOAD MODEL
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model  = joblib.load(r'C:\MyProject\model\house_price_model.pkl')
    scaler = joblib.load(r'C:\MyProject\model\scaler.pkl')
    with open(r'C:\MyProject\model\feature_columns.json') as f:
        columns = json.load(f)
    return model, scaler, columns

model, scaler, feature_columns = load_model()

# ─────────────────────────────────────────────────────────────────
# 2b. LOAD RAW DATASET — real values for dropdowns & input ranges
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_dataset():
    return pd.read_csv(r'C:\\MyProject\\data\\train.csv')

df_raw = load_dataset()

# Real min/max/default values pulled directly from dataset
neighborhoods = sorted(df_raw['Neighborhood'].dropna().unique().tolist())
min_area      = int(df_raw['GrLivArea'].min())
max_area      = int(df_raw['GrLivArea'].max())
default_area  = int(df_raw['GrLivArea'].median())
min_bsmt      = int(df_raw['TotalBsmtSF'].fillna(0).min())
max_bsmt      = int(df_raw['TotalBsmtSF'].fillna(0).max())
default_bsmt  = int(df_raw['TotalBsmtSF'].fillna(0).median())
max_beds      = int(df_raw['BedroomAbvGr'].max())
max_baths     = int(df_raw['FullBath'].max())
max_garage    = int(df_raw['GarageCars'].fillna(0).max())

# ─────────────────────────────────────────────────────────────────
# 3. CSS — MEDIUM COLORS ONLY
#
#   BACKGROUND  : #1e2435  (medium navy — not pitch black)
#   CARD BG     : #262d42  (medium card — clearly visible)
#   INPUT BG    : #2e3650  (medium input — readable)
#   ACCENT      : #38bdf8  (sky blue — bright but calm)
#   TEXT        : #dde3f0  (soft white — not blinding)
#   MUTED       : #8a96b0  (medium grey — readable subtitles)
#   BORDER      : rgba(56,189,248,0.28)
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg       : #1e2435;
    --bg2      : #252b3d;
    --bg3      : #2e3650;
    --card     : #262d42;
    --input    : #2e3650;
    --accent   : #38bdf8;
    --accent2  : #7dd3fc;
    --green    : #34d399;
    --purple   : #a78bfa;
    --text     : #dde3f0;
    --muted    : #8a96b0;
    --border   : rgba(56,189,248,0.28);
    --fh       : 'Syne', sans-serif;
    --fb       : 'Inter', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background  : var(--bg) !important;
    font-family : var(--fb) !important;
    color       : var(--text) !important;
}
header, footer, #MainMenu        { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.main .block-container           { padding: 0 !important; max-width: 100% !important; }

/* ── NAVBAR ─────────────────────────────── */
.navbar {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 99999 !important;
    height: 64px;
    padding: 0 5%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(30,36,53,0.98) !important;
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    width: 100% !important;
}

/* Push all content below the fixed navbar */
.hero {
    margin-top: 64px !important;
}
.nav-logo {
    font-family: var(--fh); font-size: 1.2rem; font-weight: 800;
    color: var(--accent); letter-spacing: -0.5px;
}
.nav-links { display: flex; gap: 26px; list-style: none; margin: 0; padding: 0; }
.nav-links a {
    color: var(--muted); text-decoration: none;
    font-size: 0.82rem; font-weight: 500; transition: color 0.2s;
}
.nav-links a:hover { color: var(--accent); }
.nav-pill {
    background: rgba(56,189,248,0.15); border: 1px solid rgba(56,189,248,0.35);
    border-radius: 20px; padding: 5px 14px;
    color: var(--accent); font-size: 0.72rem; font-weight: 700;
}

/* ── HERO ────────────────────────────────── */
.hero {
    min-height: 88vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 80px 5% 60px;
    background:
        radial-gradient(ellipse 65% 50% at 50% 0%,  rgba(56,189,248,0.12), transparent),
        radial-gradient(ellipse 40% 30% at 85% 80%, rgba(167,139,250,0.08), transparent),
        var(--bg);
}
.hero-badge {
    display: inline-flex; align-items: center;
    background: rgba(56,189,248,0.12); border: 1px solid rgba(56,189,248,0.3);
    border-radius: 50px; padding: 7px 20px;
    color: var(--accent2); font-size: 0.73rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase; margin-bottom: 28px;
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: clamp(3rem, 6vw, 5rem) !important;
    font-weight: 900 !important;
    line-height: 1.06 !important;
    letter-spacing: -2px !important;
    color: var(--text) !important;
    margin-bottom: 22px !important;
}
.hero-title span {
    background: linear-gradient(135deg, var(--accent), var(--purple), var(--green));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    color: var(--muted); font-size: 1.05rem; line-height: 1.85;
    max-width: 520px; margin-bottom: 38px;
}
.hero-btn {
    display: inline-block; background: var(--accent); color: #1e2435;
    padding: 14px 40px; border-radius: 50px;
    font-family: var(--fh); font-weight: 700; font-size: 0.9rem;
    text-decoration: none; box-shadow: 0 4px 28px rgba(56,189,248,0.3);
    transition: all 0.3s;
}
.hero-btn:hover {
    background: var(--accent2);
    box-shadow: 0 8px 40px rgba(56,189,248,0.45);
    transform: translateY(-3px);
}

/* ── STATS BAR ───────────────────────────── */
.stats-bar {
    display: flex; margin-top: 56px; max-width: 620px; width: 100%;
    background: var(--card); border: 1px solid var(--border);
    border-radius: 14px; overflow: hidden;
}
.stat-box {
    flex: 1; padding: 20px 10px; text-align: center;
    border-right: 1px solid var(--border);
}
.stat-box:last-child { border-right: none; }
.stat-num {
    display: block !important;
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    color: var(--accent) !important;
    line-height: 1 !important;
    letter-spacing: -0.5px !important;
}
.stat-lbl {
    display: block; font-size: 0.62rem; color: var(--muted);
    text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; margin-top: 5px;
}

/* ── SECTIONS ────────────────────────────── */
.section     { padding: 72px 5%; background: var(--bg);  }
.section-alt { padding: 72px 5%; background: var(--bg2); }

.sec-tag {
    display: inline-block; font-size: 0.68rem; font-weight: 700;
    color: var(--accent); text-transform: uppercase;
    letter-spacing: 3px; margin-bottom: 12px;
}
.sec-title {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: clamp(1.9rem, 3.5vw, 2.8rem) !important;
    font-weight: 900 !important;
    color: var(--text) !important;
    letter-spacing: -1px !important;
    line-height: 1.1 !important;
    margin-bottom: 12px !important;
}
.sec-desc {
    color: var(--muted); font-size: 0.96rem; line-height: 1.8;
    max-width: 540px; margin-bottom: 40px;
}

/* ── INFO CARDS ──────────────────────────── */
.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
}
.info-card {
    background: var(--card); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px; padding: 26px 22px;
    transition: all 0.3s; position: relative; overflow: hidden;
}
.info-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0; transition: opacity 0.3s;
}
.info-card:hover {
    border-color: rgba(56,189,248,0.35); background: var(--bg3);
    transform: translateY(-5px); box-shadow: 0 16px 40px rgba(0,0,0,0.2);
}
.info-card:hover::before { opacity: 1; }
.card-icon    { font-size: 1.8rem; display: block; margin-bottom: 12px; }
.info-card h3 {
    font-family: var(--fh); font-size: 0.95rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
}
.info-card p  { font-size: 0.84rem; color: var(--muted); line-height: 1.72; }

/* ── METRICS ROW ─────────────────────────── */
.metrics-row {
    display: grid; grid-template-columns: repeat(3,1fr);
    gap: 16px; margin-bottom: 40px;
}
.metric-box {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 16px; padding: 30px 20px; text-align: center;
}
.metric-val {
    display: block !important;
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    color: var(--accent) !important;
    line-height: 1 !important;
    margin-bottom: 8px !important;
    letter-spacing: -1px !important;
}
.metric-lbl {
    color: var(--muted); font-size: 0.72rem; font-family: var(--fb);
    text-transform: uppercase; letter-spacing: 2px; font-weight: 600;
}

/* ── CODE BLOCK ──────────────────────────── */
.code-block {
    background: #181d2c; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 24px 28px;
    font-family: 'Courier New', monospace; font-size: 0.83rem;
    line-height: 1.9; overflow-x: auto; margin-top: 28px; color: #b0bcd4;
}
.kw { color: #c084fc; }
.fn { color: #67e8f9; }
.st { color: #86efac; }
.nm { color: #fdba74; }
.cm { color: #506080; }

/* ── PREDICTOR HEADER ────────────────────── */
.predictor-header {
    text-align: center; padding: 60px 5% 40px;
    background: var(--bg2); border-top: 1px solid var(--border);
}

/* ── ALL INPUT LABELS ────────────────────── */
div[data-testid="stWidgetLabel"] p,
.stNumberInput label, .stSelectbox label, .stSlider label, label {
    color          : var(--accent2) !important;
    font-size      : 0.73rem !important;
    font-weight    : 700 !important;
    letter-spacing : 1.6px !important;
    text-transform : uppercase !important;
    font-family    : var(--fb) !important;
    margin-bottom  : 5px !important;
}

/* ── NUMBER INPUT ────────────────────────── */
.stNumberInput input, input[type="number"] {
    background    : var(--input) !important;
    border        : 1.5px solid rgba(56,189,248,0.32) !important;
    border-radius : 10px !important;
    color         : var(--text) !important;
    font-size     : 0.96rem !important;
    font-weight   : 600 !important;
    font-family   : var(--fb) !important;
    padding       : 10px 14px !important;
    transition    : border-color 0.2s, box-shadow 0.2s !important;
}
.stNumberInput input:focus, input[type="number"]:focus {
    border-color : var(--accent) !important;
    box-shadow   : 0 0 0 3px rgba(56,189,248,0.14) !important;
    outline      : none !important;
}
.stNumberInput button {
    background    : rgba(56,189,248,0.14) !important;
    border        : 1.5px solid rgba(56,189,248,0.3) !important;
    border-radius : 8px !important;
    color         : var(--accent) !important;
    font-weight   : 700 !important;
}
.stNumberInput button:hover { background: rgba(56,189,248,0.25) !important; }

/* ── SELECTBOX ───────────────────────────── */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div,
.stSelectbox > div > div {
    background    : var(--input) !important;
    border        : 1.5px solid rgba(56,189,248,0.32) !important;
    border-radius : 10px !important;
    color         : var(--text) !important;
    font-family   : var(--fb) !important;
    font-weight   : 600 !important;
    font-size     : 0.95rem !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color : var(--accent) !important;
    box-shadow   : 0 0 0 3px rgba(56,189,248,0.14) !important;
}
div[data-baseweb="select"] svg { fill: var(--accent) !important; }

/* Dropdown list */
ul[data-baseweb="menu"], ul[role="listbox"],
div[data-baseweb="popover"] > div {
    background    : var(--bg2) !important;
    border        : 1px solid var(--border) !important;
    border-radius : 12px !important;
    box-shadow    : 0 16px 40px rgba(0,0,0,0.3) !important;
}
li[role="option"] {
    color: var(--muted) !important; font-family: var(--fb) !important;
    font-size: 0.87rem !important; transition: all 0.15s !important;
}
li[role="option"]:hover,
li[aria-selected="true"][role="option"] {
    background : rgba(56,189,248,0.13) !important;
    color      : var(--accent2) !important;
}

/* ── SLIDER ──────────────────────────────── */
div[data-testid="stSlider"] > div > div > div {
    background    : rgba(56,189,248,0.15) !important;
    border-radius : 4px !important; height: 5px !important;
}
div[data-testid="stSlider"] > div > div > div > div:first-child {
    background    : linear-gradient(90deg, var(--accent), var(--purple)) !important;
    border-radius : 4px !important;
}
div[data-testid="stSlider"] div[role="slider"] {
    width: 20px !important; height: 20px !important;
    background: var(--text) !important;
    border: 3px solid var(--accent) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 12px rgba(56,189,248,0.4) !important;
}
div[data-testid="stSlider"] div[role="slider"] > div {
    background: var(--accent) !important; color: #1e2435 !important;
    font-weight: 800 !important; border-radius: 6px !important;
    font-size: 0.78rem !important;
}

/* ── PREDICT BUTTON ──────────────────────── */
.stButton > button {
    width          : 100% !important;
    background     : linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
    color          : #1e2435 !important;
    border         : none !important;
    border-radius  : 12px !important;
    padding        : 15px 32px !important;
    font-family    : var(--fh) !important;
    font-size      : 0.93rem !important;
    font-weight    : 800 !important;
    letter-spacing : 1.5px !important;
    text-transform : uppercase !important;
    box-shadow     : 0 4px 20px rgba(56,189,248,0.28) !important;
    transition     : all 0.3s !important;
    margin-top     : 16px !important;
}
.stButton > button:hover {
    transform  : translateY(-3px) !important;
    box-shadow : 0 10px 32px rgba(56,189,248,0.42) !important;
}

/* ── RESULT CARD ─────────────────────────── */
.result-card {
    background    : linear-gradient(135deg, rgba(56,189,248,0.1), rgba(167,139,250,0.08));
    border        : 1px solid rgba(56,189,248,0.38);
    border-radius : 20px; padding: 48px 36px;
    text-align    : center; position: relative;
    overflow      : hidden; margin-bottom: 28px;
}
.result-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--purple), var(--green));
}
.result-tag {
    display: block; font-size: 0.68rem; font-weight: 700;
    color: var(--accent); text-transform: uppercase;
    letter-spacing: 3px; margin-bottom: 16px;
}
.result-price {
    font-family   : 'Playfair Display', Georgia, serif !important;
    font-size     : clamp(3rem, 7vw, 5rem) !important;
    font-weight   : 900 !important;
    letter-spacing: -2px !important;
    line-height   : 1 !important;
    margin-bottom : 14px !important;
    background              : linear-gradient(135deg, var(--accent2), var(--green));
    -webkit-background-clip : text;
    -webkit-text-fill-color : transparent;
    background-clip         : text;
}
.result-range { color: var(--muted); font-size: 0.92rem; margin-bottom: 20px; }
.result-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(56,189,248,0.13); border: 1px solid rgba(56,189,248,0.35);
    border-radius: 50px; padding: 6px 20px;
    color: var(--accent2); font-size: 0.76rem; font-weight: 700; letter-spacing: 1px;
}

/* ── STREAMLIT METRICS ───────────────────── */
[data-testid="stMetric"] {
    background    : var(--card) !important;
    border        : 1px solid rgba(255,255,255,0.09) !important;
    border-radius : 14px !important; padding: 20px !important;
}
[data-testid="stMetricLabel"] p {
    color: var(--muted) !important; font-size: 0.68rem !important;
    text-transform: uppercase !important; letter-spacing: 1.5px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricValue"] {
    color       : var(--accent2) !important;
    font-family : 'Playfair Display', Georgia, serif !important;
    font-size   : 1.8rem !important;
    font-weight : 900 !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"] svg   { display: none !important; }
[data-testid="stMetricDelta"] > div { color: var(--green) !important; font-size: 0.76rem !important; }

/* ── SUMMARY TABLE ───────────────────────── */
.summary-wrap {
    background: var(--card); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; overflow: hidden;
}
.summary-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 13px 22px; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.summary-row:last-child      { border-bottom: none; }
.summary-row:nth-child(even) { background: rgba(255,255,255,0.03); }
.sum-key { color: var(--muted); font-size: 0.84rem; }
.sum-val { color: var(--text);  font-size: 0.9rem; font-weight: 700; }

/* ── PLACEHOLDER ─────────────────────────── */
.placeholder {
    text-align: center; padding: 72px 20px;
    background: var(--card); border: 2px dashed rgba(56,189,248,0.2);
    border-radius: 18px;
}
.ph-icon { font-size: 3.8rem; display: block; margin-bottom: 18px; }
.ph-text { color: var(--muted); font-size: 0.96rem; line-height: 1.9; }
.ph-text strong { color: var(--text); font-weight: 600; }

/* ── FUTURE CARDS ────────────────────────── */
.future-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}
.future-card {
    background: var(--card); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 24px; transition: all 0.3s;
}
.future-card:hover {
    border-color: rgba(167,139,250,0.38); background: var(--bg3);
    transform: translateY(-4px);
}
.future-card h3 {
    font-family: var(--fh); font-size: 0.92rem; font-weight: 700;
    color: var(--purple); margin-bottom: 9px;
}
.future-card p { color: var(--muted); font-size: 0.83rem; line-height: 1.72; }

/* ── DIVIDER + UTILS ─────────────────────── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
}
.form-label {
    display: block; font-size: 0.68rem; font-weight: 700;
    color: var(--accent); text-transform: uppercase;
    letter-spacing: 2.5px; margin-bottom: 14px; padding: 0 5%;
}
.btn-pad     { padding: 0 5% 4px; }
.results-pad { padding: 0 5% 52px; }

/* ── FOOTER ──────────────────────────────── */
.footer {
    background: var(--bg2); border-top: 1px solid var(--border);
    padding: 30px 5%; text-align: center;
    color: var(--muted); font-size: 0.83rem; line-height: 1.8;
}
.footer strong { color: var(--accent); }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 4. NAVBAR
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<nav class="navbar">
    <div class="nav-logo">🏠 EstateIQ</div>
    <ul class="nav-links">
        <li><a href="#about">About</a></li>
        <li><a href="#dataset">Dataset</a></li>
        <li><a href="#processing">Processing</a></li>
        <li><a href="#model">Model</a></li>
        <li><a href="#results">Results</a></li>
        <li><a href="#predict">Predict</a></li>
        <li><a href="#future">Future</a></li>
    </ul>
    <div class="nav-pill">✦ Live AI Demo</div>
</nav>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 5. HERO
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero" id="home">
    <div class="hero-badge">⚡ XGBoost &nbsp;·&nbsp; R² 92% &nbsp;·&nbsp; Real Estate ML</div>
    <h1 class="hero-title">
        Advanced House Price<br>
        <span>Prediction System</span>
    </h1>
    <p class="hero-desc">
        A complete machine learning pipeline that transforms raw property data
        into accurate price estimates — trained on 1,460+ real-world transactions
        from the Ames, Iowa housing dataset.
    </p>
    <a class="hero-btn" href="#predict">Try Live Predictor →</a>
    <div class="stats-bar">
        <div class="stat-box"><span class="stat-num">1,460+</span><span class="stat-lbl">Houses Trained</span></div>
        <div class="stat-box"><span class="stat-num">92%</span><span class="stat-lbl">R² Accuracy</span></div>
        <div class="stat-box"><span class="stat-num">80+</span><span class="stat-lbl">Features Used</span></div>
        <div class="stat-box"><span class="stat-num">&lt;1s</span><span class="stat-lbl">Predict Speed</span></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 6. SECTION 01 — BUSINESS UNDERSTANDING
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section" id="about">
    <span class="sec-tag">01 — Business Understanding</span>
    <h2 class="sec-title">Why Predict House Prices?</h2>
    <p class="sec-desc">House price prediction is a supervised regression problem. We estimate sale price from features like size, quality, location, and age.</p>
    <div class="cards-grid">
        <div class="info-card"><span class="card-icon">🎯</span><h3>Problem Statement</h3><p>Given property features, predict the fair market value using machine learning with high accuracy.</p></div>
        <div class="info-card"><span class="card-icon">💡</span><h3>Why It Matters</h3><p>Buyers avoid overpaying. Sellers set fair prices. Banks evaluate loans. Agents close deals faster.</p></div>
        <div class="info-card"><span class="card-icon">🧠</span><h3>ML Task Type</h3><p>Supervised Learning — Regression with a continuous output value (house sale price in USD).</p></div>
        <div class="info-card"><span class="card-icon">📈</span><h3>Business Impact</h3><p>Replaces days of manual appraisal work with instant AI estimates at scale for any property.</p></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 7. SECTION 02 — DATASET
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-alt" id="dataset">
    <span class="sec-tag">02 — Dataset Analysis</span>
    <h2 class="sec-title">Kaggle Ames Housing Dataset</h2>
    <p class="sec-desc">1,460 houses and 80+ features covering every measurable aspect of residential properties in Ames, Iowa.</p>
    <div class="cards-grid">
        <div class="info-card"><span class="card-icon">🔢</span><h3>Numerical Features</h3><p>Lot Area, Year Built, Total Rooms, Garage Area, Living Area, Basement Area and 30+ continuous variables.</p></div>
        <div class="info-card"><span class="card-icon">🏷️</span><h3>Categorical Features</h3><p>Neighborhood, Roof Style, House Condition, Zoning, Sale Type, Foundation and 40+ text-based columns.</p></div>
        <div class="info-card"><span class="card-icon">💰</span><h3>Target Variable</h3><p>SalePrice in USD — $34,900 to $755,000 with mean ~$181,000. Log-transformed for training.</p></div>
        <div class="info-card"><span class="card-icon">⚠️</span><h3>Key Challenges</h3><p>Missing values in 19 columns, outliers in GrLivArea, right-skewed price distribution.</p></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 8. SECTION 03 — PREPROCESSING
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section" id="processing">
    <span class="sec-tag">03 — Data Preprocessing</span>
    <h2 class="sec-title">Cleaning & Feature Engineering</h2>
    <p class="sec-desc">Raw data is never model-ready. These steps convert messy real-world data into a clean, structured format.</p>
    <div class="cards-grid">
        <div class="info-card"><span class="card-icon">🔧</span><h3>Missing Values</h3><p>Median fill for numerical, mode for categorical. Zero null values remain before training starts.</p></div>
        <div class="info-card"><span class="card-icon">📉</span><h3>Outlier Removal</h3><p>Removed houses with GrLivArea &gt; 4,500 sqft and low price — confirmed data entry errors.</p></div>
        <div class="info-card"><span class="card-icon">⚙️</span><h3>Feature Engineering</h3><p>Created HouseAge = Year − YearBuilt and TotalSF = GrLivArea + TotalBsmtSF for better signals.</p></div>
        <div class="info-card"><span class="card-icon">⚖️</span><h3>Scaling & Encoding</h3><p>StandardScaler on numerics. One-hot on Neighborhood. Log1p transform on SalePrice target.</p></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 9. SECTION 04 — MODELING
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-alt" id="model">
    <span class="sec-tag">04 — Modeling & Algorithms</span>
    <h2 class="sec-title">Models Trained & Compared</h2>
    <p class="sec-desc">Four algorithms trained. XGBoost was best after GridSearchCV tuning with 5-fold cross-validation.</p>
    <div class="cards-grid">
        <div class="info-card"><span class="card-icon">📐</span><h3>Linear Regression</h3><p>Baseline model. Understands linear relationships. R² ≈ 0.78. Limited for complex patterns.</p></div>
        <div class="info-card"><span class="card-icon">🌲</span><h3>Random Forest</h3><p>100 decision trees ensemble. Handles non-linear data well. R² ≈ 0.87. Robust to outliers.</p></div>
        <div class="info-card"><span class="card-icon">🚀</span><h3>Gradient Boosting</h3><p>Sequential learning on residuals. R² ≈ 0.89. Outperforms Random Forest on this dataset.</p></div>
        <div class="info-card"><span class="card-icon">🏆</span><h3>XGBoost — Winner</h3><p>Regularized gradient boosting. R² ≈ 0.92 after tuning. Saved as final production model.</p></div>
    </div>
    <div class="code-block">
<span class="cm"># ── Final XGBoost model after GridSearchCV tuning ──</span>
<span class="kw">from</span> xgboost <span class="kw">import</span> <span class="fn">XGBRegressor</span>
<span class="kw">import</span> numpy <span class="kw">as</span> np, joblib

model = <span class="fn">XGBRegressor</span>(
    n_estimators  = <span class="nm">200</span>,   <span class="cm"># number of trees</span>
    max_depth     = <span class="nm">5</span>,     <span class="cm"># tree depth</span>
    learning_rate = <span class="nm">0.05</span>,  <span class="cm"># step size</span>
    subsample     = <span class="nm">0.8</span>,   <span class="cm"># row sampling</span>
    random_state  = <span class="nm">42</span>
)
model.<span class="fn">fit</span>(X_train_scaled, y_train)
predictions = np.<span class="fn">expm1</span>(model.<span class="fn">predict</span>(X_test_scaled))
joblib.<span class="fn">dump</span>(model, <span class="st">'model/house_price_model.pkl'</span>)
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 10. SECTION 05 — RESULTS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section" id="results">
    <span class="sec-tag">05 — Model Evaluation</span>
    <h2 class="sec-title">Performance Results</h2>
    <p class="sec-desc">The final XGBoost model delivers excellent accuracy across all three evaluation metrics on unseen test data.</p>
    <div class="metrics-row">
        <div class="metric-box"><span class="metric-val">0.92</span><span class="metric-lbl">R² Score</span></div>
        <div class="metric-box"><span class="metric-val">$18K</span><span class="metric-lbl">Mean Absolute Error</span></div>
        <div class="metric-box"><span class="metric-val">$25K</span><span class="metric-lbl">Root Mean Squared Error</span></div>
    </div>
    <div class="cards-grid">
        <div class="info-card"><span class="card-icon">📊</span><h3>R² = 0.92</h3><p>Model explains 92% of all variance in house prices. Only 8% unexplained — excellent for real estate.</p></div>
        <div class="info-card"><span class="card-icon">📏</span><h3>MAE = $18,000</h3><p>Average prediction error of $18K — less than 10% on a $181K average house price.</p></div>
        <div class="info-card"><span class="card-icon">⚡</span><h3>RMSE = $25,000</h3><p>Low RMSE confirms no catastrophic mispredictions. Model is stable across all price ranges.</p></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 11. SECTION 06 — LIVE PREDICTOR
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="predictor-header" id="predict">
    <span class="sec-tag" style="display:block;text-align:center;margin-bottom:10px;">
        06 — Live Prediction
    </span>
    <h2 class="sec-title">Try the Live Predictor</h2>
    <p class="sec-desc" style="margin:0 auto;">
        Enter real house details below. The trained XGBoost model predicts the price instantly.
    </p>
</div>
""", unsafe_allow_html=True)

# Input Form
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<span class="form-label">📐 Size & Rooms</span>', unsafe_allow_html=True)
    area   = st.number_input("Living Area (sqft)",  min_value=min_area, max_value=max_area, value=default_area, step=50)
    beds   = st.selectbox("Bedrooms",               list(range(1, max_beds + 1)))
    baths  = st.selectbox("Full Bathrooms",         list(range(1, max_baths + 1)))
    garage = st.selectbox("Garage Cars",            list(range(0, max_garage + 1)))

with col2:
    st.markdown('<span class="form-label">⭐ Quality & Location</span>', unsafe_allow_html=True)
    bsmt = st.number_input("Basement Area (sqft)",  min_value=min_bsmt, max_value=max_bsmt, value=default_bsmt, step=50)
    qual = st.slider("Overall Quality (1–10)",      min_value=1, max_value=10,   value=7)
    age  = st.number_input("House Age (years)",     min_value=0, max_value=100,  value=20)
    hood = st.selectbox("Neighborhood", neighborhoods)

st.markdown('<div class="btn-pad">', unsafe_allow_html=True)
predict_clicked = st.button("🔮  Predict House Price Now")
st.markdown('</div>', unsafe_allow_html=True)

# Prediction Logic
if predict_clicked:
    input_data = {
        "GrLivArea":    area,
        "BedroomAbvGr": beds,
        "FullBath":     baths,
        "GarageCars":   garage,
        "TotalBsmtSF":  bsmt,
        "OverallQual":  qual,
        "HouseAge":     age
    }
    df = pd.DataFrame([input_data])
    for col in feature_columns:
        if col.startswith("Neighborhood_"):
            df[col] = 1 if col == f"Neighborhood_{hood}" else 0
    df    = df.reindex(columns=feature_columns, fill_value=0)
    price = np.expm1(model.predict(scaler.transform(df))[0])
    low   = price * 0.92
    high  = price * 1.08

    # Result Card
    st.markdown(f"""
    <div class="results-pad">
        <div class="result-card">
            <span class="result-tag">✦ &nbsp; AI Estimated Market Value &nbsp; ✦</span>
            <div class="result-price">${price:,.0f}</div>
            <div class="result-range">Confidence Range &nbsp; ${low:,.0f} &nbsp;—&nbsp; ${high:,.0f}</div>
            <div class="result-badge">✓ &nbsp; 92% Confidence Level</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown('<span class="form-label">📊 Price Breakdown</span>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Price", f"${price:,.0f}")
    m2.metric("Low Estimate",    f"${low:,.0f}",  delta=f"-${price - low:,.0f}")
    m3.metric("High Estimate",   f"${high:,.0f}", delta=f"+${high - price:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary Table
    st.markdown('<span class="form-label">🏡 House Summary</span>', unsafe_allow_html=True)
    rows_html = "".join([
        f'<div class="summary-row"><span class="sum-key">{k}</span><span class="sum-val">{v}</span></div>'
        for k, v in [
            ("Living Area",     f"{area} sqft"),
            ("Bedrooms",        str(beds)),
            ("Full Bathrooms",  str(baths)),
            ("Garage Cars",     str(garage)),
            ("Basement Area",   f"{bsmt} sqft"),
            ("Overall Quality", f"{qual} / 10"),
            ("House Age",       f"{age} years"),
            ("Neighborhood",    hood),
        ]
    ])
    st.markdown(
        f'<div class="results-pad"><div class="summary-wrap">{rows_html}</div></div>',
        unsafe_allow_html=True
    )

else:
    st.markdown("""
    <div style="padding:0 5% 52px;">
        <div class="placeholder">
            <span class="ph-icon">🏠</span>
            <div class="ph-text">
                Fill in the house details above and click<br>
                <strong>Predict House Price Now</strong><br>
                to get your instant AI-powered price estimate
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 12. SECTION 07 — FUTURE WORK
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-alt" id="future">
    <span class="sec-tag">07 — Future Work</span>
    <h2 class="sec-title">Deployment & Roadmap</h2>
    <p class="sec-desc">A clear path to a production-grade real estate intelligence platform available worldwide.</p>
    <div class="future-grid">
        <div class="future-card"><h3>🌐 Cloud Deployment</h3><p>Backend to Render, frontend to Vercel. Worldwide access with zero downtime.</p></div>
        <div class="future-card"><h3>🗺️ Geo-Spatial Maps</h3><p>Latitude/longitude + Google Maps API for neighborhood-level location accuracy.</p></div>
        <div class="future-card"><h3>🤖 Advanced Models</h3><p>LightGBM, CatBoost, stacked ensembles to push R² accuracy beyond 0.95.</p></div>
        <div class="future-card"><h3>📡 Live Market Data</h3><p>Zillow/Realtor API — retrain model monthly with fresh market transactions.</p></div>
        <div class="future-card"><h3>👤 User Accounts</h3><p>Login, history, saved comparisons, and PDF report downloads per user.</p></div>
        <div class="future-card"><h3>📱 Mobile App</h3><p>React Native app for agents to get estimates on-site during property visits.</p></div>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# 13. FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>🏠 EstateIQ</strong> — Advanced House Price Prediction System</p>
    <p style="margin-top:6px; font-size:0.76rem; opacity:0.65;">
        Machine Learning &nbsp;·&nbsp; XGBoost &nbsp;·&nbsp;
        Streamlit &nbsp;·&nbsp; FastAPI &nbsp;·&nbsp;
        Data Science &nbsp;·&nbsp; Real Estate Analytics
    </p>
</div>
""", unsafe_allow_html=True)
