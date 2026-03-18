import React from "react";
import { generatePDFReport } from "../utils/reportGenerator";
import "./Results.css";

function Results({ data }) {
  if (!data.success) return <div className="error">Error: {data.error}</div>;

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
          <div className="confidence-badge">{placement_probability.confidence}</div>
        </div>
      </div>

      <div className="skills-section">
        <div className="skills-box matched">
          <h3>✅ Matched Skills ({gap_analysis.matched_skills.length})</h3>
          <div className="skill-tags">
            {gap_analysis.matched_skills.map((skill, i) => (
              <span key={i} className="skill-tag matched-tag">{skill}</span>
            ))}
          </div>
        </div>
        <div className="skills-box missing">
          <h3>❌ Missing Skills ({gap_analysis.missing_skills.length})</h3>
          <div className="skill-tags">
            {gap_analysis.missing_skills.map((skill, i) => (
              <span key={i} className="skill-tag missing-tag">{skill}</span>
            ))}
          </div>
        </div>
      </div>

      {recommendations?.courses && recommendations.courses.length > 0 && (
        <div className="recommendations-section">
          <h2>🎓 Recommended Learning Path</h2>
          <div className="courses-grid">
            {recommendations.courses.map((rec, i) => (
              <div key={i} className="course-card">
                <div className="course-header">
                  <span className="skill-badge">{rec.skill}</span>
                  <span className="level-badge">{rec.level}</span>
                </div>
                <h4>{rec.course}</h4>
                <div className="course-meta">
                  <span>📚 {rec.provider}</span>
                  <span>⏱️ {rec.duration}</span>
                </div>
                <a href={rec.url} target="_blank" rel="noopener noreferrer" className="enroll-btn">Start Learning →</a>
              </div>
            ))}
          </div>
        </div>
      )}

      {recommendations?.interview_prep && recommendations.interview_prep.length > 0 && (
        <div className="interview-prep-section">
          <h2>🎤 Interview Preparation</h2>
          <div className="prep-resources">
            {recommendations.interview_prep.map((resource, i) => (
              <a key={i} href={resource.url} target="_blank" rel="noopener noreferrer" className="prep-card">
                <div className="prep-icon">
                  {resource.type === "Coding Practice" ? "💻" : resource.type === "Projects" ? "🛠️" : resource.type === "Conceptual" ? "📖" : "❓"}
                </div>
                <div className="prep-content">
                  <h4>{resource.title}</h4>
                  <span className="prep-type">{resource.type}</span>
                </div>
                <span className="arrow">→</span>
              </a>
            ))}
          </div>
        </div>
      )}

      <button className="download-btn" onClick={() => generatePDFReport(data)}>📥 Download PDF Report</button>
    </div>
  );
}

export default Results;
