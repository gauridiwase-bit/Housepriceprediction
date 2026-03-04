import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const features = [
    { icon: "🧠", title: "AI-Powered", desc: "XGBoost model trained on 1,460+ real house sales with 92% accuracy" },
    { icon: "⚡", title: "Instant Results", desc: "Get price predictions in milliseconds, not days" },
    { icon: "📊", title: "Visual Analytics", desc: "Charts and comparisons to understand your property value" },
    { icon: "📋", title: "PDF Reports", desc: "Download professional reports to share with clients" },
    { icon: "🔍", title: "Compare Houses", desc: "Compare multiple properties side by side" },
    { icon: "📈", title: "Price History", desc: "Track all your past predictions in one place" },
  ];

  const stats = [
    { number: "1,460+", label: "Houses Trained On" },
    { number: "92%", label: "Model Accuracy" },
    { number: "31", label: "Features Analyzed" },
    { number: "<1s", label: "Prediction Time" },
  ];

  return (
    <div style={styles.page}>
      {/* Hero Section */}
      <section style={styles.hero}>
        <div style={styles.heroBadge}>🏆 AI-Powered Real Estate Intelligence</div>
        <h1 style={styles.heroTitle}>
          Predict House Prices<br />
          <span style={styles.heroAccent}>With Confidence</span>
        </h1>
        <p style={styles.heroSubtitle}>
          Advanced machine learning model trained on thousands of real estate transactions.
          Get accurate price predictions instantly.
        </p>
        <div style={styles.heroButtons}>
          <button
            onClick={() => navigate(user ? "/predict" : "/register")}
            style={styles.primaryBtn}
          >
            {user ? "Start Predicting →" : "Get Started Free →"}
          </button>
          {!user && (
            <button onClick={() => navigate("/login")} style={styles.secondaryBtn}>
              Sign In
            </button>
          )}
        </div>

        {/* Stats Bar */}
        <div style={styles.statsBar}>
          {stats.map((stat, i) => (
            <div key={i} style={styles.stat}>
              <div style={styles.statNumber}>{stat.number}</div>
              <div style={styles.statLabel}>{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section style={styles.featuresSection}>
        <h2 style={styles.sectionTitle}>Everything You Need</h2>
        <p style={styles.sectionSubtitle}>Professional tools for real estate price analysis</p>
        <div style={styles.featuresGrid}>
          {features.map((f, i) => (
            <div key={i} style={styles.featureCard}>
              <div style={styles.featureIcon}>{f.icon}</div>
              <h3 style={styles.featureTitle}>{f.title}</h3>
              <p style={styles.featureDesc}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section style={styles.ctaSection}>
        <h2 style={styles.ctaTitle}>Ready to Get Started?</h2>
        <p style={styles.ctaSubtitle}>Join and start predicting house prices instantly</p>
        <button
          onClick={() => navigate(user ? "/predict" : "/register")}
          style={styles.ctaBtn}
        >
          {user ? "Go to Predictor →" : "Create Free Account →"}
        </button>
      </section>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#080c1e",
    color: "#fff",
    fontFamily: "'Segoe UI', sans-serif",
  },
  hero: {
    textAlign: "center",
    padding: "100px 40px 80px",
    background: "radial-gradient(ellipse 80% 60% at 50% 0%, rgba(59,130,246,0.15), transparent)",
  },
  heroBadge: {
    display: "inline-block",
    background: "rgba(59,130,246,0.15)",
    border: "1px solid rgba(59,130,246,0.3)",
    borderRadius: "50px",
    padding: "6px 20px",
    fontSize: "13px",
    color: "#93c5fd",
    marginBottom: "24px",
  },
  heroTitle: {
    fontSize: "clamp(40px, 6vw, 72px)",
    fontWeight: "900",
    lineHeight: 1.1,
    letterSpacing: "-2px",
    margin: "0 0 20px",
    fontFamily: "'Georgia', serif",
  },
  heroAccent: {
    background: "linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  heroSubtitle: {
    fontSize: "18px",
    color: "rgba(255,255,255,0.5)",
    maxWidth: "520px",
    margin: "0 auto 36px",
    lineHeight: 1.7,
  },
  heroButtons: { display: "flex", gap: "12px", justifyContent: "center", marginBottom: "60px" },
  primaryBtn: {
    background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    color: "#fff", border: "none", borderRadius: "12px",
    padding: "14px 32px", fontSize: "16px", fontWeight: "700",
    cursor: "pointer",
  },
  secondaryBtn: {
    background: "rgba(255,255,255,0.07)",
    color: "#fff", border: "1px solid rgba(255,255,255,0.15)",
    borderRadius: "12px", padding: "14px 32px",
    fontSize: "16px", cursor: "pointer",
  },
  statsBar: {
    display: "flex", justifyContent: "center", gap: "60px",
    flexWrap: "wrap",
  },
  stat: { textAlign: "center" },
  statNumber: {
    fontSize: "32px", fontWeight: "800",
    background: "linear-gradient(135deg, #60a5fa, #a78bfa)",
    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
  },
  statLabel: { fontSize: "13px", color: "rgba(255,255,255,0.4)", marginTop: "4px" },
  featuresSection: {
    padding: "80px 40px",
    maxWidth: "1100px", margin: "0 auto",
  },
  sectionTitle: {
    fontSize: "36px", fontWeight: "800", textAlign: "center",
    letterSpacing: "-1px", marginBottom: "12px",
    fontFamily: "'Georgia', serif",
  },
  sectionSubtitle: {
    textAlign: "center", color: "rgba(255,255,255,0.4)",
    fontSize: "16px", marginBottom: "48px",
  },
  featuresGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "20px",
  },
  featureCard: {
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px", padding: "28px",
  },
  featureIcon: { fontSize: "32px", marginBottom: "14px" },
  featureTitle: { fontSize: "18px", fontWeight: "700", marginBottom: "8px" },
  featureDesc: { fontSize: "14px", color: "rgba(255,255,255,0.5)", lineHeight: 1.6 },
  ctaSection: {
    textAlign: "center", padding: "80px 40px",
    background: "linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1))",
    borderTop: "1px solid rgba(255,255,255,0.06)",
  },
  ctaTitle: { fontSize: "36px", fontWeight: "800", marginBottom: "12px", fontFamily: "'Georgia', serif" },
  ctaSubtitle: { color: "rgba(255,255,255,0.5)", fontSize: "16px", marginBottom: "32px" },
  ctaBtn: {
    background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    color: "#fff", border: "none", borderRadius: "12px",
    padding: "16px 40px", fontSize: "17px", fontWeight: "700",
    cursor: "pointer",
  },
};
