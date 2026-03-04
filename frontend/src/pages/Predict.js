import { useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const NEIGHBORHOODS = [
  "NAmes", "CollgCr", "OldTown", "Edwards", "Somerst",
  "NridgHt", "Gilbert", "Sawyer", "NWAmes", "SawyerW",
  "BrkSide", "Crawfor", "Mitchel", "NoRidge", "Timber"
];

const FIELDS = [
  { label: "Living Area (sqft)", name: "GrLivArea", placeholder: "e.g. 1500", type: "number" },
  { label: "Bedrooms", name: "BedroomAbvGr", placeholder: "e.g. 3", type: "number" },
  { label: "Bathrooms", name: "FullBath", placeholder: "e.g. 2", type: "number" },
  { label: "Garage Cars", name: "GarageCars", placeholder: "e.g. 2", type: "number" },
  { label: "Basement Area (sqft)", name: "TotalBsmtSF", placeholder: "e.g. 800", type: "number" },
  { label: "Overall Quality (1-10)", name: "OverallQual", placeholder: "e.g. 7", type: "number" },
  { label: "House Age (years)", name: "HouseAge", placeholder: "e.g. 20", type: "number" },
];

export default function Predict() {
  const { user } = useAuth();
  const [form, setForm] = useState({
    GrLivArea: "", BedroomAbvGr: "", FullBath: "",
    GarageCars: "", TotalBsmtSF: "", OverallQual: "",
    HouseAge: "", Neighborhood: "NAmes"
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", {
        GrLivArea: parseFloat(form.GrLivArea),
        BedroomAbvGr: parseInt(form.BedroomAbvGr),
        FullBath: parseInt(form.FullBath),
        GarageCars: parseInt(form.GarageCars),
        TotalBsmtSF: parseFloat(form.TotalBsmtSF),
        OverallQual: parseInt(form.OverallQual),
        HouseAge: parseInt(form.HouseAge),
        Neighborhood: form.Neighborhood,
        user_id: user?.id || null
      });
      setResult(res.data);
    } catch {
      setError("Prediction failed. Make sure the backend is running.");
    }
    setLoading(false);
  };

  const downloadPDF = () => {
    if (!result) return;
    const content = `
ESTATEIQ - HOUSE PRICE PREDICTION REPORT
==========================================
Generated: ${new Date().toLocaleString()}
User: ${user?.name || "Guest"}

HOUSE DETAILS
------------------------------------------
Living Area:       ${form.GrLivArea} sqft
Bedrooms:          ${form.BedroomAbvGr}
Bathrooms:         ${form.FullBath}
Garage Cars:       ${form.GarageCars}
Basement Area:     ${form.TotalBsmtSF} sqft
Overall Quality:   ${form.OverallQual}/10
House Age:         ${form.HouseAge} years
Neighborhood:      ${form.Neighborhood}

PREDICTION RESULTS
------------------------------------------
Estimated Price:   ${result.formatted_price}
Price Range:       ${result.price_range.low} - ${result.price_range.high}
Confidence:        ${result.confidence}

==========================================
Powered by EstateIQ - AI Real Estate Intelligence
    `;
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `house_price_report_${Date.now()}.txt`;
    a.click();
  };

  // Price bar chart data
  const qualityPrices = [80000, 100000, 130000, 155000, 180000, 210000, 245000, 290000, 350000, 430000];
  const currentQual = parseInt(form.OverallQual) || 5;

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Price Predictor</h1>
          <p style={styles.subtitle}>Enter house details to get an AI-powered price estimate</p>
        </div>

        <div style={styles.layout}>
          {/* Form */}
          <div style={styles.formCard}>
            <form onSubmit={handleSubmit}>
              <div style={styles.grid}>
                {FIELDS.map(({ label, name, placeholder }) => (
                  <div key={name} style={styles.field}>
                    <label style={styles.label}>{label}</label>
                    <input
                      style={styles.input}
                      type="number"
                      placeholder={placeholder}
                      value={form[name]}
                      onChange={e => setForm({ ...form, [name]: e.target.value })}
                      required
                    />
                  </div>
                ))}
                <div style={styles.field}>
                  <label style={styles.label}>Neighborhood</label>
                  <select
                    style={styles.input}
                    value={form.Neighborhood}
                    onChange={e => setForm({ ...form, Neighborhood: e.target.value })}
                  >
                    {NEIGHBORHOODS.map(n => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
              </div>

              {error && <div style={styles.error}>{error}</div>}

              <button type="submit" style={styles.btn} disabled={loading}>
                {loading ? "⏳ Calculating..." : "🔮 Predict Price"}
              </button>
            </form>
          </div>

          {/* Results Panel */}
          <div style={styles.resultsPanel}>
            {!result ? (
              <div style={styles.placeholder}>
                <div style={styles.placeholderIcon}>🏠</div>
                <p style={styles.placeholderText}>Fill in the form and click Predict Price to see results</p>
              </div>
            ) : (
              <div>
                {/* Price Result */}
                <div style={styles.priceCard}>
                  <p style={styles.priceLabel}>Estimated Price</p>
                  <p style={styles.priceValue}>{result.formatted_price}</p>
                  <p style={styles.priceRange}>
                    Range: {result.price_range.low} – {result.price_range.high}
                  </p>
                  <div style={styles.confidenceBadge}>
                    ✓ {result.confidence} Confidence
                  </div>
                </div>

                {/* Quality vs Price Chart */}
                <div style={styles.chartCard}>
                  <p style={styles.chartTitle}>Quality vs Price</p>
                  <div style={styles.barChart}>
                    {qualityPrices.map((price, i) => {
                      const qual = i + 1;
                      const maxPrice = Math.max(...qualityPrices);
                      const height = (price / maxPrice) * 100;
                      const isActive = qual === currentQual;
                      return (
                        <div key={qual} style={styles.barWrapper}>
                          <div style={{
                            ...styles.bar,
                            height: `${height}%`,
                            background: isActive
                              ? "linear-gradient(180deg, #60a5fa, #3b82f6)"
                              : "rgba(255,255,255,0.1)",
                            border: isActive ? "1px solid #60a5fa" : "none",
                          }} />
                          <span style={{ ...styles.barLabel, color: isActive ? "#60a5fa" : "rgba(255,255,255,0.3)" }}>
                            {qual}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  <p style={styles.chartNote}>Quality rating (1-10) vs estimated price</p>
                </div>

                {/* Details Summary */}
                <div style={styles.summaryCard}>
                  <p style={styles.summaryTitle}>House Summary</p>
                  {[
                    ["Area", `${form.GrLivArea} sqft`],
                    ["Bedrooms", form.BedroomAbvGr],
                    ["Bathrooms", form.FullBath],
                    ["Garage", `${form.GarageCars} cars`],
                    ["Quality", `${form.OverallQual}/10`],
                    ["Age", `${form.HouseAge} years`],
                    ["Neighborhood", form.Neighborhood],
                  ].map(([k, v]) => (
                    <div key={k} style={styles.summaryRow}>
                      <span style={styles.summaryKey}>{k}</span>
                      <span style={styles.summaryVal}>{v}</span>
                    </div>
                  ))}
                </div>

                {/* Download PDF */}
                <button onClick={downloadPDF} style={styles.pdfBtn}>
                  📄 Download Report
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "#080c1e", color: "#fff", fontFamily: "'Segoe UI', sans-serif", padding: "40px 20px" },
  container: { maxWidth: "1100px", margin: "0 auto" },
  header: { marginBottom: "32px" },
  title: { fontSize: "32px", fontWeight: "800", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  subtitle: { color: "rgba(255,255,255,0.4)", fontSize: "15px", margin: 0 },
  layout: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" },
  formCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", padding: "28px" },
  grid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "20px" },
  field: {},
  label: { display: "block", color: "rgba(255,255,255,0.6)", fontSize: "12px", fontWeight: "600", marginBottom: "6px", textTransform: "uppercase", letterSpacing: "0.5px" },
  input: { width: "100%", padding: "10px 14px", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px", color: "#fff", fontSize: "14px", boxSizing: "border-box", outline: "none" },
  error: { background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: "8px", padding: "10px", color: "#fca5a5", fontSize: "13px", marginBottom: "16px" },
  btn: { width: "100%", padding: "13px", background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", color: "#fff", border: "none", borderRadius: "10px", fontSize: "15px", fontWeight: "700", cursor: "pointer" },
  resultsPanel: {},
  placeholder: { background: "rgba(255,255,255,0.04)", border: "2px dashed rgba(255,255,255,0.1)", borderRadius: "16px", padding: "60px 20px", textAlign: "center" },
  placeholderIcon: { fontSize: "48px", marginBottom: "16px" },
  placeholderText: { color: "rgba(255,255,255,0.3)", fontSize: "14px" },
  priceCard: { background: "linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15))", border: "1px solid rgba(59,130,246,0.3)", borderRadius: "16px", padding: "24px", textAlign: "center", marginBottom: "16px" },
  priceLabel: { color: "rgba(255,255,255,0.5)", fontSize: "13px", margin: "0 0 8px" },
  priceValue: { fontSize: "44px", fontWeight: "900", color: "#60a5fa", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  priceRange: { color: "rgba(255,255,255,0.4)", fontSize: "13px", margin: "0 0 12px" },
  confidenceBadge: { display: "inline-block", background: "rgba(34,197,94,0.15)", border: "1px solid rgba(34,197,94,0.3)", borderRadius: "50px", padding: "4px 14px", color: "#86efac", fontSize: "12px", fontWeight: "600" },
  chartCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", padding: "20px", marginBottom: "16px" },
  chartTitle: { color: "rgba(255,255,255,0.7)", fontSize: "13px", fontWeight: "600", margin: "0 0 16px", textTransform: "uppercase", letterSpacing: "0.5px" },
  barChart: { display: "flex", alignItems: "flex-end", gap: "6px", height: "80px", marginBottom: "8px" },
  barWrapper: { flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "flex-end", height: "100%" },
  bar: { width: "100%", borderRadius: "4px 4px 0 0", transition: "all 0.3s", minHeight: "4px" },
  barLabel: { fontSize: "10px", marginTop: "4px" },
  chartNote: { color: "rgba(255,255,255,0.3)", fontSize: "11px", margin: 0, textAlign: "center" },
  summaryCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", padding: "20px", marginBottom: "16px" },
  summaryTitle: { color: "rgba(255,255,255,0.7)", fontSize: "13px", fontWeight: "600", margin: "0 0 14px", textTransform: "uppercase", letterSpacing: "0.5px" },
  summaryRow: { display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: "1px solid rgba(255,255,255,0.05)" },
  summaryKey: { color: "rgba(255,255,255,0.4)", fontSize: "13px" },
  summaryVal: { color: "#fff", fontSize: "13px", fontWeight: "600" },
  pdfBtn: { width: "100%", padding: "12px", background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.12)", color: "#fff", borderRadius: "10px", fontSize: "14px", fontWeight: "600", cursor: "pointer" },
};
