import { useState } from "react";
import RepositoryImport from "../components/RepositoryImport";
import RepositoryFiles from "../components/RepositoryFiles";
import FileViewer from "../components/FileViewer";

function Dashboard() {
  const [repository, setRepository] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleRepositoryImported = (importedRepository) => {
    setRepository(importedRepository);
    setSelectedFile(null);
  };

  const handleFileSelected = (file) => {
    setSelectedFile(file);
  };

  return (
    <div>
      <h1>DevPilot AI</h1>

      <h2>Dashboard</h2>

      <p>Welcome to your developer workspace.</p>

      <RepositoryImport
        onImported={handleRepositoryImported}
      />

      {repository && (
        <div>
          <h3>Imported Repository</h3>

          <p>
            <strong>Name:</strong> {repository.name}
          </p>

          <p>
            <strong>Owner:</strong> {repository.owner}
          </p>

          <p>
            <strong>Language:</strong>{" "}
            {repository.language || "Not specified"}
          </p>

          <p>
            <strong>Default Branch:</strong>{" "}
            {repository.default_branch}
          </p>

          <p>
            <strong>Description:</strong>{" "}
            {repository.description || "No description"}
          </p>

          <a
            href={repository.github_url}
            target="_blank"
            rel="noreferrer"
          >
            View on GitHub
          </a>

          <RepositoryFiles
            repositoryId={repository.id}
            onFileSelected={handleFileSelected}
          />

          <FileViewer
            repositoryId={repository.id}
            file={selectedFile}
          />
        </div>
      )}        
    </div>
  );
}

export default Dashboard;