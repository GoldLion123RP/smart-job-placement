import requests
from typing import List, Dict

class CourseRecommender:
    def __init__(self):
        self.course_database = self._build_course_db()
    
    def _build_course_db(self) -> Dict:
        return {
            'python': [
                {'title': 'Python for Everybody', 'provider': 'Coursera', 'url': 'https://www.coursera.org/specializations/python', 'level': 'Beginner', 'duration': '8 months'},
                {'title': 'Complete Python Bootcamp', 'provider': 'Udemy', 'url': 'https://www.udemy.com/course/complete-python-bootcamp/', 'level': 'All Levels', 'duration': '22 hours'}
            ],
            'machine learning': [
                {'title': 'Machine Learning Specialization', 'provider': 'Coursera', 'url': 'https://www.coursera.org/specializations/machine-learning-introduction', 'level': 'Intermediate', 'duration': '3 months'},
                {'title': 'Practical Machine Learning', 'provider': 'YouTube', 'url': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI', 'level': 'Beginner', 'duration': '4 hours'}
            ],
            'deep learning': [
                {'title': 'Deep Learning Specialization', 'provider': 'Coursera', 'url': 'https://www.coursera.org/specializations/deep-learning', 'level': 'Advanced', 'duration': '5 months'}
            ],
            'sql': [
                {'title': 'SQL for Data Science', 'provider': 'Coursera', 'url': 'https://www.coursera.org/learn/sql-for-data-science', 'level': 'Beginner', 'duration': '4 weeks'}
            ],
            'react': [
                {'title': 'React - The Complete Guide', 'provider': 'Udemy', 'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/', 'level': 'All Levels', 'duration': '48 hours'}
            ],
            'docker': [
                {'title': 'Docker Mastery', 'provider': 'Udemy', 'url': 'https://www.udemy.com/course/docker-mastery/', 'level': 'All Levels', 'duration': '19 hours'}
            ],
            'aws': [
                {'title': 'AWS Certified Solutions Architect', 'provider': 'AWS Training', 'url': 'https://aws.amazon.com/certification/certified-solutions-architect-associate/', 'level': 'Intermediate', 'duration': 'Self-paced'}
            ]
        }
    
    def get_recommendations(self, missing_skills: List[str]) -> List[Dict]:
        recommendations = []
        for skill in missing_skills[:5]:
            skill_lower = skill.lower()
            if skill_lower in self.course_database:
                for course in self.course_database[skill_lower][:2]:
                    recommendations.append({'skill': skill, 'course': course['title'], 'provider': course['provider'], 'url': course['url'], 'level': course['level'], 'duration': course['duration']})
            else:
                recommendations.append({'skill': skill, 'course': f'Learn {skill.title()}', 'provider': 'YouTube', 'url': f'https://www.youtube.com/results?search_query=learn+{skill.replace(" ", "+")}', 'level': 'All Levels', 'duration': 'Varies'})
        return recommendations
    
    def get_interview_prep(self, role: str) -> List[Dict]:
        interview_resources = {
            'data_scientist': [
                {'title': 'Data Science Interview Questions', 'type': 'Practice', 'url': 'https://www.interviewquery.com/p/data-science-interview-questions'},
                {'title': 'Kaggle Competitions', 'type': 'Hands-on', 'url': 'https://www.kaggle.com/competitions'}
            ],
            'software_engineer': [
                {'title': 'LeetCode Problem Set', 'type': 'Coding Practice', 'url': 'https://leetcode.com/problemset/all/'},
                {'title': 'System Design Primer', 'type': 'Conceptual', 'url': 'https://github.com/donnemartin/system-design-primer'}
            ],
            'web_developer': [
                {'title': 'Frontend Mentor Challenges', 'type': 'Projects', 'url': 'https://www.frontendmentor.io/challenges'},
                {'title': 'JavaScript Interview Questions', 'type': 'Q&A', 'url': 'https://github.com/sudheerj/javascript-interview-questions'}
            ],
            'ml_engineer': [
                {'title': 'MLOps Interview Questions', 'type': 'Practice', 'url': 'https://www.youtube.com/results?search_query=mlops+interview+questions'},
                {'title': 'Kaggle Competitions', 'type': 'Hands-on', 'url': 'https://www.kaggle.com/competitions'}
            ],
            'data_analyst': [
                {'title': 'SQL Interview Questions', 'type': 'Practice', 'url': 'https://www.interviewquery.com/p/sql-interview-questions'},
                {'title': 'Tableau Public Gallery', 'type': 'Projects', 'url': 'https://public.tableau.com/gallery'}
            ],
            'frontend_engineer': [
                {'title': 'Frontend Interview Handbook', 'type': 'Practice', 'url': 'https://www.frontendinterviewhandbook.com/'},
                {'title': 'Frontend Mentor Challenges', 'type': 'Projects', 'url': 'https://www.frontendmentor.io/challenges'}
            ],
            'backend_engineer': [
                {'title': 'Backend Interview Questions', 'type': 'Practice', 'url': 'https://www.interviewbit.com/backend-developer-interview-questions/'},
                {'title': 'System Design Primer', 'type': 'Conceptual', 'url': 'https://github.com/donnemartin/system-design-primer'}
            ],
            'fullstack_developer': [
                {'title': 'Full Stack Open', 'type': 'Projects', 'url': 'https://fullstackopen.com/en/'},
                {'title': 'LeetCode Problem Set', 'type': 'Coding Practice', 'url': 'https://leetcode.com/problemset/all/'}
            ],
            'devops_engineer': [
                {'title': 'DevOps Interview Questions', 'type': 'Practice', 'url': 'https://www.interviewbit.com/devops-interview-questions/'},
                {'title': 'Kubernetes By Example', 'type': 'Hands-on', 'url': 'https://kubernetesbyexample.com/'}
            ],
            'cloud_engineer': [
                {'title': 'AWS Skill Builder', 'type': 'Hands-on', 'url': 'https://skillbuilder.aws/'},
                {'title': 'Azure Architecture Center', 'type': 'Conceptual', 'url': 'https://learn.microsoft.com/en-us/azure/architecture/'}
            ],
            'data_engineer': [
                {'title': 'Data Engineering Zoomcamp', 'type': 'Projects', 'url': 'https://github.com/DataTalksClub/data-engineering-zoomcamp'},
                {'title': 'SQL Interview Questions', 'type': 'Practice', 'url': 'https://www.interviewquery.com/p/sql-interview-questions'}
            ],
            'ai_engineer': [
                {'title': 'Hugging Face Course', 'type': 'Hands-on', 'url': 'https://huggingface.co/learn'},
                {'title': 'LLM Engineering Guide', 'type': 'Conceptual', 'url': 'https://github.com/mlabonne/llm-course'}
            ],
            'mobile_developer': [
                {'title': 'Android Developers Guides', 'type': 'Conceptual', 'url': 'https://developer.android.com/guide'},
                {'title': 'Flutter Codelabs', 'type': 'Hands-on', 'url': 'https://docs.flutter.dev/codelabs'}
            ],
            'cybersecurity_analyst': [
                {'title': 'TryHackMe Learning Paths', 'type': 'Hands-on', 'url': 'https://tryhackme.com/r/resources/blog/free_path'},
                {'title': 'OWASP Top 10', 'type': 'Conceptual', 'url': 'https://owasp.org/www-project-top-ten/'}
            ],
            'qa_engineer': [
                {'title': 'Playwright Docs', 'type': 'Hands-on', 'url': 'https://playwright.dev/docs/intro'},
                {'title': 'Cypress Best Practices', 'type': 'Practice', 'url': 'https://docs.cypress.io/guides/references/best-practices'}
            ]
        }
        return interview_resources.get(role, [])
