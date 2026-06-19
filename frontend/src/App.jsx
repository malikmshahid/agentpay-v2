import { useState } from "react";

function App() {
  const [amount, setAmount] = useState("");
  const [toAddress, setToAddress] = useState("");
  const [reason, setReason] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const makePayment = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/pay?amount=${amount}&to_address=${toAddress}&reason=${reason}`,
        { method: "POST" }
      );
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Connection failed" });
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", fontFamily: "Arial", padding: "20px" }}>
      <h1 style={{ color: "#2563eb" }}>🤖 AgentPay</h1>
      <p style={{ color: "#666" }}>AI-Powered USDC Payments on Arc</p>

      <div style={{ background: "#f8fafc", padding: "20px", borderRadius: "10px", marginTop: "20px" }}>
        <h3>Make a Payment</h3>
        <input
          placeholder="Amount (USDC)"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px", borderRadius: "5px", border: "1px solid #ddd" }}
        />
        <input
          placeholder="To Address (0x...)"
          value={toAddress}
          onChange={(e) => setToAddress(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px", borderRadius: "5px", border: "1px solid #ddd" }}
        />
        <input
          placeholder="Reason (e.g. API service payment)"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px", borderRadius: "5px", border: "1px solid #ddd" }}
        />
        <button
          onClick={makePayment}
          disabled={loading}
          style={{ width: "100%", padding: "12px", background: "#2563eb", color: "white", border: "none", borderRadius: "5px", cursor: "pointer", fontSize: "16px" }}
        >
          {loading ? "Processing..." : "⚡ Send USDC Payment"}
        </button>
      </div>

      {result && (
        <div style={{ background: "#f0fdf4", padding: "15px", borderRadius: "10px", marginTop: "20px" }}>
          <h3>✅ Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;