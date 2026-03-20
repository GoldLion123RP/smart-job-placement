import React, { useState, useCallback } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import Results from './components/Results';

// Security: Validate API URL
// Default to local backend URL for development
const getApiUrl = () => {
  // Check for environment variable first
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) {
    // Validate it's a proper URL
    try {
      const url = new URL(envUrl);
      // Only allow http/https
      if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        console.warn('Invalid API URL protocol, using default');
        return 'http://localhost:10000';
      }
      return envUrl;
    } catch {
      console.warn('Invalid API URL format, using default');
      return 'http://localhost:10000';
    }
  }
  // Default to local backend
  return 'http://localhost:10000';
};

// Show warning if API URL is not configured
const API_URL = getApiUrl();

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = useCallback(async (file, role) => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('role', role);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
        // Security: Don't include credentials unless necessary
        // body is FormData, so Content-Type is set automatically with boundary
      });
      
      // Handle HTTP errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error ${response.status}`);
      }
      
      const data = await response.json();
      
      // Validate response structure
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed');
      }
      
      setResults(data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.message || 'Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleReset = useCallback(() => {
    setResults(null);
    setError(null);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Job Placement Analyzer</h1>
        <p>Upload your resume and discover your skill gaps!</p>
      </header>
      <main className="App-main">
        {!results ? (
          <>
            <FileUpload onAnalyze={handleAnalyze} loading={loading} />
            {error && (
              <div className="error-banner">
                <p>❌ {error}</p>
                <button onClick={() => setError(null)}>Dismiss</button>
              </div>
            )}
          </>
        ) : (
          <div className="results-wrapper">
            <Results data={results} />
            <button className="reset-btn" onClick={handleReset}>
              🔄 Analyze Another Resume
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
