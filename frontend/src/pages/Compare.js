import { useState } from "react";
import axios from "axios";

const NEIGHBORHOODS = ["NAmes","CollgCr","OldTown","Edwards","Somerst","NridgHt","Gilbert","Sawyer","NWAmes","SawyerW"];

const emptyHouse = () => ({
  GrLivArea: "", BedroomAbvGr: "", FullBath: "",
  GarageCars: "", TotalBsmtSF: "", OverallQual: "",
  HouseAge: "", Neighborhood: "NAmes"
});

export default function Compare() {
  const [houses, setHouses] = useState([emptyHouse(), emptyHouse()]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const updateHouse = (index, field, value) => {
    const updated = [...houses];
    updated[index] = { ...updated[index], [field]: value };
    setHouses(updated);
  };

  const addHouse = () => {
    if (houses.length < 4) setHouses([...houses, emptyHouse()]);
  };

  const removeHouse = (index) => {
    if (houses.length > 2) setHouses(houses.filter((_, i) => i !== index));
  };

  const handleCompare = async () => {
    setLoading(true);
    setError("");
    try {
      const payload = {
        houses: houses.map(h => ({
          GrLivArea: parseFloat(h.GrLivArea),
          BedroomAbvGr: parseInt(h.BedroomAbvGr),
          FullBath: parseInt(h.FullBath),
          GarageCars: parseInt(h.GarageCars),
          TotalBsmtSF: parseFloat(h.TotalBsmtSF),
          OverallQual: parseInt(h.OverallQual),
          HouseAge: parseInt(h.HouseAge),
          Neighborhood: h.Neighborhood,
        }))
      };
      const res = await axios.post("http://127.0.0.1:8000/compare", payload);
      setResults(res.data.comparisons);
    } catch {
      setError("Comparison failed. Make sure all fields are filled and backend is running.");
    }
    setLoading(false);
  };

  const maxPrice = results ? Math.max(...results.map(r => r.predicted_price)) : 0;
  const COLORS = ["#60a5fa", "#a78bfa", "#f472b6", "#34d399"];

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Compare Houses</h1>
          <p style={styles.subtitle}>Compare up to 4 properties side by side</p>
        </div>

        {/* House Forms */}
        <div style={{ ...styles.grid, gridTemplateColumns: `repeat(${houses.length}, 1fr)` }}>
          {houses.map((house, i) => (
            <div key={i} style={{ ...styles.houseCard, borderColor: COLORS[i] + "40" }}>
              <div style={styles.cardHeader}>
                <span style={{ ...styles.houseLabel, color: COLORS[i] }}>House {i + 1}</span>
                {houses.length > 2 && (
                  <button onClick={() => removeHouse(i)} style={styles.removeBtn}>✕</button>
                )}
              </div>

              {[
                { label: "Area (sqft)", field: "GrLivArea" },
                { label: "Bedrooms", field: "BedroomAbvGr" },
                { label: "Bathrooms", field: "FullBath" },
                { label: "Garage Cars", field: "GarageCars" },
                { label: "Basement (sqft)", field: "TotalBsmtSF" },
                { label: "Quality (1-10)", field: "OverallQual" },
                { label: "House Age", field: "HouseAge" },
              ].map(({ label, field }) => (
                <div key={field} style={styles.field}>
                  <label style={styles.label}>{label}</label>
                  <input
                    style={styles.input}
                    type="number"
                    value={house[field]}
                    onChange={e => updateHouse(i, field, e.target.value)}
                    placeholder="0"
                  />
                </div>
              ))}

              <div style={styles.field}>
                <label style={styles.label}>Neighborhood</label>
                <select style={styles.input} value={house.Neighborhood}
                  onChange={e => updateHouse(i, "Neighborhood", e.target.value)}>
                  {NEIGHBORHOODS.map(n => <option key={n} value={n}>{n}</option>)}
                </select>
              </div>
            </div>
          ))}
        </div>

        {/* Buttons */}
        <div style={styles.btnRow}>
          {houses.length < 4 && (
            <button onClick={addHouse} style={styles.addBtn}>+ Add House</button>
          )}
          <button onClick={handleCompare} style={styles.compareBtn} disabled={loading}>
            {loading ? "⏳ Comparing..." : "⚖️ Compare Now"}
          </button>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        {/* Results */}
        {results && (
          <div style={styles.resultsSection}>
            <h2 style={styles.resultsTitle}>Comparison Results</h2>

            {/* Bar Chart */}
            <div style={styles.chartCard}>
              <p style={styles.chartTitle}>Price Comparison</p>
              <div style={styles.barChart}>
                {results.map((r, i) => {
                  const pct = (r.predicted_price / maxPrice) * 100;
                  return (
                    <div key={i} style={styles.barGroup}>
                      <span style={styles.barPrice}>{r.formatted_price}</span>
                      <div style={styles.barTrack}>
                        <div style={{ ...styles.barFill, width: `${pct}%`, background: COLORS[i] }} />
                      </div>
                      <span style={{ ...styles.barName, color: COLORS[i] }}>House {i + 1}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Winner */}
            <div style={styles.winnerCard}>
              <span style={styles.winnerCrown}>👑</span>
              <div>
                <p style={styles.winnerTitle}>Best Value</p>
                <p style={styles.winnerDesc}>
                  House {results.indexOf(results.find(r => r.predicted_price === maxPrice)) + 1} has the highest estimated value at{" "}
                  <strong style={{ color: "#60a5fa" }}>
                    {results.find(r => r.predicted_price === maxPrice)?.formatted_price}
                  </strong>
                </p>
              </div>
            </div>

            {/* Stats Table */}
            <div style={styles.tableCard}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Feature</th>
                    {results.map((_, i) => (
                      <th key={i} style={{ ...styles.th, color: COLORS[i] }}>House {i + 1}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    ["Predicted Price", r => r.formatted_price],
                    ["Living Area", r => `${r.details.GrLivArea} sqft`],
                    ["Bedrooms", r => r.details.BedroomAbvGr],
                    ["Bathrooms", r => r.details.FullBath],
                    ["Quality", r => `${r.details.OverallQual}/10`],
                    ["House Age", r => `${r.details.HouseAge} yrs`],
                    ["Neighborhood", r => r.details.Neighborhood],
                  ].map(([label, getter]) => (
                    <tr key={label}>
                      <td style={styles.tdLabel}>{label}</td>
                      {results.map((r, i) => (
                        <td key={i} style={styles.td}>{getter(r)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "#080c1e", color: "#fff", fontFamily: "'Segoe UI', sans-serif", padding: "40px 20px" },
  container: { maxWidth: "1200px", margin: "0 auto" },
  header: { marginBottom: "32px" },
  title: { fontSize: "32px", fontWeight: "800", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  subtitle: { color: "rgba(255,255,255,0.4)", fontSize: "15px", margin: 0 },
  grid: { display: "grid", gap: "16px", marginBottom: "20px" },
  houseCard: { background: "rgba(255,255,255,0.04)", border: "1px solid", borderRadius: "16px", padding: "20px" },
  cardHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" },
  houseLabel: { fontSize: "16px", fontWeight: "800" },
  removeBtn: { background: "rgba(239,68,68,0.15)", border: "none", color: "#fca5a5", borderRadius: "6px", padding: "4px 8px", cursor: "pointer", fontSize: "12px" },
  field: { marginBottom: "12px" },
  label: { display: "block", color: "rgba(255,255,255,0.5)", fontSize: "11px", fontWeight: "600", marginBottom: "4px", textTransform: "uppercase" },
  input: { width: "100%", padding: "8px 12px", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: "8px", color: "#fff", fontSize: "13px", boxSizing: "border-box", outline: "none" },
  btnRow: { display: "flex", gap: "12px", marginBottom: "20px" },
  addBtn: { padding: "12px 24px", background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.15)", color: "#fff", borderRadius: "10px", cursor: "pointer", fontSize: "14px", fontWeight: "600" },
  compareBtn: { padding: "12px 32px", background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", color: "#fff", border: "none", borderRadius: "10px", cursor: "pointer", fontSize: "15px", fontWeight: "700" },
  error: { background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: "8px", padding: "12px", color: "#fca5a5", fontSize: "13px", marginBottom: "20px" },
  resultsSection: {},
  resultsTitle: { fontSize: "24px", fontWeight: "800", marginBottom: "20px", fontFamily: "'Georgia', serif" },
  chartCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", padding: "24px", marginBottom: "16px" },
  chartTitle: { color: "rgba(255,255,255,0.7)", fontSize: "13px", fontWeight: "600", margin: "0 0 20px", textTransform: "uppercase", letterSpacing: "0.5px" },
  barChart: { display: "flex", flexDirection: "column", gap: "12px" },
  barGroup: { display: "flex", alignItems: "center", gap: "12px" },
  barPrice: { width: "100px", color: "#fff", fontSize: "13px", fontWeight: "700", textAlign: "right" },
  barTrack: { flex: 1, background: "rgba(255,255,255,0.06)", borderRadius: "6px", height: "28px", overflow: "hidden" },
  barFill: { height: "100%", borderRadius: "6px", transition: "width 0.8s ease" },
  barName: { width: "60px", fontSize: "13px", fontWeight: "600" },
  winnerCard: { display: "flex", alignItems: "center", gap: "16px", background: "rgba(250,204,21,0.08)", border: "1px solid rgba(250,204,21,0.2)", borderRadius: "16px", padding: "20px", marginBottom: "16px" },
  winnerCrown: { fontSize: "32px" },
  winnerTitle: { color: "#fde68a", fontWeight: "700", margin: "0 0 4px" },
  winnerDesc: { color: "rgba(255,255,255,0.6)", fontSize: "14px", margin: 0 },
  tableCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", overflow: "hidden" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { padding: "14px 16px", background: "rgba(255,255,255,0.04)", fontSize: "13px", fontWeight: "700", textAlign: "left", borderBottom: "1px solid rgba(255,255,255,0.08)" },
  tdLabel: { padding: "12px 16px", color: "rgba(255,255,255,0.5)", fontSize: "13px", borderBottom: "1px solid rgba(255,255,255,0.05)", fontWeight: "600" },
  td: { padding: "12px 16px", color: "#fff", fontSize: "13px", borderBottom: "1px solid rgba(255,255,255,0.05)" },
};
