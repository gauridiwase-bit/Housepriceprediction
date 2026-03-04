# ════════════════════════════════════════════════════════════════
#  EstateIQ — House Price Prediction API
#  FastAPI Backend | Custom Swagger UI Styling
# ════════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import joblib, json, numpy as np, pandas as pd
import sqlite3, hashlib, datetime
from typing import Optional

# ─────────────────────────────────────────────────────────────────
# 1. APP SETUP WITH CUSTOM DOCS
# ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "EstateIQ — House Price API",
    description = "AI-powered house price prediction using XGBoost. R² = 92%.",
    version     = "1.0.0",
    docs_url    = None,   # disable default — we use custom below
    redoc_url   = None,
)

# ─────────────────────────────────────────────────────────────────
# 2. CORS — allow Streamlit frontend to connect
# ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ─────────────────────────────────────────────────────────────────
# 3. LOAD MODEL
# ─────────────────────────────────────────────────────────────────
model  = joblib.load(r'C:\MyProject\model\house_price_model.pkl')
scaler = joblib.load(r'C:\MyProject\model\scaler.pkl')
with open(r'C:\MyProject\model\feature_columns.json') as f:
    feature_columns = json.load(f)

# ─────────────────────────────────────────────────────────────────
# 4. DATABASE SETUP
# ─────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(r'C:\MyProject\database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role     TEXT DEFAULT 'user',
            created  TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            input_data TEXT,
            price      REAL,
            created    TEXT
        )
    """)
    # Default admin
    try:
        conn.execute("""
            INSERT INTO users (email, password, role, created)
            VALUES (?, ?, ?, ?)
        """, (
            'admin@estatiq.com',
            hashlib.sha256('admin123'.encode()).hexdigest(),
            'admin',
            str(datetime.datetime.now())
        ))
    except:
        pass
    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────────────────────────
# 5. SCHEMAS
# ─────────────────────────────────────────────────────────────────
class PredictInput(BaseModel):
    GrLivArea    : float
    BedroomAbvGr : int
    FullBath     : int
    GarageCars   : int
    TotalBsmtSF  : float
    OverallQual  : int
    HouseAge     : int
    Neighborhood : str

class RegisterInput(BaseModel):
    email    : str
    password : str

class LoginInput(BaseModel):
    email    : str
    password : str

# ─────────────────────────────────────────────────────────────────
# 6. CUSTOM SWAGGER UI — EstateIQ Dark Theme
# ─────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap');

/* ── BASE ─────────────────────────────── */
body {
    background : #f0f4ff !important;
    color      : #1e2435 !important;
    font-family: 'Inter', sans-serif !important;
    margin     : 0 !important;
}

/* ── TOPBAR ───────────────────────────── */
.swagger-ui .topbar {
    background    : #f0f4ff !important;
    border-bottom : 2px solid rgba(56,189,248,0.35) !important;
    padding       : 12px 24px !important;
}
.swagger-ui .topbar-wrapper img { display: none !important; }
.swagger-ui .topbar-wrapper::before {
    content     : '🏠 EstateIQ API';
    font-family : 'Playfair Display', Georgia, serif !important;
    font-size   : 1.5rem !important;
    font-weight : 900 !important;
    color       : #1a6eb5 !important;
    letter-spacing: -0.5px;
}
.swagger-ui .topbar-wrapper a { text-decoration: none !important; }
.swagger-ui .topbar .download-url-wrapper input[type=text] {
    background    : #dce3f5 !important;
    border        : 1px solid rgba(56,189,248,0.35) !important;
    border-radius : 8px !important;
    color         : #1e2435 !important;
    font-family   : 'Inter', sans-serif !important;
    padding       : 8px 14px !important;
}

/* ── TITLE ────────────────────────────── */
.swagger-ui .info hgroup.main h2.title {
    font-family : 'Playfair Display', Georgia, serif !important;
    font-size   : 2.2rem !important;
    font-weight : 900 !important;
    color       : #1e2435 !important;
    letter-spacing: -1px !important;
}
.swagger-ui .info .description p,
.swagger-ui .info p {
    color      : #4a5568 !important;
    font-family: 'Inter', sans-serif !important;
    font-size  : 0.95rem !important;
    line-height: 1.7 !important;
}
.swagger-ui .info a {
    color: #38bdf8 !important;
}

/* ── VERSION BADGE ────────────────────── */
.swagger-ui .info .version {
    background    : rgba(56,189,248,0.15) !important;
    border        : 1px solid rgba(56,189,248,0.35) !important;
    border-radius : 20px !important;
    padding       : 3px 12px !important;
    color         : #38bdf8 !important;
    font-family   : 'Inter', sans-serif !important;
    font-weight   : 700 !important;
    font-size     : 0.8rem !important;
}

/* ── MAIN WRAPPER ─────────────────────── */
.swagger-ui .wrapper { background: #f0f4ff !important; max-width: 1100px !important; }
.swagger-ui { background: #f0f4ff !important; }

/* ── SECTION HEADERS ──────────────────── */
.swagger-ui .opblock-tag {
    font-family   : 'Playfair Display', Georgia, serif !important;
    font-size     : 1.3rem !important;
    font-weight   : 800 !important;
    color         : #1e2435 !important;
    border-bottom : 1px solid rgba(56,189,248,0.3) !important;
    padding       : 12px 0 !important;
    margin-bottom : 12px !important;
}
.swagger-ui .opblock-tag:hover { background: transparent !important; }

/* ── ENDPOINT BLOCKS ──────────────────── */
.swagger-ui .opblock {
    background    : #e2e8f8 !important;
    border        : 1px solid rgba(56,189,248,0.25) !important;
    border-radius : 12px !important;
    margin-bottom : 10px !important;
    box-shadow    : 0 4px 16px rgba(0,0,0,0.2) !important;
}
.swagger-ui .opblock:hover {
    border-color: rgba(56,189,248,0.35) !important;
}

/* GET method */
.swagger-ui .opblock.opblock-get {
    border-left: 4px solid #38bdf8 !important;
    background : rgba(56,189,248,0.06) !important;
}
.swagger-ui .opblock.opblock-get .opblock-summary-method {
    background    : #38bdf8 !important;
    color         : #f0f4ff !important;
    border-radius : 8px !important;
    font-weight   : 800 !important;
    font-family   : 'Inter', sans-serif !important;
    font-size     : 0.78rem !important;
    padding       : 6px 14px !important;
}

/* POST method */
.swagger-ui .opblock.opblock-post {
    border-left: 4px solid #34d399 !important;
    background : rgba(52,211,153,0.06) !important;
}
.swagger-ui .opblock.opblock-post .opblock-summary-method {
    background    : #34d399 !important;
    color         : #f0f4ff !important;
    border-radius : 8px !important;
    font-weight   : 800 !important;
    font-family   : 'Inter', sans-serif !important;
    font-size     : 0.78rem !important;
    padding       : 6px 14px !important;
}

/* ── ENDPOINT PATH TEXT ───────────────── */
.swagger-ui .opblock-summary-path {
    font-family: 'Inter', sans-serif !important;
    font-size  : 0.95rem !important;
    font-weight: 600 !important;
    color      : #1e2435 !important;
}
.swagger-ui .opblock-summary-description {
    color      : #4a5568 !important;
    font-family: 'Inter', sans-serif !important;
    font-size  : 0.85rem !important;
}
.swagger-ui .opblock-summary {
    background    : transparent !important;
    border-radius : 10px !important;
    padding       : 12px 16px !important;
}
.swagger-ui .opblock-summary:hover { background: rgba(255,255,255,0.03) !important; }

/* ── EXPANDED CONTENT ─────────────────── */
.swagger-ui .opblock-body,
.swagger-ui .opblock-section,
.swagger-ui .opblock-description-wrapper {
    background : #dce3f5 !important;
    color      : #1e2435 !important;
    font-family: 'Inter', sans-serif !important;
}
.swagger-ui .opblock-section-header {
    background : #dce3f5 !important;
    color      : #4a5568 !important;
    font-family: 'Inter', sans-serif !important;
}
.swagger-ui .opblock-section-header h4 {
    color: #38bdf8 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* ── TRY IT OUT BUTTON ────────────────── */
.swagger-ui .btn.try-out__btn {
    background    : rgba(56,189,248,0.15) !important;
    border        : 1px solid rgba(56,189,248,0.35) !important;
    border-radius : 8px !important;
    color         : #38bdf8 !important;
    font-family   : 'Inter', sans-serif !important;
    font-weight   : 700 !important;
    font-size     : 0.8rem !important;
    padding       : 6px 16px !important;
    transition    : all 0.2s !important;
}
.swagger-ui .btn.try-out__btn:hover {
    background: rgba(56,189,248,0.25) !important;
}

/* ── EXECUTE BUTTON ───────────────────── */
.swagger-ui .btn.execute {
    background    : linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
    border        : none !important;
    border-radius : 8px !important;
    color         : #f0f4ff !important;
    font-family   : 'Inter', sans-serif !important;
    font-weight   : 800 !important;
    font-size     : 0.85rem !important;
    padding       : 8px 24px !important;
    letter-spacing: 0.5px !important;
}
.swagger-ui .btn.execute:hover { opacity: 0.9 !important; }

/* ── INPUTS / TEXTAREA ────────────────── */
.swagger-ui textarea,
.swagger-ui input[type=text],
.swagger-ui input[type=email],
.swagger-ui input[type=password] {
    background    : #dce3f5 !important;
    border        : 1.5px solid rgba(56,189,248,0.35) !important;
    border-radius : 8px !important;
    color         : #1e2435 !important;
    font-family   : 'Inter', sans-serif !important;
    font-size     : 0.9rem !important;
    padding       : 8px 12px !important;
}
.swagger-ui textarea:focus,
.swagger-ui input:focus {
    border-color: #38bdf8 !important;
    outline     : none !important;
    box-shadow  : 0 0 0 3px rgba(56,189,248,0.12) !important;
}

/* ── RESPONSE SECTION ─────────────────── */
.swagger-ui .responses-wrapper,
.swagger-ui .response-col_description {
    background : #f0f4ff !important;
    color      : #1e2435 !important;
    font-family: 'Inter', sans-serif !important;
}
.swagger-ui .response-col_status {
    color      : #34d399 !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
}
.swagger-ui table thead tr th {
    color         : #4a5568 !important;
    font-size     : 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    font-family   : 'Inter', sans-serif !important;
    border-bottom : 1px solid rgba(56,189,248,0.25) !important;
}
.swagger-ui table tbody tr td {
    color      : #1e2435 !important;
    font-family: 'Inter', sans-serif !important;
    border-bottom: 1px solid rgba(56,189,248,0.2) !important;
}

/* ── CODE / JSON RESPONSE ─────────────── */
.swagger-ui .highlight-code,
.swagger-ui .microlight {
    background    : #d8e0f2 !important;
    border        : 1px solid rgba(56,189,248,0.25) !important;
    border-radius : 10px !important;
    padding       : 16px !important;
    font-size     : 0.83rem !important;
    line-height   : 1.7 !important;
}
.swagger-ui .response-col_description__inner div.markdown p {
    color: #4a5568 !important;
}

/* ── SCHEMA SECTION ───────────────────── */
.swagger-ui section.models {
    background    : #e2e8f8 !important;
    border        : 1px solid rgba(56,189,248,0.25) !important;
    border-radius : 12px !important;
    padding       : 16px !important;
}
.swagger-ui section.models h4 {
    font-family: 'Playfair Display', Georgia, serif !important;
    font-size  : 1.1rem !important;
    font-weight: 800 !important;
    color      : #1e2435 !important;
}
.swagger-ui .model-title {
    font-family: 'Inter', sans-serif !important;
    color      : #38bdf8 !important;
    font-weight: 700 !important;
}
.swagger-ui .model {
    color      : #4a5568 !important;
    font-family: 'Inter', sans-serif !important;
    font-size  : 0.85rem !important;
}

/* ── SCROLLBAR ────────────────────────── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0f4ff; }
::-webkit-scrollbar-thumb { background: rgba(56,189,248,0.35); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

/* ── AUTHORIZE BUTTON ─────────────────── */
.swagger-ui .btn.authorize {
    background    : rgba(56,189,248,0.12) !important;
    border        : 1px solid rgba(56,189,248,0.35) !important;
    border-radius : 8px !important;
    color         : #38bdf8 !important;
    font-family   : 'Inter', sans-serif !important;
    font-weight   : 700 !important;
}

/* ── CLEAR BUTTON ─────────────────────── */
.swagger-ui .btn-clear {
    color      : #e05555 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
}

/* ── SELECT / DROPDOWN ────────────────── */
.swagger-ui select {
    background    : #dce3f5 !important;
    border        : 1px solid rgba(56,189,248,0.35) !important;
    border-radius : 8px !important;
    color         : #1e2435 !important;
    font-family   : 'Inter', sans-serif !important;
}
"""

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return HTMLResponse(f"""
<!DOCTYPE html>
<html>
<head>
    <title>EstateIQ — House Price API</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css"
        href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
    <link rel="icon" type="image/png" href="https://fastapi.tiangolo.com/img/favicon.png"/>
    <style>{CUSTOM_CSS}</style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
    SwaggerUIBundle({{
        url        : '/openapi.json',
        dom_id     : '#swagger-ui',
        presets    : [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
        layout     : "BaseLayout",
        deepLinking: true,
    }})
</script>
</body>
</html>
""")

