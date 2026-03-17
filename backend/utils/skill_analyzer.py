from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SkillGapAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.job_role_skills = {
            'data_scientist': ['python', 'machine learning', 'statistics', 'sql', 'data visualization', 'deep learning', 'nlp', 'pandas', 'numpy', 'scikit-learn'],
            'software_engineer': ['java', 'python', 'algorithms', 'data structures', 'git', 'oop', 'sql', 'api development', 'testing', 'debugging'],
            'web_developer': ['javascript', 'html', 'css', 'react', 'node.js', 'git', 'responsive design', 'rest api', 'mongodb', 'express'],
            'ml_engineer': ['python', 'tensorflow', 'pytorch', 'mlops', 'docker', 'kubernetes', 'aws', 'model deployment', 'mlflow', 'data engineering'],
            'data_analyst': ['sql', 'python', 'excel', 'tableau', 'power bi', 'statistics', 'data visualization', 'pandas', 'data cleaning']
        }

    def get_available_roles(self):
        return list(self.job_role_skills.keys())

    def analyze_gap(self, resume_skills, target_role):
        if target_role.lower() not in self.job_role_skills:
            return {"error": "Role not found"}

        required_skills = self.job_role_skills[target_role.lower()]
        resume_skill_list = resume_skills['detected']

        resume_embedding = self.model.encode(' '.join(resume_skill_list))
        required_embedding = self.model.encode(' '.join(required_skills))

        similarity_score = cosine_similarity(
            resume_embedding.reshape(1, -1),
            required_embedding.reshape(1, -1)
        )[0][0]

        resume_text = ' '.join(resume_skill_list).lower()
        missing_skills = [skill for skill in required_skills if skill not in resume_text]
        matched_skills = [skill for skill in required_skills if skill in resume_text]

        return {
            'match_score': round(similarity_score * 100, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'skill_coverage': round((len(matched_skills) / len(required_skills)) * 100, 2)
        }

    def get_recommendations(self, missing_skills):
        course_map = {
            'python': 'https://www.coursera.org/learn/python',
            'machine learning': 'https://www.coursera.org/learn/machine-learning',
            'deep learning': 'https://www.coursera.org/specializations/deep-learning',
            'sql': 'https://www.coursera.org/learn/sql-for-data-science',
            'react': 'https://react.dev/learn',
            'node.js': 'https://nodejs.org/en/docs/guides',
            'docker': 'https://docs.docker.com/get-started/',
            'aws': 'https://aws.amazon.com/training/'
        }

        recommendations = []
        for skill in missing_skills[:5]:
            recommendations.append({
                'skill': skill,
                'resource': course_map.get(skill.lower(), 'https://www.youtube.com/results?search_query=' + skill.replace(' ', '+'))
            })

        return recommendations
