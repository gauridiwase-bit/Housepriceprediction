import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Admin() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState("overview");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user || user.role !== "admin") { navigate("/"); return; }
    Promise.all([
      axios.get("http://127.0.0.1:8000/admin/stats"),
      axios.get("http://127.0.0.1:8000/admin/users"),
    ]).then(([statsRes, usersRes]) => {
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
    }).finally(() => setLoading(false));
  }, [user, navigate]);

  if (loading) return <div style={styles.loading}>Loading dashboard...</div>;

  const TABS = ["overview", "predictions", "users", "neighborhoods"];

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        {/* Header */}
        <div style={styles.header}>
          <div>
            <h1 style={styles.title}>Admin Dashboard</h1>
            <p style={styles.subtitle}>Welcome back, {user?.name}</p>
          </div>
          <div style={styles.adminBadge}>👑 Administrator</div>
        </div>

        {/* Stat Cards */}
        <div style={styles.statsGrid}>
          {[
            { label: "Total Predictions", value: stats?.total_predictions || 0, icon: "📊", color: "#60a5fa" },
            { label: "Registered Users", value: stats?.total_users || 0, icon: "👥", color: "#a78bfa" },
            { label: "Avg Price", value: stats?.avg_price ? `$${Math.round(stats.avg_price).toLocaleString()}` : "$0", icon: "💰", color: "#34d399" },
            { label: "Max Price", value: stats?.max_price ? `$${Math.round(stats.max_price).toLocaleString()}` : "$0", icon: "🏆", color: "#f472b6" },
          ].map((s, i) => (
            <div key={i} style={styles.statCard}>
              <div style={styles.statTop}>
                <span style={styles.statIcon}>{s.icon}</span>
                <span style={{ ...styles.statValue, color: s.color }}>{s.value}</span>
              </div>
              <p style={styles.statLabel}>{s.label}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div style={styles.tabs}>
          {TABS.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{ ...styles.tab, ...(activeTab === tab ? styles.activeTab : {}) }}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Overview Tab */}
        {activeTab === "overview" && (
          <div>
            <h3 style={styles.sectionTitle}>Recent Predictions</h3>
            <div style={styles.tableCard}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    {["User", "Neighborhood", "Area", "Quality", "Price", "Date"].map(h => (
                      <th key={h} style={styles.th}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {(stats?.recent_predictions || []).map((p, i) => (
                    <tr key={i}>
                      <td style={styles.td}>{p.name || "—"}</td>
                      <td style={styles.td}>{p.neighborhood}</td>
                      <td style={styles.td}>{p.gr_liv_area} sqft</td>
                      <td style={styles.td}>{p.overall_qual}/10</td>
                      <td style={{ ...styles.td, color: "#60a5fa", fontWeight: "700" }}>
                        ${Math.round(p.predicted_price).toLocaleString()}
                      </td>
                      <td style={styles.td}>
                        {new Date(p.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                  {(stats?.recent_predictions || []).length === 0 && (
                    <tr><td colSpan={6} style={{ ...styles.td, textAlign: "center", color: "rgba(255,255,255,0.3)" }}>No predictions yet</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === "users" && (
          <div>
            <h3 style={styles.sectionTitle}>All Users ({users.length})</h3>
            <div style={styles.tableCard}>
              <table style={styles.table}>
                <thead>
                  <tr>
                    {["ID", "Name", "Email", "Role", "Joined"].map(h => (
                      <th key={h} style={styles.th}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {users.map((u, i) => (
                    <tr key={i}>
                      <td style={styles.td}>#{u.id}</td>
                      <td style={styles.td}>{u.name}</td>
                      <td style={styles.td}>{u.email}</td>
                      <td style={styles.td}>
                        <span style={{ ...styles.roleBadge, background: u.role === "admin" ? "rgba(250,204,21,0.15)" : "rgba(59,130,246,0.15)", color: u.role === "admin" ? "#fde68a" : "#93c5fd" }}>
                          {u.role}
                        </span>
                      </td>
                      <td style={styles.td}>{new Date(u.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Neighborhoods Tab */}
        {activeTab === "neighborhoods" && (
          <div>
            <h3 style={styles.sectionTitle}>Neighborhood Analytics</h3>
            <div style={styles.neighborhoodGrid}>
              {(stats?.neighborhood_stats || []).map((n, i) => (
                <div key={i} style={styles.neighborCard}>
                  <p style={styles.neighborName}>{n.neighborhood || "Unknown"}</p>
                  <p style={styles.neighborPrice}>${Math.round(n.avg_price || 0).toLocaleString()}</p>
                  <p style={styles.neighborCount}>{n.count} predictions</p>
                </div>
              ))}
              {(stats?.neighborhood_stats || []).length === 0 && (
                <p style={{ color: "rgba(255,255,255,0.3)" }}>No data yet</p>
              )}
            </div>
          </div>
        )}

        {/* Predictions Tab */}
        {activeTab === "predictions" && (
          <div>
            <h3 style={styles.sectionTitle}>Price Distribution</h3>
            <div style={styles.distributionCard}>
              {[
                { label: "Min Price", value: stats?.min_price, color: "#34d399" },
                { label: "Avg Price", value: stats?.avg_price, color: "#60a5fa" },
                { label: "Max Price", value: stats?.max_price, color: "#f472b6" },
              ].map((item, i) => (
                <div key={i} style={styles.distItem}>
                  <p style={styles.distLabel}>{item.label}</p>
                  <p style={{ ...styles.distValue, color: item.color }}>
                    ${Math.round(item.value || 0).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: { minHeight: "100vh", background: "#080c1e", color: "#fff", fontFamily: "'Segoe UI', sans-serif", padding: "40px 20px" },
  loading: { minHeight: "100vh", background: "#080c1e", color: "rgba(255,255,255,0.4)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "16px" },
  container: { maxWidth: "1100px", margin: "0 auto" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "32px" },
  title: { fontSize: "32px", fontWeight: "800", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  subtitle: { color: "rgba(255,255,255,0.4)", fontSize: "15px", margin: 0 },
  adminBadge: { background: "rgba(250,204,21,0.1)", border: "1px solid rgba(250,204,21,0.25)", borderRadius: "10px", padding: "8px 16px", color: "#fde68a", fontSize: "13px", fontWeight: "700" },
  statsGrid: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "16px", marginBottom: "28px" },
  statCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "14px", padding: "20px" },
  statTop: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" },
  statIcon: { fontSize: "24px" },
  statValue: { fontSize: "24px", fontWeight: "800" },
  statLabel: { color: "rgba(255,255,255,0.4)", fontSize: "12px", margin: 0, textTransform: "uppercase", letterSpacing: "0.5px" },
  tabs: { display: "flex", gap: "4px", marginBottom: "24px", background: "rgba(255,255,255,0.04)", padding: "4px", borderRadius: "10px", width: "fit-content" },
  tab: { padding: "8px 20px", background: "transparent", border: "none", color: "rgba(255,255,255,0.4)", borderRadius: "8px", cursor: "pointer", fontSize: "14px", fontWeight: "500" },
  activeTab: { background: "rgba(255,255,255,0.1)", color: "#fff", fontWeight: "700" },
  sectionTitle: { fontSize: "18px", fontWeight: "700", marginBottom: "16px", color: "rgba(255,255,255,0.8)" },
  tableCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", overflow: "hidden" },
  table: { width: "100%", borderCollapse: "collapse" },
  th: { padding: "14px 16px", background: "rgba(255,255,255,0.04)", color: "rgba(255,255,255,0.5)", fontSize: "12px", fontWeight: "700", textAlign: "left", borderBottom: "1px solid rgba(255,255,255,0.08)", textTransform: "uppercase", letterSpacing: "0.5px" },
  td: { padding: "13px 16px", color: "rgba(255,255,255,0.8)", fontSize: "13px", borderBottom: "1px solid rgba(255,255,255,0.05)" },
  roleBadge: { display: "inline-block", borderRadius: "6px", padding: "3px 10px", fontSize: "12px", fontWeight: "600" },
  neighborhoodGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: "12px" },
  neighborCard: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "12px", padding: "16px", textAlign: "center" },
  neighborName: { color: "#fff", fontWeight: "700", fontSize: "14px", margin: "0 0 8px" },
  neighborPrice: { color: "#60a5fa", fontWeight: "800", fontSize: "18px", margin: "0 0 4px" },
  neighborCount: { color: "rgba(255,255,255,0.3)", fontSize: "12px", margin: 0 },
  distributionCard: { display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" },
  distItem: { background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "16px", padding: "28px", textAlign: "center" },
  distLabel: { color: "rgba(255,255,255,0.4)", fontSize: "13px", marginBottom: "12px", textTransform: "uppercase", letterSpacing: "0.5px" },
  distValue: { fontSize: "32px", fontWeight: "900", margin: 0, fontFamily: "'Georgia', serif" },
};
