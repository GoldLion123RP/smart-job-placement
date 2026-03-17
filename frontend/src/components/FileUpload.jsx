import React, { useState } from 'react';
import './FileUpload.css';

const roles = [
  'data_scientist',
  'software_engineer',
  'web_developer',
  'ml_engineer',
  'data_analyst'
];

function FileUpload({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState('data_scientist');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onAnalyze(file, role);
    }
  };

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Upload Resume (PDF)</label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            required
          />
          {file && <p className="file-name">{file.name}</p>}
        </div>

        <div className="form-group">
          <label>Target Job Role</label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            {roles.map(r => (
              <option key={r} value={r}>
                {r.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={loading || !file}>
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </form>
    </div>
  );
}

export default FileUpload;
