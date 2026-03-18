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
            ]
        }
        return interview_resources.get(role, [])
