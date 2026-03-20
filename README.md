# Smart Job Placement & Skill Gap Analyzer

An AI-powered full-stack web application that analyzes resumes, identifies skill gaps against target job roles, predicts placement probability, and recommends personalized learning resources.

🔗 **Live Demo:** [https://GoldLion123RP.github.io/smart-job-placement](https://GoldLion123RP.github.io/smart-job-placement)
🔗 **Backend API:** [https://smart-job-placement.onrender.com](https://smart-job-placement.onrender.com)

---

## Features

- **Resume Parsing** — Extracts skills, education, and experience from PDF resumes using PyMuPDF and spaCy
- **Skill Gap Analysis** — TF-IDF cosine similarity matching between resume skills and target job role requirements
- **Placement Prediction** — Weighted scoring model based on skill count, experience, education, skill coverage, and match score
- **Course Recommendations** — Curated learning resources from Coursera, Udemy, and YouTube for missing skills
- **Interview Preparation** — Role-specific interview prep resources and practice links
- **PDF Report Download** — Generate and download a full skill gap analysis report as PDF

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask, spaCy, scikit-learn, PyMuPDF, gunicorn |
| Frontend | React 18, Vite, Chart.js, jsPDF |
| Backend Hosting | Render (Free Tier) |
| Frontend Hosting | GitHub Pages |

---

## Project Structure

```
smart-job-placement/
├── backend/
│   ├── utils/
│   │   ├── resume_parser.py        # PDF parsing + skill extraction
│   │   ├── skill_analyzer.py       # TF-IDF skill gap analysis
│   │   ├── placement_predictor.py  # Placement probability scoring
│   │   └── course_recommender.py   # Course + interview prep recommendations
│   ├── app.py                      # Flask REST API
│   ├── requirements.txt
│   └── Procfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── FileUpload.css
│   │   │   ├── Results.jsx
│   │   │   └── Results.css
│   │   ├── utils/
│   │   │   └── reportGenerator.js  # PDF report generation
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── vite.config.js
│   └── package.json
└── README.md
```

---

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js v20+
- npm

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at `http://localhost:10000`

### Frontend

```bash
cd frontend
copy .env.example .env.local
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### Environment Files

- Use `frontend/.env.example` as a public template (safe to commit).
- Put real values in `frontend/.env.local` (never commit).
- Recommended local values:

```env
VITE_API_URL=https://smart-job-placement.onrender.com
GITHUB_PAGES_URL=https://goldlion123rp.github.io
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/analyze` | Analyze resume PDF against target role |
| GET | `/api/roles` | List available job roles |

### POST /api/analyze

**Request:** `multipart/form-data`
- `resume` — PDF file
- `role` — Target role

**Response:**
```json
{
  "success": true,
  "skills": { "detected": [...], "categories": {} },
  "education": ["B.TECH"],
  "experience": 2,
  "gap_analysis": {
    "match_score": 37.38,
    "skill_coverage": 50.0,
    "matched_skills": [...],
    "missing_skills": [...]
  },
  "placement_probability": {
    "probability": 58.5,
    "confidence": "Medium"
  },
  "recommendations": {
    "courses": [...],
    "interview_prep": [...]
  }
}
```

---

## Supported Job Roles

- `data_scientist`
- `software_engineer`
- `web_developer`
- `ml_engineer`
- `data_analyst`

---

## Deployment

### Backend — Render
1. Push `backend/` to GitHub
2. Create Web Service on [render.com](https://render.com)
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Frontend — GitHub Pages
```bash
cd frontend
npm run build
cd ..
git add frontend/dist -f
git commit -m "Deploy frontend"
git subtree push --prefix frontend/dist origin gh-pages
```
Enable Pages on `gh-pages` branch in repository Settings.

---

## Known Issues & Notes

- `torch` and `sentence-transformers` removed — exceeded Render free tier 512MB RAM limit
- spaCy model installed via direct wheel URL for Render compatibility
- Vite uses `VITE_` env prefix — not `REACT_APP_`
- Node.js path must have no spaces on Windows

---

## Developer 👤

**Rahul Pal** — [GitHub](https://github.com/GoldLion123RP)

