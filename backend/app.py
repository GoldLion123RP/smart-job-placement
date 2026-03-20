from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from functools import wraps
from utils.resume_parser import ResumeParser
from utils.skill_analyzer import SkillGapAnalyzer
from utils.placement_predictor import PlacementPredictor
from utils.course_recommender import CourseRecommender

app = Flask(__name__)
# Security: Configure CORS properly - restrict to known origins in production
# For development, use specific origins; for production, configure properly
# CORS Configuration for GitHub Pages and local development
# Add your GitHub Pages URL to this list
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
# Also allow GitHub Pages URL from environment variable if provided
github_pages = os.environ.get('GITHUB_PAGES_URL', '')
cors_origins = CORS_ORIGINS.split(',')
if github_pages:
    cors_origins.append(github_pages)

CORS(app, 
    origins=cors_origins,
    methods=['POST', 'GET'],
    allow_headers=['Content-Type'],
    supports_credentials=True
)

# Security: Set secret key for sessions (use environment variable in production)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Security: Configure max content length for file uploads (5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Initialize utilities
parser = ResumeParser()
analyzer = SkillGapAnalyzer()
predictor = PlacementPredictor()
course_recommender = CourseRecommender()

# Valid roles for input validation
try:
    VALID_ROLES = analyzer.get_available_roles()
except Exception as e:
    print(f"Warning: Could not load roles: {e}")
    VALID_ROLES = []

# Security: Input validation decorator
def validate_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip validation if roles list is empty (fallback mode)
        if not VALID_ROLES:
            return f(*args, **kwargs)
        
        role = request.form.get("role", "data_scientist")
        if role not in VALID_ROLES:
            return jsonify({"error": "Invalid role specified"}), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Smart Job Placement API", "version": "1.0.0"})

@app.route("/api/analyze", methods=["POST"])
@validate_role
def analyze_resume():
    temp_path = None
    try:
        # Security: Validate file presence
        if "resume" not in request.files:
            return jsonify({"error": "No resume file provided"}), 400

        file = request.files["resume"]
        
        # Security: Validate file type (check both content-type and extension)
        filename = file.filename.lower()
        if not filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Security: Validate file content starts with PDF magic bytes
        file_content = file.read(5)
        file.seek(0)  # Reset file pointer
        if file_content != b'%PDF-':
            return jsonify({"error": "Invalid PDF file"}), 400

        target_role = request.form.get("role", "data_scientist")

        # Create temp directory with secure permissions
        os.makedirs("data", exist_ok=True)
        temp_path = os.path.join("data", f"temp_resume_{os.urandom(8).hex()}.pdf")
        file.save(temp_path)

        # Parse resume
        resume_text = parser.extract_text_from_pdf(temp_path)
        
        # Security: Limit text processing to prevent DoS
        if len(resume_text) > 500000:  # 500KB limit
            return jsonify({"error": "Resume content too large. Please upload a smaller file."}), 400
        
        skills = parser.extract_skills(resume_text)
        education = parser.extract_education(resume_text)
        experience = parser.extract_experience(resume_text)

        # Analyze and predict
        gap_analysis = analyzer.analyze_gap(skills, target_role)
        placement_score = predictor.predict_placement({
            "skills": skills,
            "education": education,
            "experience": experience
        }, gap_analysis)

        course_recs = course_recommender.get_recommendations(gap_analysis["missing_skills"])
        interview_prep = course_recommender.get_interview_prep(target_role)

        return jsonify({
            "success": True,
            "skills": skills,
            "education": education,
            "experience": experience,
            "gap_analysis": gap_analysis,
            "placement_probability": placement_score,
            "recommendations": {
                "courses": course_recs,
                "interview_prep": interview_prep
            }
        })

    # Security: Don't expose raw error messages to clients
    except (ValueError, KeyError, TypeError) as e:
        app.logger.error(f"Validation error: {str(e)}")
        return jsonify({"error": "Invalid input provided"}), 400
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({"error": "An error occurred while analyzing your resume. Please try again."}), 500
    finally:
        # Security: Always clean up temp file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

@app.route("/api/roles", methods=["GET"])
def get_roles():
    return jsonify({"roles": analyzer.get_available_roles()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
