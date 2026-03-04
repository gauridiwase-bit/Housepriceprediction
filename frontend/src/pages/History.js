import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function History() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) { navigate("/login"); return; }
    axios.get(`http://127.0.0.1:8000/history/${user.id}`)
      .then(res => setHistory(res.data.history))
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, [user, navigate]);

  const avgPrice = history.length
    ? history.reduce((sum, h) => sum + h.predicted_price, 0) / history.length
    : 0;

  const maxPrice = history.length ? Math.max(...history.map(h => h.predicted_price)) : 0;

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>Prediction History</h1>
          <p style={styles.subtitle}>All your past house price predictions</p>
        </div>

        {/* Stats */}
        <div style={styles.statsGrid}>
          {[
            { label: "Total Predictions", value: history.length, icon: "📊" },
            { label: "Average Price", value: avgPrice ? `$${Math.round(avgPrice).toLocaleString()}` : "—", icon: "💰" },
            { label: "Highest Price", value: maxPrice ? `$${Math.round(maxPrice).toLocaleString()}` : "—", icon: "🏆" },
          ].map((s, i) => (
            <div key={i} style={styles.statCard}>
              <span style={styles.statIcon}>{s.icon}</span>
              <div>
                <p style={styles.statValue}>{s.value}</p>
                <p style={styles.statLabel}>{s.label}</p>
              </div>
            </div>
          ))}
        </div>

        {/* History List */}
        {loading ? (
          <div style={styles.loading}>Loading history...</div>
        ) : history.length === 0 ? (
          <div style={styles.empty}>
            <p style={styles.emptyIcon}>📭</p>
            <p style={styles.emptyText}>No predictions yet</p>
            <button onClick={() => navigate("/predict")} style={styles.emptyBtn}>
              Make Your First Prediction →
            </button>
          </div>
        ) : (
          <div style={styles.list}>
            {history.map((item, i) => (
              <div key={i} style={styles.historyCard}>
                <div style={styles.cardLeft}>
                  <div style={styles.cardIndex}>#{history.length - i}</div>
                  <div>
                    <p style={styles.cardNeighborhood}>{item.neighborhood}</p>
                    <p style={styles.cardDate}>
                      {new Date(item.created_at).toLocaleDateString("en-US", {
                        year: "numeric", month: "short", day: "numeric",
                        hour: "2-digit", minute: "2-digit"
                      })}
                    </p>
                  </div>
                </div>

                <div style={styles.cardDetails}>
                  {[
                    ["Area", `${item.gr_liv_area} sqft`],
                    ["Beds", item.bedroom],
                    ["Baths", item.full_bath],
                    ["Quality", `${item.overall_qual}/10`],
                    ["Age", `${item.house_age}yr`],
                  ].map(([k, v]) => (
                    <div key={k} style={styles.detail}>
                      <span style={styles.detailKey}>{k}</span>
                      <span style={styles.detailVal}>{v}</span>
                    </div>
                  ))}
                </div>

                <div style={styles.cardPrice}>
                  ${Math.round(item.predicted_price).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "#080c1e", color: "#fff", fontFamily: "'Segoe UI', sans-serif", padding: "40px 20px" },
  container: { maxWidth: "900px", margin: "0 auto" },
  header: { marginBottom: "32px" },
  title: { fontSize: "32px", fontWeight: "800", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  subtitle: { color: "rgba(255,255,255,0.4)", fontSize: "15px", margin: 0 },
  statsGrid: { display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginBottom: "32px" },
  statCard: { display: "flex", alignItems: "center", gap: "14px", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "14px", padding: "20px" },
  statIcon: { fontSize: "28px" },
  statValue: { fontSize: "22px", fontWeight: "800", color: "#60a5fa", margin: "0 0 4px" },
  statLabel: { fontSize: "12px", color: "rgba(255,255,255,0.4)", margin: 0 },
  loading: { textAlign: "center", color: "rgba(255,255,255,0.4)", padding: "60px" },
  empty: { textAlign: "center", padding: "60px", background: "rgba(255,255,255,0.04)", border: "2px dashed rgba(255,255,255,0.1)", borderRadius: "16px" },
  emptyIcon: { fontSize: "48px", margin: "0 0 12px" },
  emptyText: { color: "rgba(255,255,255,0.4)", fontSize: "16px", marginBottom: "20px" },
  emptyBtn: { background: "linear-gradient(135deg, #3b82f6, #8b5cf6)", color: "#fff", border: "none", borderRadius: "10px", padding: "12px 24px", fontSize: "14px", fontWeight: "700", cursor: "pointer" },
  list: { display: "flex", flexDirection: "column", gap: "12px" },
  historyCard: { display: "flex", alignItems: "center", gap: "20px", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "14px", padding: "18px 24px" },
  cardLeft: { display: "flex", alignItems: "center", gap: "14px", minWidth: "160px" },
  cardIndex: { width: "36px", height: "36px", background: "rgba(59,130,246,0.15)", border: "1px solid rgba(59,130,246,0.3)", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "#60a5fa", fontSize: "12px", fontWeight: "700", flexShrink: 0 },
  cardNeighborhood: { color: "#fff", fontWeight: "700", fontSize: "14px", margin: "0 0 2px" },
  cardDate: { color: "rgba(255,255,255,0.3)", fontSize: "12px", margin: 0 },
  cardDetails: { display: "flex", gap: "20px", flex: 1 },
  detail: { display: "flex", flexDirection: "column", gap: "2px" },
  detailKey: { color: "rgba(255,255,255,0.3)", fontSize: "11px", textTransform: "uppercase" },
  detailVal: { color: "#fff", fontSize: "13px", fontWeight: "600" },
  cardPrice: { fontSize: "20px", fontWeight: "900", color: "#60a5fa", fontFamily: "'Georgia', serif", flexShrink: 0 },
};
