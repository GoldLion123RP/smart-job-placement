import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import Results from './components/Results';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (file, role) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('role', role);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Job Placement Analyzer</h1>
        <p>Upload your resume and discover your skill gaps!</p>
      </header>
      <main className="App-main">
        <FileUpload onAnalyze={handleAnalyze} loading={loading} />
        {results && <Results data={results} />}
      </main>
    </div>
  );
}

export default App;
