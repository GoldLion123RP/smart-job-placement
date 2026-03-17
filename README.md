# Smart Job Placement & Skill Gap Analyzer

An AI-powered platform that analyzes resumes, predicts placement probability, and identifies skill gaps based on target job roles.

## Features

- **Resume Parsing** — Extracts skills, education, and experience from PDF resumes using PyMuPDF and spaCy
- **Skill Gap Analysis** — Semantic matching between resume skills and target job role requirements using Sentence Transformers
- **Placement Prediction** — Weighted scoring based on skill count, experience, education, skill coverage, and match score
- **Smart Recommendations** — Personalized learning resource links for missing skills

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask, scikit-learn, spaCy, Sentence Transformers, PyMuPDF |
| Frontend | React 18, Vite, Chart.js |
| Deployment | Render (Backend), GitHub Pages (Frontend) |

## Project Structure

```
smart-job-placement/
├── backend/
│   ├── data/
│   ├── models/
│   ├── utils/
│   │   ├── resume_parser.py       # PDF parsing + skill extraction
│   │   ├── skill_analyzer.py      # Semantic skill gap analysis
│   │   └── placement_predictor.py # Placement probability scoring
│   ├── app.py                     # Flask API
│   ├── requirements.txt
│   ├── Procfile                   # For Render deployment
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   └── Results.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── .env
└── README.md
```

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js v20+ (use a path **without spaces**)
- npm

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
python app.py
```

Backend runs at `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

> **Important:** Keep both terminals running simultaneously. Frontend calls backend at `http://localhost:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/analyze` | Analyze resume PDF |
| GET | `/api/roles` | List available job roles |

### POST /api/analyze

**Request:** `multipart/form-data`
- `resume` — PDF file
- `role` — Target role (`data_scientist`, `software_engineer`, `web_developer`, `ml_engineer`, `data_analyst`)

**Response:**
```json
{
  "success": true,
  "skills": { "detected": [...], "categories": {...} },
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
  "recommendations": [...]
}
```

## Supported Job Roles

- `data_scientist`
- `software_engineer`
- `web_developer`
- `ml_engineer`
- `data_analyst`

## Known Issues & Notes

- Project path must have **no spaces** — use `E:\Projects\smart-job-placement` (Node.js v24 on Windows breaks with spaces in paths)
- `sentence-transformers==2.7.0` required — v2.2.2 is incompatible with `huggingface_hub>=0.36`
- spaCy model must be installed manually via direct wheel URL (see setup above)
- Vite uses `VITE_` env prefix — not `REACT_APP_`

## Deployment

### Backend (Render)
1. Push `backend/` folder to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app`

### Frontend (GitHub Pages)
1. Update `VITE_API_URL` in `frontend/.env` with your Render backend URL
2. Run `npm run build`
3. Deploy `dist/` folder to GitHub Pages

## Developer

**Rahul Pal** 