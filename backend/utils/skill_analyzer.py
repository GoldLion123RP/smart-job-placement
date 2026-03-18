from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

ROLE_SKILLS = {
    "data_scientist": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "sql", "statistics", "pandas", "numpy", "scikit-learn", "data visualization", "nlp", "computer vision"],
    "software_engineer": ["python", "java", "javascript", "algorithms", "data structures", "system design", "git", "docker", "kubernetes", "rest api", "sql", "agile"],
    "web_developer": ["html", "css", "javascript", "react", "node.js", "responsive design", "rest api", "mongodb", "express", "git", "typescript"],
    "ml_engineer": ["python", "tensorflow", "pytorch", "mlops", "docker", "aws", "model deployment", "mlflow", "data engineering", "kubernetes", "airflow"],
    "data_analyst": ["sql", "python", "excel", "tableau", "power bi", "statistics", "data visualization", "pandas", "numpy", "reporting"]
}

RESOURCES = {
    "python": "https://www.python.org/about/gettingstarted/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.deeplearning.ai/",
    "tensorflow": "https://www.tensorflow.org/tutorials",
    "pytorch": "https://pytorch.org/tutorials/",
    "sql": "https://www.w3schools.com/sql/",
    "docker": "https://docs.docker.com/get-started/",
    "aws": "https://aws.amazon.com/training/",
    "react": "https://react.dev/learn",
    "javascript": "https://www.youtube.com/results?search_query=javascript",
    "kubernetes": "https://kubernetes.io/docs/tutorials/",
    "mlops": "https://www.youtube.com/results?search_query=mlops",
    "tableau": "https://www.tableau.com/learn/training",
}

class SkillGapAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def analyze_gap(self, skills, target_role):
        detected = [s.lower() for s in skills.get("detected", [])]
        required = ROLE_SKILLS.get(target_role, [])

        matched = [s for s in required if any(s in d or d in s for d in detected)]
        missing = [s for s in required if s not in matched]

        skill_coverage = round(len(matched) / len(required) * 100, 2) if required else 0

        if detected and required:
            all_skills = detected + required
            try:
                tfidf = self.vectorizer.fit_transform([" ".join(detected), " ".join(required)])
                match_score = round(float(cosine_similarity(tfidf[0], tfidf[1])[0][0]) * 100, 2)
            except:
                match_score = skill_coverage
        else:
            match_score = 0

        return {
            "match_score": match_score,
            "skill_coverage": skill_coverage,
            "matched_skills": matched,
            "missing_skills": missing,
            "required_skills": required
        }

    def get_recommendations(self, missing_skills):
        recommendations = []
        for skill in missing_skills[:5]:
            resource = RESOURCES.get(skill, f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}")
            recommendations.append({"skill": skill, "resource": resource})
        return recommendations

    def get_available_roles(self):
        return list(ROLE_SKILLS.keys())
