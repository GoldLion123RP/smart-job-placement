import React, { useState, useCallback } from 'react';
import './FileUpload.css';

const roles = [
  'data_scientist',
  'software_engineer',
  'web_developer',
  'ml_engineer',
  'data_analyst'
];

const roleDisplayNames = {
  'data_scientist': 'Data Scientist',
  'software_engineer': 'Software Engineer',
  'web_developer': 'Web Developer',
  'ml_engineer': 'ML Engineer',
  'data_analyst': 'Data Analyst'
};

// Security: File size limit (5MB)
const MAX_FILE_SIZE = 5 * 1024 * 1024;

function FileUpload({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState('data_scientist');
  const [error, setError] = useState('');

  const handleFileChange = useCallback((e) => {
    const selectedFile = e.target.files?.[0];
    
    if (!selectedFile) {
      return;
    }

    // Security: Validate file type
    if (selectedFile.type !== 'application/pdf') {
      setError('Please upload a PDF file only');
      setFile(null);
      return;
    }
    
    // Security: Validate file extension as additional check
    const fileName = selectedFile.name.toLowerCase();
    if (!fileName.endsWith('.pdf')) {
      setError('Please upload a PDF file only');
      setFile(null);
      return;
    }

    // Security: Validate file size
    if (selectedFile.size > MAX_FILE_SIZE) {
      setError('File size should not exceed 5MB');
      setFile(null);
      return;
    }
    
    // Security: Validate file name for potential path traversal
    if (selectedFile.name.includes('..') || selectedFile.name.includes('/') || selectedFile.name.includes('\\')) {
      setError('Invalid file name');
      setFile(null);
      return;
    }

    setError('');
    setFile(selectedFile);
  }, []);

  const handleRoleChange = useCallback((e) => {
    setRole(e.target.value);
  }, []);

  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    if (file && !error) {
      onAnalyze(file, role);
    }
  }, [file, error, onAnalyze, role]);

  return (
    <div className="upload-container">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>📄 Upload Resume (PDF only, max 5MB)</label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={loading}
            required
          />
          {file && !error && (
            <p className="file-name">✅ {file.name} ({(file.size / 1024).toFixed(2)} KB)</p>
          )}
          {error && <p className="error-message">❌ {error}</p>}
        </div>

        <div className="form-group">
          <label>🎯 Target Job Role</label>
          <select
            value={role}
            onChange={handleRoleChange}
            disabled={loading}
          >
            {roles.map(r => (
              <option key={r} value={r}>
                {roleDisplayNames[r]}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={loading || !file || error}>
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Resume...
            </>
          ) : (
            '🚀 Analyze Resume'
          )}
        </button>
      </form>

      {loading && (
        <div className="loading-info">
          <p>⏱️ This may take 10-30 seconds (free tier server)</p>
          <p>🔍 Parsing PDF, extracting skills, analyzing gaps...</p>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
