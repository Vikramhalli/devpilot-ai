import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import api from "../services/api";

function FileViewer({ repositoryId, file }) {
  const [fileData, setFileData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [analysis, setAnalysis] = useState("");
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    if (!file || file.type !== "file") {
      setFileData(null);
      setAnalysis("");
      return;
    }

    const fetchFile = async () => {
      setLoading(true);
      setError("");
      setAnalysis("");

      try {
        const response = await api.get(
          `/repositories/${repositoryId}/file`,
          {
            params: {
              path: file.path,
            },
          }
        );

        setFileData(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Failed to load file."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchFile();
  }, [repositoryId, file]);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    setError("");
    setAnalysis("");

    try {
      const response = await api.post(
        `/repositories/${repositoryId}/analyze`,
        null,
        {
          params: {
            path: file.path,
          },
        }
      );

      setAnalysis(response.data.analysis);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "AI analysis failed."
      );
    } finally {
      setAnalyzing(false);
    }
  };

  if (!file) {
    return <p>Select a file to view its contents.</p>;
  }

  if (loading) {
    return <p>Loading file...</p>;
  }

  if (error && !fileData) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h3>Source Code</h3>

      <p>
        <strong>{fileData?.name}</strong>
      </p>

      <pre
        style={{
          whiteSpace: "pre-wrap",
          overflowX: "auto",
          overflowWrap: "anywhere",
          maxWidth: "100%",
        }}
      >
        <code>{fileData?.content}</code>
      </pre>

      <button
        onClick={handleAnalyze}
        disabled={analyzing}
      >
        {analyzing
          ? "Analyzing..."
          : "🤖 Analyze with AI"}
      </button>

      {error && <p>{error}</p>}

      {analysis && (
        <div
          style={{
            marginTop: "20px",
            padding: "20px",
            maxWidth: "100%",
            lineHeight: "1.6",
          }}
        >
          <h3>AI Analysis</h3>

          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {analysis}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default FileViewer;