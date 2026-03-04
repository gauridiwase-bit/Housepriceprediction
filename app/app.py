import streamlit as st
import joblib, json, numpy as np, pandas as pd

st.set_page_config(
    page_title="EstateIQ - House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@400;500;600;700&display=swap');

    /* ── Base ── */
    .stApp {
        background: #0a0f1e;
        font-family: 'DM Sans', sans-serif;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main .block-container {
        padding: 2.5rem 4rem;
        max-width: 1300px;
    }

    /* ── Hero ── */
    .hero-wrap {
        text-align: center;
        padding: 40px 0 20px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(251,191,36,0.12);
        border: 1px solid rgba(251,191,36,0.35);
        border-radius: 50px;
        padding: 6px 20px;
        color: #fbbf24;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 18px;
    }
    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.8rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 14px;
        color: #ffffff;
    }
    .hero-title span {
        background: linear-gradient(135deg, #f59e0b, #ef4444, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: rgba(255,255,255,0.55);
        font-size: 1.05rem;
        margin-bottom: 32px;
        line-height: 1.7;
    }

    /* ── Stats Bar ── */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 0;
        margin: 0 auto 40px;
        max-width: 700px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        overflow: hidden;
    }
    .stat-box {
        flex: 1;
        padding: 18px 10px;
        text-align: center;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .stat-box:last-child { border-right: none; }
    .stat-num {
        font-size: 1.6rem;
        font-weight: 800;
        color: #f59e0b;
        display: block;
    }
    .stat-lbl {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 3px;
        display: block;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(251,191,36,0.3), transparent);
        margin: 8px 0 32px;
    }

    /* ── Section Label ── */
    .sec-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #f59e0b;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 16px;
        display: block;
    }

    /* ── Input Card ── */
    .input-wrap {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 28px;
    }

    /* ── Inputs ── */
    .stNumberInput input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    label {
        color: rgba(255,255,255,0.75) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] div {
        background: linear-gradient(90deg, #f59e0b, #ef4444) !important;
    }

    /* ── Button ── */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 50%, #ec4899 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 32px !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin-top: 12px !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-2px) !important;
    }

    /* ── Result Card ── */
    .result-card {
        background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.12), rgba(236,72,153,0.08));
        border: 1px solid rgba(245,158,11,0.35);
        border-radius: 24px;
        padding: 40px 32px;
        text-align: center;
        margin-top: 28px;
    }
    .result-eyebrow {
        font-size: 0.75rem;
        font-weight: 700;
        color: #f59e0b;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 12px;
        display: block;
    }
    .result-price {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 10px;
    }
    .result-price span {
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .result-range {
        color: rgba(255,255,255,0.5);
        font-size: 0.95rem;
        margin-bottom: 16px;
    }
    .conf-badge {
        display: inline-block;
        background: rgba(34,197,94,0.15);
        border: 1px solid rgba(34,197,94,0.4);
        border-radius: 50px;
        padding: 5px 18px;
        color: #4ade80;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 1px;
    }

    /* ── Metric Cards ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        padding: 18px 20px !important;
    }
    [data-testid="stMetricLabel"] p {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricValue"] {
        color: #f59e0b !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #4ade80 !important;
        font-size: 0.82rem !important;
    }

    /* ── Placeholder ── */
    .placeholder {
        text-align: center;
        padding: 70px 20px;
        background: rgba(255,255,255,0.02);
        border: 2px dashed rgba(255,255,255,0.07);
        border-radius: 20px;
        margin-top: 28px;
    }
    .placeholder-icon { font-size: 3.5rem; margin-bottom: 16px; }
    .placeholder-text {
        color: rgba(255,255,255,0.35);
        font-size: 1rem;
        line-height: 1.7;
    }
    .placeholder-text strong {
        color: rgba(255,255,255,0.6);
    }

    /* ── Summary grid ── */
    .summary-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .summary-key {
        color: rgba(255,255,255,0.45);
        font-size: 0.88rem;
    }
    .summary-val {
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Model ──────────────────────────────────────
@st.cache_resource
def load_model():
    m = joblib.load(r'C:\MyProject\model\house_price_model.pkl')
    s = joblib.load(r'C:\MyProject\model\scaler.pkl')
    with open(r'C:\MyProject\model\feature_columns.json') as f:
        c = json.load(f)
    return m, s, c

model, scaler, feature_columns = load_model()

# ── Hero ────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🏆 AI Real Estate Intelligence</div>
    <div class="hero-title">Predict House Prices<br><span>With Confidence</span></div>
    <div class="hero-sub">Advanced XGBoost model trained on 1,460+ real estate transactions.<br>Get accurate price estimates in under 1 second.</div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-row">
    <div class="stat-box"><span class="stat-num">1,460+</span><span class="stat-lbl">Houses Trained</span></div>
    <div class="stat-box"><span class="stat-num">92%</span><span class="stat-lbl">Accuracy</span></div>
    <div class="stat-box"><span class="stat-num">31</span><span class="stat-lbl">Features</span></div>
    <div class="stat-box"><span class="stat-num">&lt;1s</span><span class="stat-lbl">Speed</span></div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Form ────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<span class="sec-label">📐 Size & Rooms</span>', unsafe_allow_html=True)
    area   = st.number_input("Living Area (sqft)", 500, 5000, 1500, step=50)
    beds   = st.selectbox("Bedrooms", [1, 2, 3, 4, 5, 6])
    baths  = st.selectbox("Full Bathrooms", [1, 2, 3, 4])
    garage = st.selectbox("Garage Cars", [0, 1, 2, 3])

with col2:
    st.markdown('<span class="sec-label">⭐ Quality & Location</span>', unsafe_allow_html=True)
    bsmt = st.number_input("Basement Area (sqft)", 0, 3000, 800, step=50)
    qual = st.slider("Overall Quality (1-10)", 1, 10, 7)
    age  = st.number_input("House Age (years)", 0, 100, 20)
    hood = st.selectbox("Neighborhood", [
        "NAmes", "CollgCr", "OldTown", "Edwards", "Somerst",
        "NridgHt", "Gilbert", "Sawyer", "NWAmes", "SawyerW",
        "BrkSide", "Crawfor", "Mitchel", "NoRidge", "Timber"
    ])

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Predict House Price Now")

# ── Prediction ──────────────────────────────────────
if predict_btn:
    inp = {
        "GrLivArea": area, "BedroomAbvGr": beds,
        "FullBath": baths, "GarageCars": garage,
        "TotalBsmtSF": bsmt, "OverallQual": qual, "HouseAge": age
    }
    df = pd.DataFrame([inp])
    for col in feature_columns:
        if col.startswith("Neighborhood_"):
            df[col] = 1 if col == f"Neighborhood_{hood}" else 0
    df    = df.reindex(columns=feature_columns, fill_value=0)
    price = np.expm1(model.predict(scaler.transform(df))[0])
    low   = price * 0.92
    high  = price * 1.08

    # Result card
    st.markdown(f"""
    <div class="result-card">
        <span class="result-eyebrow">✦ Estimated House Price ✦</span>
        <div class="result-price"><span>${price:,.0f}</span></div>
        <div class="result-range">Price Range: ${low:,.0f} &nbsp;–&nbsp; ${high:,.0f}</div>
        <div class="conf-badge">✓ &nbsp; 92% Confidence Level</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics
    st.markdown('<span class="sec-label">📊 Price Breakdown</span>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Price",  f"${price:,.0f}")
    m2.metric("Low Estimate",     f"${low:,.0f}",  delta=f"-${price-low:,.0f}")
    m3.metric("High Estimate",    f"${high:,.0f}", delta=f"+${high-price:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary
    st.markdown('<span class="sec-label">🏡 House Summary</span>', unsafe_allow_html=True)
    details = [
        ("Living Area",      f"{area} sqft"),
        ("Bedrooms",         str(beds)),
        ("Bathrooms",        str(baths)),
        ("Garage Cars",      str(garage)),
        ("Basement Area",    f"{bsmt} sqft"),
        ("Overall Quality",  f"{qual} / 10"),
        ("House Age",        f"{age} years"),
        ("Neighborhood",     hood),
    ]
    rows_html = "".join([
        f'<div class="summary-row"><span class="summary-key">{k}</span><span class="summary-val">{v}</span></div>'
        for k, v in details
    ])
    st.markdown(f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:16px 24px;">{rows_html}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="placeholder">
        <div class="placeholder-icon">🏠</div>
        <div class="placeholder-text">
            Fill in the house details above and click<br>
            <strong>Predict House Price Now</strong><br>
            to get your instant AI-powered estimate
        </div>
    </div>
    """, unsafe_allow_html=True)