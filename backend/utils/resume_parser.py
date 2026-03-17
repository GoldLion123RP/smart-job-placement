import fitz  # PyMuPDF
import re
import spacy

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            print("Downloading spaCy model...")
            import os
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')

        self.skill_keywords = {
            'programming': ['python', 'java', 'c++', 'javascript', 'sql', 'r', 'scala', 'go', 'kotlin', 'swift'],
            'ml_ai': ['machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv'],
            'web': ['react', 'angular', 'vue', 'node.js', 'django', 'flask', 'html', 'css', 'bootstrap', 'tailwind'],
            'tools': ['git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'tableau', 'power bi', 'jenkins', 'ci/cd'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical']
        }

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,@-]', '', text)
        return text.lower().strip()

    def extract_skills(self, text):
        text = self.clean_text(text)
        found_skills = {'detected': [], 'categories': {}}

        for category, skills in self.skill_keywords.items():
            category_skills = []
            for skill in skills:
                if skill.lower() in text:
                    category_skills.append(skill)
                    if skill not in found_skills['detected']:
                        found_skills['detected'].append(skill)

            if category_skills:
                found_skills['categories'][category] = category_skills

        return found_skills

    def extract_education(self, text):
        degrees = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'mba', 'b.sc', 'm.sc', 'b.e', 'm.e']
        education = []
        text = text.lower()

        for degree in degrees:
            if degree in text:
                education.append(degree.upper())

        return list(set(education))

    def extract_experience(self, text):
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?'
        ]

        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))

        return 0
