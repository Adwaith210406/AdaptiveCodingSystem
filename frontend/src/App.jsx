import { useState } from "react";
import "./App.css";
import { FaUser, FaLock } from "react-icons/fa";
import AnalyzerPage from "./AnalyzerPage";

function App() {
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({ username: "", password: "" });

  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");

  const [stats, setStats] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);

  const [view, setView] = useState("home");
  const [selectedProblem, setSelectedProblem] = useState(null);

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

  // 🎯 RECOMMEND (🔥 FIXED)
  const getRecommendation = async () => {
    try {
      if (!user?.id) {
        alert("User not logged in properly");
        return;
      }

      const res = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id })
      });

      if (!res.ok) {
        throw new Error("Server error while fetching recommendations");
      }

      const data = await res.json();

      console.log("RECOMMEND RESPONSE:", data); // 🔥 DEBUG

      // 🔥 CRITICAL FIX
      if (!data || !Array.isArray(data.problems) || data.problems.length === 0) {
        alert("No problems received from backend");
        return;
      }

      setResult(data);
      setView("problems");

    } catch (err) {
      console.error("Recommendation error:", err);
      alert("Failed to fetch recommendations");
    }
  };

  // 📊 FETCH CHART
  const fetchChartStats = async () => {
    try {
      if (!user?.id) return;

      const res = await fetch(`http://127.0.0.1:5000/stats/${user.id}`);
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        setStats([]);
        return;
      }

      setStats(
        data.map((attempt, index) => ({
          id: `${attempt.problem_name}-${index}`,
          problemName: attempt.problem_name,
          accuracy: Number((attempt.accuracy * 100).toFixed(1))
        }))
      );

    } catch (err) {
      console.error("Chart stats error:", err);
    }
  };

  // 🏆 FETCH LEADERBOARD
  const fetchLeaderboard = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/leaderboard");
      const data = await res.json();

      if (!Array.isArray(data) || data.length === 0) {
        setLeaderboard([]);
        return;
      }

      setLeaderboard(
        data.filter((entry) => entry.username !== user?.username)
      );

    } catch (err) {
      console.error("Leaderboard error:", err);
    }
  };

  // 🔥 AFTER ANALYZER DONE
  const handleDone = async (accuracy) => {
    try {
      if (accuracy === null || accuracy === undefined || !selectedProblem) return;

      const res = await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          problem_id: selectedProblem.id,
          problem_name: selectedProblem.name,
          difficulty: result?.difficulty,
          accuracy: accuracy
        })
      });

      if (!res.ok) {
        throw new Error("Submission failed");
      }

      await Promise.all([fetchChartStats(), fetchLeaderboard()]);

      setView("chart");

      // 🔥 REFRESH RECOMMENDATIONS
      getRecommendation();

    } catch (err) {
      console.error("Submit error:", err);
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

  // 🔥 ANALYZER PAGE
  if (view === "analyzer") {
    return (
      <AnalyzerPage
        problem={selectedProblem}
        onDone={handleDone}
      />
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
        <button onClick={() => { fetchChartStats(); setView("chart"); }}>
          Show Chart
        </button>

        <button onClick={() => { fetchLeaderboard(); setView("leaderboard"); }}>
          Show Leaderboard
        </button>
      </div>

      <div className="card">

        {/* PROBLEMS */}
        {view === "problems" && result?.problems && (
          <>
            <h3>🎯 {result.difficulty.toUpperCase()} Problems</h3>

            {result.problems.map((p, i) => (
              <div key={i} className="problem">

                <span
                  className="link"
                  onClick={() => {
                    setSelectedProblem({
                      id: p.contestId + p.index,
                      name: p.name
                    });
                    setView("analyzer");
                  }}
                >
                  {p.name} ({p.rating})
                </span>

                <button
                  onClick={() =>
                    window.open(
                      `https://codeforces.com/problemset/problem/${p.contestId}/${p.index}`,
                      "_blank"
                    )
                  }
                >
                  Solve
                </button>

              </div>
            ))}
          </>
        )}

        {/* CHART */}
        {view === "chart" && (
          <>
            <h3>📊 Performance</h3>
            {stats.length === 0 ? (
              <p>No data yet</p>
            ) : (
              stats.map((s) => (
                <p key={s.id}>{s.problemName}: {s.accuracy}%</p>
              ))
            )}
          </>
        )}

        {/* LEADERBOARD */}
        {view === "leaderboard" && (
          <>
            <h3>🏆 Leaderboard</h3>

            {leaderboard.length === 0 ? (
              <p>No leaderboard data yet</p>
            ) : (
              leaderboard.map((u, i) => (
                <div key={i} className="leader-item">
                  <div className="rank">#{i + 1}</div>
                  <div className="name">
                    <strong>{u.username}</strong>
                    <div className="problem-name">{u.problem_name}</div>
                  </div>
                  <div className="score">
                    {(u.accuracy * 100).toFixed(1)}%
                  </div>
                </div>
              ))
            )}
          </>
        )}

      </div>

      <button className="logout" onClick={() => setUser(null)}>
        Logout
      </button>

    </div>
  );
}

export default App;