import fitz  # PyMuPDF
from pypdf import PdfReader
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

    def _has_meaningful_text(self, text):
        """Return True when extracted text likely contains readable resume content."""
        if not text:
            return False
        # Require a minimum number of alphanumeric characters to avoid empty/scanned PDFs.
        return len(re.findall(r'[A-Za-z0-9]', text)) >= 40

    def _extract_with_pymupdf(self, pdf_path):
        doc = None
        try:
            doc = fitz.open(pdf_path)
            if len(doc) > 100:
                logger.warning(f"PDF has too many pages ({len(doc)}), limiting extraction")

            text_parts = []
            for page in doc[:100]:
                text_parts.append(page.get_text() or "")

            text = " ".join(text_parts)
            if len(text) > 500000:
                logger.warning("PDF text too large, truncating")
                text = text[:500000]
            return text
        finally:
            if doc:
                doc.close()

    def _extract_with_pypdf(self, pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            text_parts = []
            for page in reader.pages[:100]:
                text_parts.append(page.extract_text() or "")

        text = " ".join(text_parts)
        if len(text) > 500000:
            text = text[:500000]
        return text

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
        try:
            text = self._extract_with_pymupdf(pdf_path)
        except Exception as fitz_error:
            logger.warning(f"PyMuPDF extraction failed, trying pypdf fallback: {fitz_error}")
            try:
                text = self._extract_with_pypdf(pdf_path)
            except Exception as pypdf_error:
                logger.error(f"PDF extraction failed with both parsers: {pypdf_error}")
                raise ValueError(
                    "Could not read this PDF. Please re-export it as a standard, unlocked PDF and try again."
                )

        if not self._has_meaningful_text(text):
            raise ValueError(
                "Could not extract readable text from this PDF. If it is scanned/image-based, run OCR or export a text PDF and retry."
            )

        return text

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
