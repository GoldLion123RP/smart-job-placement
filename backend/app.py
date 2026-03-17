from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.resume_parser import ResumeParser
from utils.skill_analyzer import SkillGapAnalyzer
from utils.placement_predictor import PlacementPredictor

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

parser = ResumeParser()
analyzer = SkillGapAnalyzer()
predictor = PlacementPredictor()

@app.route('/')
def home():
    return jsonify({'status': 'running', 'message': 'Smart Job Placement API', 'version': '1.0.0'})

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400

        file = request.files['resume']
        target_role = request.form.get('role', 'data_scientist')

        temp_path = os.path.join('data', 'temp_resume.pdf')
        file.save(temp_path)

        resume_text = parser.extract_text_from_pdf(temp_path)
        skills = parser.extract_skills(resume_text)
        education = parser.extract_education(resume_text)
        experience = parser.extract_experience(resume_text)

        gap_analysis = analyzer.analyze_gap(skills, target_role)

        placement_score = predictor.predict_placement({
            'skills': skills,
            'education': education,
            'experience': experience
        }, gap_analysis)

        os.remove(temp_path)

        return jsonify({
            'success': True,
            'skills': skills,
            'education': education,
            'experience': experience,
            'gap_analysis': gap_analysis,
            'placement_probability': placement_score,
            'recommendations': analyzer.get_recommendations(gap_analysis['missing_skills'])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/roles', methods=['GET'])
def get_roles():
    return jsonify({'roles': analyzer.get_available_roles()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
