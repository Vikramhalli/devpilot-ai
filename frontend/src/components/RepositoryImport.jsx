import { useState } from "react";
import api from "../services/api";

function RepositoryImport({ onImported }) {
  const [githubUrl, setGithubUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImport = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await api.post("/github/import", {
        github_url: githubUrl,
      });

      setGithubUrl("");

      if (onImported) {
        onImported(response.data);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Failed to import repository."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Import GitHub Repository</h3>

      <form onSubmit={handleImport}>
        <input
          type="url"
          placeholder="https://github.com/owner/repository"
          value={githubUrl}
          onChange={(event) => setGithubUrl(event.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Importing..." : "Import Repository"}
        </button>
      </form>

      {error && <p>{error}</p>}
    </div>
  );
}

export default RepositoryImport;