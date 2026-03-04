import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://127.0.0.1:8000/auth/login", form);
      login(res.data.user, res.data.token);
      navigate(res.data.user.role === "admin" ? "/admin" : "/predict");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.header}>
          <div style={styles.icon}>⌂</div>
          <h1 style={styles.title}>Welcome Back</h1>
          <p style={styles.subtitle}>Sign in to your EstateIQ account</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Email Address</label>
            <input
              style={styles.input}
              type="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Password</label>
            <input
              style={styles.input}
              type="password"
              placeholder="Your password"
              value={form.password}
              onChange={e => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>

          {error && <div style={styles.error}>{error}</div>}

          <button type="submit" style={styles.btn} disabled={loading}>
            {loading ? "Signing in..." : "Sign In →"}
          </button>
        </form>

        {/* Demo Accounts */}
        <div style={styles.demoBox}>
          <p style={styles.demoTitle}>Demo Accounts:</p>
          <p style={styles.demoText}>Admin: admin@house.com / admin123</p>
        </div>

        <p style={styles.switchText}>
          Don't have an account? <Link to="/register" style={styles.switchLink}>Sign up free</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh", background: "#080c1e",
    display: "flex", alignItems: "center", justifyContent: "center",
    padding: "20px", fontFamily: "'Segoe UI', sans-serif",
  },
  card: {
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.1)",
    borderRadius: "20px", padding: "40px",
    width: "100%", maxWidth: "420px",
  },
  header: { textAlign: "center", marginBottom: "32px" },
  icon: {
    fontSize: "40px", marginBottom: "12px",
    background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
  },
  title: { fontSize: "26px", fontWeight: "800", color: "#fff", margin: "0 0 8px", fontFamily: "'Georgia', serif" },
  subtitle: { color: "rgba(255,255,255,0.4)", fontSize: "14px", margin: 0 },
  field: { marginBottom: "18px" },
  label: { display: "block", color: "rgba(255,255,255,0.7)", fontSize: "13px", fontWeight: "600", marginBottom: "8px" },
  input: {
    width: "100%", padding: "12px 16px",
    background: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: "10px", color: "#fff", fontSize: "14px",
    boxSizing: "border-box", outline: "none",
  },
  error: {
    background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)",
    borderRadius: "8px", padding: "10px 14px",
    color: "#fca5a5", fontSize: "13px", marginBottom: "16px",
  },
  btn: {
    width: "100%", padding: "13px",
    background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    color: "#fff", border: "none", borderRadius: "10px",
    fontSize: "15px", fontWeight: "700", cursor: "pointer", marginTop: "4px",
  },
  demoBox: {
    marginTop: "20px", padding: "12px 16px",
    background: "rgba(59,130,246,0.08)",
    border: "1px solid rgba(59,130,246,0.2)",
    borderRadius: "10px",
  },
  demoTitle: { color: "#93c5fd", fontSize: "12px", fontWeight: "700", margin: "0 0 4px" },
  demoText: { color: "rgba(255,255,255,0.5)", fontSize: "12px", margin: 0 },
  switchText: { textAlign: "center", color: "rgba(255,255,255,0.4)", fontSize: "14px", marginTop: "20px" },
  switchLink: { color: "#60a5fa", textDecoration: "none", fontWeight: "600" },
};
