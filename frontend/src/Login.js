
import React, { useState } from "react";
import "./App.css";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page reload
    if (username === "admin" && password === "admin123") {
      onLogin();
    } else {
      setError("Invalid credentials. Try again.");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <div className="icon-circle">🔐</div>
          <h2>Welcome Back</h2>
          <p>Please enter your details to access the dashboard</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="error-banner">{error}</div>}

          <button type="submit" className="login-btn">Sign In</button>
        </form>

        <div className="hint-box">
          <small>Demo Access</small>
          <p>User: <span>admin</span> | Pass: <span>admin123</span></p>
        </div>
      </div>
    </div>
  );
}

export default Login;