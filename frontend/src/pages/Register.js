import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirm) {
      setError("Passwords do not match!");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("http://127.0.0.1:8000/auth/register", {
        name: form.name, email: form.email, password: form.password
      });
      login(res.data.user, res.data.token);
      navigate("/predict");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    }
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.header}>
          <div style={styles.icon}>⌂</div>
          <h1 style={styles.title}>Create Account</h1>
          <p style={styles.subtitle}>Start predicting house prices for free</p>
        </div>

        <form onSubmit={handleSubmit}>
          {[
            { label: "Full Name", key: "name", type: "text", placeholder: "John Smith" },
            { label: "Email Address", key: "email", type: "email", placeholder: "you@example.com" },
            { label: "Password", key: "password", type: "password", placeholder: "Min 6 characters" },
            { label: "Confirm Password", key: "confirm", type: "password", placeholder: "Repeat password" },
          ].map(({ label, key, type, placeholder }) => (
            <div key={key} style={styles.field}>
              <label style={styles.label}>{label}</label>
              <input
                style={styles.input}
                type={type}
                placeholder={placeholder}
                value={form[key]}
                onChange={e => setForm({ ...form, [key]: e.target.value })}
                required
              />
            </div>
          ))}

          {error && <div style={styles.error}>{error}</div>}

          <button type="submit" style={styles.btn} disabled={loading}>
            {loading ? "Creating account..." : "Create Account →"}
          </button>
        </form>

        <p style={styles.switchText}>
          Already have an account? <Link to="/login" style={styles.switchLink}>Sign in</Link>
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
  field: { marginBottom: "16px" },
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
  switchText: { textAlign: "center", color: "rgba(255,255,255,0.4)", fontSize: "14px", marginTop: "20px" },
  switchLink: { color: "#60a5fa", textDecoration: "none", fontWeight: "600" },
};
