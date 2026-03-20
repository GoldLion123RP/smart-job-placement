import fitz  # PyMuPDF
import re
import spacy
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        # Security: Use proper model loading with error handling
        self.nlp = self._load_spacy_model()
        
        # Optimization: Pre-compile regex patterns
        self._whitespace_pattern = re.compile(r'\s+')
        self._clean_pattern = re.compile(r'[^\w\s.,@-]')
        self._experience_patterns = [
            re.compile(r'(\d+)\+?\s*years?\s*(?:of)?\s*experience', re.IGNORECASE),
            re.compile(r'experience\s*:?\s*(\d+)\+?\s*years?', re.IGNORECASE)
        ]
        
        # Optimization: Use frozenset for faster lookups
        self.skill_keywords = {
            'programming': frozenset(['python', 'java', 'c++', 'javascript', 'sql', 'r', 'scala', 'go', 'kotlin', 'swift']),
            'ml_ai': frozenset(['machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'opencv']),
            'web': frozenset(['react', 'angular', 'vue', 'node.js', 'django', 'flask', 'html', 'css', 'bootstrap', 'tailwind']),
            'tools': frozenset(['git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'tableau', 'power bi', 'jenkins', 'ci/cd']),
            'databases': frozenset(['mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch']),
            'soft_skills': frozenset(['leadership', 'communication', 'teamwork', 'problem-solving', 'analytical'])
        }
        
        # Pre-compile skill patterns for word boundary matching
        self._skill_patterns = {}
        for skills in self.skill_keywords.values():
            for skill in skills:
                if ' ' not in skill:  # Only compile for single-word skills
                    self._skill_patterns[skill] = re.compile(r'\b' + re.escape(skill) + r'\b')

    def _load_spacy_model(self):
        """Load spaCy model with proper error handling"""
        try:
            return spacy.load('en_core_web_sm')
        except OSError:
            logger.warning("spaCy model not found, attempting to download...")
            try:
                import subprocess
                subprocess.run(
                    ['python', '-m', 'spacy', 'download', 'en_core_web_sm'],
                    capture_output=True,
                    check=True
                )
                return spacy.load('en_core_web_sm')
            except Exception as e:
                logger.error(f"Failed to download spaCy model: {e}")
                # Return None - will skip NLP processing if unavailable
                return None

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF with error handling"""
        doc = None
        try:
            doc = fitz.open(pdf_path)
            # Security: Limit number of pages to prevent DoS
            if len(doc) > 100:
                logger.warning(f"PDF has too many pages ({len(doc)}), limiting extraction")
            
            text_parts = []
            for page in doc[:100]:  # Limit to first 100 pages
                text_parts.append(page.get_text())
            
            # Security: Limit total text length
            text = " ".join(text_parts)
            if len(text) > 500000:  # 500KB limit
                logger.warning("PDF text too large, truncating")
                text = text[:500000]
            
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
        finally:
            if doc:
                doc.close()

    def clean_text(self, text):
        # Optimization: Use pre-compiled patterns
        text = self._whitespace_pattern.sub(' ', text)
        text = self._clean_pattern.sub('', text)
        return text.lower().strip()

    def extract_skills(self, text):
        text = self.clean_text(text)
        found_skills = {'detected': [], 'categories': {}}
        
        # Optimization: Use pre-compiled patterns for single-word skills
        for category, skills in self.skill_keywords.items():
            category_skills = []
            for skill in skills:
                # Use word boundaries for short skills, contains for multi-word
                if ' ' in skill:
                    if skill in text:
                        category_skills.append(skill)
                        if skill not in found_skills['detected']:
                            found_skills['detected'].append(skill)
                else:
                    # Use pre-compiled pattern
                    pattern = self._skill_patterns.get(skill)
                    if pattern and pattern.search(text):
                        category_skills.append(skill)
                        if skill not in found_skills['detected']:
                            found_skills['detected'].append(skill)

            if category_skills:
                found_skills['categories'][category] = category_skills

        return found_skills

    def extract_education(self, text):
        degrees = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'mba', 'b.sc', 'm.sc', 'b.e', 'm.e']
        text_lower = text.lower()
        
        # Optimization: Use set for faster unique detection
        education = set()
        for degree in degrees:
            if degree in text_lower:
                education.add(degree.upper())

        return list(education)

    def extract_experience(self, text):
        # Optimization: Use pre-compiled patterns
        text_lower = text.lower()
        
        for pattern in self._experience_patterns:
            match = pattern.search(text_lower)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue

        return 0
