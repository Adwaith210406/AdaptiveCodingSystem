import { useState } from "react";
import "./App.css";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";
import { FaUser, FaLock } from "react-icons/fa";

function App() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({ username: "", password: "" });

  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");

  const [code, setCode] = useState("");
  const [feedback, setFeedback] = useState([]);

  const [stats, setStats] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);

  const [view, setView] = useState("none");

  // 🔐 AUTH
  const handleAuth = async (type) => {
    try {
      const res = await fetch(`http://127.0.0.1:5000/${type}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      const data = await res.json();

      if (type === "login" && data.user_id) {
        setUser({
          id: data.user_id,
          username: data.username
        });
        setMessage("");
      } else {
        setMessage(data.message || data.error || "Something went wrong");
      }
    } catch (err) {
      console.error(err);
      setMessage("Server error");
    }
  };

  // 🎯 RECOMMEND
  const getRecommendation = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id })
      });

      const data = await res.json();
      setResult(data);
      setView("problems");
    } catch (err) {
      console.error(err);
    }
  };

  // 📊 FETCH STATS + LEADERBOARD
  const fetchStats = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/leaderboard");
      const data = await res.json();

      console.log("Leaderboard:", data);

      if (!data || data.length === 0) {
        setLeaderboard([]);
        setStats([]);
        return;
      }

      setLeaderboard(data);

      setStats(
        data.map((u) => ({
          user: u.username,
          accuracy: Number((u.accuracy * 100).toFixed(1))
        }))
      );

    } catch (err) {
      console.error("Error fetching stats:", err);
    }
  };

  // ✅ SUBMIT
  const handleSubmit = async (p) => {
    try {
      await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          problem_id: p.contestId + p.index,
          difficulty: result.difficulty,
          correct: 1,
          time_taken: 100
        })
      });

      // 🔥 Update UI instantly
      getRecommendation();
      fetchStats();

    } catch (err) {
      console.error(err);
    }
  };

  // 💻 ANALYZE
  const analyzeCode = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      });

      const data = await res.json();
      setFeedback(data.feedback);
    } catch (err) {
      console.error(err);
    }
  };

  // 🔐 LOGIN PAGE
  if (!user) {
    return (
      <div className="auth">
        <div className="auth-card">
          <h1 className="title">Adaptive Coding</h1>

          <div className="input-group">
            <FaUser className="icon" />
            <input
              placeholder=" "
              onChange={(e) =>
                setForm({ ...form, username: e.target.value })
              }
            />
            <label>Username</label>
          </div>

          <div className="input-group">
            <FaLock className="icon" />
            <input
              type="password"
              placeholder=" "
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
            />
            <label>Password</label>
          </div>

          <div className="auth-buttons">
            <button onClick={() => handleAuth("login")}>Login</button>
            <button onClick={() => handleAuth("signup")}>Sign Up</button>
          </div>

          <p>{message}</p>
        </div>
      </div>
    );
  }

  // 🔥 DASHBOARD
  return (
    <div className="dashboard">

      <h1 className="main-title">🚀 Adaptive Coding System</h1>
      <h2 className="welcome">👋 Welcome {user.username}</h2>

      <button className="primary" onClick={getRecommendation}>
        Get Recommendation
      </button>

      <div className="button-row">
        <button onClick={() => { fetchStats(); setView("chart"); }}>
          Show Chart
        </button>

        <button onClick={() => { fetchStats(); setView("leaderboard"); }}>
          Show Leaderboard
        </button>
      </div>

      {/* 🔥 DYNAMIC SECTION */}
      <div className="card">

        {/* PROBLEMS */}
        {view === "problems" && result?.problems && (
          <>
            <h3>🎯 {result.difficulty.toUpperCase()} Problems</h3>

            {result.problems.map((p, i) => (
              <div key={i} className="problem">
                <a
                  href={`https://codeforces.com/problemset/problem/${p.contestId}/${p.index}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  {p.name} ({p.rating})
                </a>

                <button onClick={() => handleSubmit(p)}>
                  Solve
                </button>
              </div>
            ))}
          </>
        )}

        {/* 📊 CHART */}
        {view === "chart" && (
          <>
            <h3>📊 Performance</h3>

            {stats.length === 0 ? (
              <p>No data yet. Solve problems first.</p>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats}>
                  <XAxis
                    dataKey="user"
                    interval={0}
                    angle={-20}
                    textAnchor="end"
                  />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="accuracy" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </>
        )}

        {/* 🏆 LEADERBOARD */}
        {view === "leaderboard" && (
          <>
            <h3>🏆 Leaderboard</h3>

            {leaderboard.length === 0 ? (
              <p>No leaderboard data yet.</p>
            ) : (
              leaderboard.map((u, i) => (
                <div key={i} className="leader-item">
                  <div className="rank">#{i + 1}</div>
                  <div className="name">{u.username}</div>
                  <div className="score">
                    {(u.accuracy * 100).toFixed(1)}%
                  </div>
                </div>
              ))
            )}
          </>
        )}

      </div>

      {/* 💻 ANALYZER */}
      <div className="card">
        <h3>💻 Code Analyzer</h3>

        <textarea
          placeholder="Paste code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <button onClick={analyzeCode}>Analyze</button>

        <div className="feedback">
          {feedback.map((f, i) => (
            <p key={i}>{f}</p>
          ))}
        </div>
      </div>

      <button className="logout" onClick={() => setUser(null)}>
        Logout
      </button>

    </div>
  );
}

export default App;