import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Login failed. Please check your credentials."
      );
    }
  };

  return (
    <div>
      <h1>DevPilot AI</h1>

      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        {error && <p>{error}</p>}

        <button type="submit">
          Login
        </button>
      </form>

      <p>
        Don't have an account?{" "}
        <button onClick={() => navigate("/register")}>
          Register
        </button>
      </p>
    </div>
  );
}

export default Login;