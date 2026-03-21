import React, { useState, useCallback, useEffect } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import Results from './components/Results';

const PROD_API_URL = 'https://smart-job-placement.onrender.com';
const LOCAL_API_URL = 'http://localhost:10000';

// Security: Validate API URL
// Use Render backend in production and localhost for local development.
const getApiUrl = () => {
  const isProductionSite = import.meta.env.PROD || window.location.hostname.includes('github.io');
  const fallbackUrl = isProductionSite ? PROD_API_URL : LOCAL_API_URL;

  // Check for environment variable first
  const envUrl = import.meta.env.VITE_API_URL;
  if (envUrl) {
    // Validate it's a proper URL
    try {
      const url = new URL(envUrl);
      // Only allow http/https
      if (url.protocol !== 'http:' && url.protocol !== 'https:') {
        console.warn('Invalid API URL protocol, using default');
        return fallbackUrl;
      }
      return envUrl;
    } catch {
      console.warn('Invalid API URL format, using default');
      return fallbackUrl;
    }
  }
  // Default based on environment
  return fallbackUrl;
};

// Show warning if API URL is not configured
const API_URL = getApiUrl();

const getFriendlyErrorMessage = (error, statusCode, apiHealthy) => {
  const defaultHelp = `Failed to analyze resume.\n\nTry this:\n1) Confirm backend URL in .env.local (VITE_API_URL).\n2) Ensure backend server is running and reachable.\n3) Retry after a few seconds (free-tier cold starts can be slow).`;

  if (statusCode === 400) {
    return 'Request was rejected. Please upload a valid PDF and choose a supported role.';
  }

  if (statusCode === 503) {
    return 'Service is temporarily unavailable. Please wait a moment and try again.';
  }

  if (error?.name === 'AbortError') {
    return 'Request timed out. The backend may be waking up. Please try again in a few seconds.';
  }

  if (error instanceof TypeError || !apiHealthy) {
    return `${defaultHelp}\n\nCurrent API: ${API_URL}`;
  }

  if (typeof error?.message === 'string' && error.message.trim()) {
    return error.message;
  }

  return defaultHelp;
};

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiHealthy, setApiHealthy] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const checkApi = async () => {
      try {
        const response = await fetch(`${API_URL}/`, {
          method: 'GET',
          signal: controller.signal
        });
        if (isMounted) {
          setApiHealthy(response.ok);
        }
      } catch {
        if (isMounted) {
          setApiHealthy(false);
        }
      }
    };

    checkApi();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, []);

  const handleAnalyze = useCallback(async (file, role) => {
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('role', role);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 45000);

      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
        // Security: Don't include credentials unless necessary
        // body is FormData, so Content-Type is set automatically with boundary
      });
      clearTimeout(timeoutId);

      setApiHealthy(true);
      
      // Handle HTTP errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const rawMessage = errorData.error || `HTTP error ${response.status}`;
        const errorWithStatus = new Error(rawMessage);
        errorWithStatus.statusCode = response.status;
        throw errorWithStatus;
      }
      
      const data = await response.json();
      
      // Validate response structure
      if (!data.success) {
        throw new Error(data.error || 'Analysis failed');
      }
      
      setResults(data);
    } catch (err) {
      console.error('Error:', err);
      setApiHealthy(false);
      setError(getFriendlyErrorMessage(err, err?.statusCode, apiHealthy));
    } finally {
      setLoading(false);
    }
  }, [apiHealthy]);

  const handleReset = useCallback(() => {
    setResults(null);
    setError(null);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <div className="hero-top-row">
          <div className={`status-pill ${apiHealthy ? 'ok' : apiHealthy === false ? 'down' : 'checking'}`}>
            {apiHealthy ? 'API Connected' : apiHealthy === false ? 'API Unreachable' : 'Checking API...'}
          </div>
          <span className="hero-chip">AI Career Readiness Suite</span>
        </div>
        <h1>
          Smart Job Placement
          <span className="title-accent"> Analyzer</span>
        </h1>
        <p className="hero-subtitle">Upload your resume, benchmark your skills, and get a focused learning path in under a minute.</p>
        <div className="hero-steps" aria-hidden="true">
          <span>01 Upload</span>
          <span>02 Analyze</span>
          <span>03 Improve</span>
        </div>
      </header>
      <main className="App-main">
        {!results ? (
          <>
            <FileUpload onAnalyze={handleAnalyze} loading={loading} />
            {error && (
              <div className="error-banner">
                <p>{error}</p>
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
