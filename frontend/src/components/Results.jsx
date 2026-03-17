import React from 'react';
import './Results.css';

function Results({ data }) {
  if (!data.success) {
    return <div className="error">Error: {data.error}</div>;
  }

  const { gap_analysis, placement_probability, recommendations } = data;

  return (
    <div className="results-container">
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Match Score</h3>
          <div className="metric-value">{gap_analysis.match_score}%</div>
        </div>
        <div className="metric-card">
          <h3>Skill Coverage</h3>
          <div className="metric-value">{gap_analysis.skill_coverage}%</div>
        </div>
        <div className="metric-card">
          <h3>Placement Probability</h3>
          <div className="metric-value">{placement_probability.probability}%</div>
        </div>
      </div>

      <div className="skills-section">
        <div className="skills-box matched">
          <h3>Matched Skills ({gap_analysis.matched_skills.length})</h3>
          <div className="skill-tags">
            {gap_analysis.matched_skills.map((skill, i) => (
              <span key={i} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>

        <div className="skills-box missing">
          <h3>Missing Skills ({gap_analysis.missing_skills.length})</h3>
          <div className="skill-tags">
            {gap_analysis.missing_skills.map((skill, i) => (
              <span key={i} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="recommendations-section">
        <h3>Recommended Learning Resources</h3>
        <div className="recommendations-list">
          {recommendations.map((rec, i) => (
            <a key={i} href={rec.resource} target="_blank" rel="noopener noreferrer" className="recommendation-card">
              <strong>{rec.skill}</strong>
              <span>Learn Now</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Results;
