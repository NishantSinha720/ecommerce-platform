import React, { useEffect, useState } from "react";
import {
  BrowserRouter, Routes, Route, Navigate, Link, useNavigate, useLocation
} from "react-router-dom";
import api from "./services/api";

function Login() {
  const navigate = useNavigate();
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        await api.post("/api/auth/register/", {username, email, password});
        setMode("login");
        setError("Account created. Please login.");
      } else {
        const r = await api.post("/api/auth/login/", {username, password});
        localStorage.setItem("access_token", r.data.access);
        localStorage.setItem("username", username);
        navigate("/dashboard", {replace: true});
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        Object.values(err.response?.data || {}).flat().join(" ") ||
        "Authentication failed."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={submit}>
        <h1>E-Commerce Platform</h1>
        <p>Order & Inventory Management System</p>
        <h2>{mode === "login" ? "Login" : "Create account"}</h2>

        <label>Username</label>
        <input value={username} onChange={e => setUsername(e.target.value)} required />

        {mode === "register" && <>
          <label>Email</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </>}

        <label>Password</label>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />

        {error && <div className="error">{error}</div>}

        <button disabled={loading}>
          {loading ? "Please wait..." : mode === "login" ? "Login" : "Register"}
        </button>

        <button
          type="button"
          className="secondary"
          onClick={() => {setMode(mode === "login" ? "register" : "login"); setError("");}}
        >
          {mode === "login" ? "Create a new account" : "Back to login"}
        </button>

        <small>Demo account: admin / Admin123!</small>
      </form>
    </div>
  );
}

function Protected({children}) {
  return localStorage.getItem("access_token")
    ? children
    : <Navigate to="/login" replace />;
}

function Layout({children}) {
  const navigate = useNavigate();
  const location = useLocation();
  const [health, setHealth] = useState("Checking");

  useEffect(() => {
    api.get("/api/v1/status/").then(() => setHealth("Online")).catch(() => setHealth("Offline"));
  }, []);

  function logout() {
    localStorage.clear();
    navigate("/login", {replace: true});
  }

  return (
    <>
      <header className="topbar">
        <strong>E-Commerce Platform</strong>
        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/products">Products</Link>
          <Link to="/inventory">Inventory</Link>
          <Link to="/orders">Orders</Link>
          <Link to="/analytics">Analytics</Link>
          <Link to="/ai">AI</Link>
        </nav>
        <span className="health">API {health}</span>
        <button onClick={logout}>Logout</button>
      </header>
      <main className="container">{children}</main>
    </>
  );
}

function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { api.get("/api/analytics/summary/").then(r => setData(r.data)); }, []);
  return <section>
    <h1>Dashboard</h1>
    <div className="grid">
      {[
        ["Products", data?.products ?? "—"],
        ["Orders", data?.orders ?? "—"],
        ["Revenue", data ? `₹ ${data.revenue.toLocaleString()}` : "—"],
        ["Stock Units", data?.stock_units ?? "—"],
        ["Low Stock", data?.low_stock ?? "—"]
      ].map(([k,v]) => <div className="card" key={k}><span>{k}</span><b>{v}</b></div>)}
    </div>
    <div className="card">
      <h2>Platform</h2>
      <p>Django + DRF + MySQL + Redis + Celery + FastAPI + React + optional Ollama RAG</p>
    </div>
  </section>;
}

function Products() {
  const [products, setProducts] = useState([]);
  useEffect(() => { api.get("/api/products/").then(r => setProducts(r.data.results || r.data)); }, []);
  return <section><h1>Products</h1><div className="card"><table><thead><tr><th>ID</th><th>Name</th><th>SKU</th><th>Price</th><th>Status</th></tr></thead><tbody>
    {products.map(p => <tr key={p.id}><td>{p.id}</td><td>{p.name}</td><td>{p.sku}</td><td>₹ {Number(p.price).toLocaleString()}</td><td>{p.is_active ? "Active" : "Inactive"}</td></tr>)}
  </tbody></table></div></section>;
}

function Inventory() {
  const [stock, setStock] = useState([]);
  useEffect(() => { api.get("/api/inventory/stock/").then(r => setStock(r.data.results || r.data)); }, []);
  return <section><h1>Inventory</h1><div className="card"><table><thead><tr><th>Product</th><th>Warehouse</th><th>Quantity</th><th>Reserved</th><th>Available</th></tr></thead><tbody>
    {stock.map(s => <tr key={s.id}><td>{s.product_name}</td><td>{s.warehouse_name}</td><td>{s.quantity}</td><td>{s.reserved_quantity}</td><td>{s.available_quantity}</td></tr>)}
  </tbody></table></div></section>;
}

function Orders() {
  const [orders, setOrders] = useState([]);
  const load = () => api.get("/api/orders/orders/").then(r => setOrders(r.data.results || r.data));
  useEffect(load, []);
  return <section><h1>Orders</h1><div className="card"><table><thead><tr><th>ID</th><th>Status</th><th>Total</th><th>Created</th></tr></thead><tbody>
    {orders.map(o => <tr key={o.id}><td>{o.id}</td><td>{o.status}</td><td>₹ {Number(o.total_amount).toLocaleString()}</td><td>{new Date(o.created_at).toLocaleString()}</td></tr>)}
  </tbody></table>{!orders.length && <p>No orders yet.</p>}</div></section>;
}

function Analytics() {
  const [summary, setSummary] = useState(null);
  const [forecast, setForecast] = useState(null);
  useEffect(() => {
    api.get("/api/analytics/summary/").then(r => setSummary(r.data));
    api.get("/api/analytics/forecast/").then(r => setForecast(r.data));
  }, []);
  return <section><h1>Analytics</h1><div className="grid">
    <div className="card"><span>Revenue</span><b>₹ {summary ? Number(summary.revenue).toLocaleString() : "—"}</b></div>
    <div className="card"><span>Orders</span><b>{summary?.orders ?? "—"}</b></div>
    <div className="card"><span>Next Forecast</span><b>{forecast?.forecast_next ?? "—"}</b></div>
  </div></section>;
}

function AI() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [status, setStatus] = useState(null);

  useEffect(() => { api.get("/api/v1/ai/status").then(r => setStatus(r.data)); }, []);

  async function ask() {
    const r = await api.post("/api/v1/ai/ask", {question});
    setAnswer(r.data);
  }

  return <section><h1>AI Assistant</h1>
    <div className="card"><p>AI status: <b>{status?.status || "Checking..."}</b></p>
      <textarea placeholder="Ask about products or inventory..." value={question} onChange={e => setQuestion(e.target.value)} />
      <button onClick={ask} disabled={!question.trim()}>Ask AI</button>
      {answer && <div className="answer"><b>{answer.provider}</b><p>{answer.answer}</p></div>}
    </div>
  </section>;
}

export default function App() {
  return <BrowserRouter><Routes>
    <Route path="/login" element={<Login />} />
    <Route path="/" element={<Navigate to="/login" replace />} />
    <Route path="/dashboard" element={<Protected><Layout><Dashboard /></Layout></Protected>} />
    <Route path="/products" element={<Protected><Layout><Products /></Layout></Protected>} />
    <Route path="/inventory" element={<Protected><Layout><Inventory /></Layout></Protected>} />
    <Route path="/orders" element={<Protected><Layout><Orders /></Layout></Protected>} />
    <Route path="/analytics" element={<Protected><Layout><Analytics /></Layout></Protected>} />
    <Route path="/ai" element={<Protected><Layout><AI /></Layout></Protected>} />
    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes></BrowserRouter>;
}
