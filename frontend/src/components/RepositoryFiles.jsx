import { useEffect, useState } from "react";
import api from "../services/api";

function RepositoryFiles({ repositoryId, onFileSelected }) {
  const [files, setFiles] = useState([]);
  const [currentPath, setCurrentPath] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFiles = async () => {
      setLoading(true);
      setError("");

      try {
        const response = await api.get(
          `/repositories/${repositoryId}/files`,
          {
            params: {
              path: currentPath,
            },
          }
        );

        setFiles(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Failed to load repository files."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, [repositoryId, currentPath]);

  const handleItemClick = (file) => {
    if (file.type === "dir") {
      setCurrentPath(file.path);
      onFileSelected(null);
    } else {
      onFileSelected(file);
    }
  };

  const goBack = () => {
    if (!currentPath) {
      return;
    }

    const pathParts = currentPath.split("/");
    pathParts.pop();

    setCurrentPath(pathParts.join("/"));
    onFileSelected(null);
  };

  if (loading) {
    return <p>Loading repository files...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h3>Repository Files</h3>

      <p>
        <strong>Current Path:</strong>{" "}
        {currentPath || "/"}
      </p>

      {currentPath && (
        <button onClick={goBack}>
          ⬅ Back
        </button>
      )}

      <div>
        {files.map((file) => (
          <div key={file.path}>
            <button
              onClick={() => handleItemClick(file)}
            >
              {file.type === "dir" ? "📁" : "📄"}{" "}
              {file.name}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RepositoryFiles;