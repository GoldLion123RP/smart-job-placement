import numpy as np

class PlacementPredictor:
    def __init__(self):
        pass

    def predict_placement(self, features, gap_analysis=None):
        skill_count = len(features['skills']['detected'])
        experience = features['experience']
        education_score = len(features['education']) * 10

        # Base score from resume features
        base_score = (min(skill_count, 15) * 3) + (min(experience, 10) * 5) + min(education_score, 30)
        base_score = min(base_score / 100, 0.6)  # max 60% from resume alone

        # Boost from skill gap analysis
        if gap_analysis and 'skill_coverage' in gap_analysis:
            coverage = gap_analysis['skill_coverage'] / 100
            match = gap_analysis['match_score'] / 100
            gap_boost = (coverage * 0.25) + (match * 0.15)
        else:
            gap_boost = 0

        probability = base_score + gap_boost
        probability = round(min(max(probability, 0.05), 0.92), 4)

        if probability > 0.75:
            confidence = 'High'
        elif probability > 0.50:
            confidence = 'Medium'
        else:
            confidence = 'Low'

        return {
            'probability': round(probability * 100, 2),
            'confidence': confidence
        }