# ─────────────────────────────────────────────────────────────────
# 7. ROUTES
# ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["Home"])
def home():
    return {
        "app"    : "EstateIQ — House Price Prediction API",
        "version": "1.0.0",
        "status" : "running",
        "docs"   : "http://localhost:8000/docs"
    }

@app.post("/auth/register", tags=["Auth"])
def register(data: RegisterInput):
    conn = get_db()
    try:
        hashed = hashlib.sha256(data.password.encode()).hexdigest()
        conn.execute(
            "INSERT INTO users (email, password, role, created) VALUES (?,?,?,?)",
            (data.email, hashed, 'user', str(datetime.datetime.now()))
        )
        conn.commit()
        return {"message": "User registered successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

@app.post("/auth/login", tags=["Auth"])
def login(data: LoginInput):
    conn = get_db()
    hashed = hashlib.sha256(data.password.encode()).hexdigest()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data.email, hashed)
    ).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {
        "message" : "Login successful",
        "user_id" : user["id"],
        "email"   : user["email"],
        "role"    : user["role"]
    }

@app.post("/predict", tags=["Prediction"])
def predict(data: PredictInput):
    inp = {
        "GrLivArea"   : data.GrLivArea,
        "BedroomAbvGr": data.BedroomAbvGr,
        "FullBath"    : data.FullBath,
        "GarageCars"  : data.GarageCars,
        "TotalBsmtSF" : data.TotalBsmtSF,
        "OverallQual" : data.OverallQual,
        "HouseAge"    : data.HouseAge,
    }
    df = pd.DataFrame([inp])
    for col in feature_columns:
        if col.startswith("Neighborhood_"):
            df[col] = 1 if col == f"Neighborhood_{data.Neighborhood}" else 0
    df    = df.reindex(columns=feature_columns, fill_value=0)
    price = float(np.expm1(model.predict(scaler.transform(df))[0]))
    return {
        "predicted_price"  : round(price, 2),
        "low_estimate"     : round(price * 0.92, 2),
        "high_estimate"    : round(price * 1.08, 2),
        "confidence"       : "92%",
        "neighborhood"     : data.Neighborhood,
    }

@app.get("/history/{user_id}", tags=["History"])
def history(user_id: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM predictions WHERE user_id=? ORDER BY created DESC LIMIT 20",
        (user_id,)
    ).fetchall()
    conn.close()
    return {"history": [dict(r) for r in rows]}

@app.get("/admin/stats", tags=["Admin"])
def admin_stats():
    conn = get_db()
    total_users       = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_predictions = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    conn.close()
    return {
        "total_users"      : total_users,
        "total_predictions": total_predictions,
        "model_accuracy"   : "92%",
        "status"           : "running"
    }

@app.get("/admin/users", tags=["Admin"])
def admin_users():
    conn = get_db()
    users = conn.execute("SELECT id, email, role, created FROM users").fetchall()
    conn.close()
    return {"users": [dict(u) for u in users]}
