import { useState } from "react";

function AnalyzerPage({ problem, onDone }) {

  const [code, setCode] = useState("");
  const [feedback, setFeedback] = useState([]);
  const [accuracy, setAccuracy] = useState(null);
  const [error, setError] = useState("");

  const analyze = async () => {

    // 🔥 FRONTEND VALIDATION (prevents request)
    if (!code.trim()) {
      setError("Please enter code before analyzing.");
      return;
    }

    setError("");
    setFeedback([]);
    setAccuracy(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code })
      });

      const data = await res.json();

      // 🔥 CRITICAL FIX (prevents crash)
      if (!res.ok || data.error) {
        setError(data.error || "Invalid input");
        return;
      }

      setFeedback(data.feedback || []);
      setAccuracy(data.accuracy ?? null);

    } catch (err) {
      console.error(err);
      setError("Server error");
    }
  };

  return (
    <div className="analyzer-page">

      <h2>{problem.name}</h2>

      <textarea
        placeholder="Paste your code here"
        value={code}
        onChange={(e)=>setCode(e.target.value)}
      />

      <button onClick={analyze}>Analyze</button>

      {/* 🔥 ERROR DISPLAY */}
      {error && <p style={{color: "red"}}>{error}</p>}

      {/* 🔥 SAFE RENDER */}
      {feedback && feedback.length > 0 &&
        feedback.map((f,i)=><p key={i}>{f}</p>)
      }

      {accuracy !== null && (
        <h3>Accuracy: {(accuracy*100).toFixed(1)}%</h3>
      )}

      {/* 🔥 SAFE DONE BUTTON */}
      <button
        disabled={accuracy === null}
        onClick={() => {
          if (accuracy === null) return;
          onDone(accuracy);
        }}
      >
        Done
      </button>

    </div>
  );
}

export default AnalyzerPage;