from flask import Flask, request, jsonify, send_file
import os
import base64
from io import BytesIO
import random

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Medical image prediction endpoint
    Accepts image upload and returns medical AI prediction results
    """
    try:
        # Check if image is uploaded
        if 'image' not in request.files:
            return jsonify({
                "errors": {
                    "error_code": "HTM0001",
                    "error_message": "No image file provided.",
                },
                "code": "400",
                "message": "Bad Request - Image required"
            }), 400
        
        # Read the sample.png file and encode it as base64 for response
        sample_image_path = 'sample.png'
        if os.path.exists(sample_image_path):
            with open(sample_image_path, 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
        else:
            img_base64 = None
        
        # Simulate some variation in probabilities for realism
        base_probs = {
            "lung_opacity": 0.024486106,
            "mass": 0.555674,
            "nodule": 0.787056,
            "edema": 0.00045697083,
            "atelectasis": 0.00043212515,
            "cardiomegaly": 0.002482325,
            "pleural_effusion": 0.98906904
        }
        
        # Add small random variation (±5%) to make it more realistic
        varied_probs = {}
        for condition, prob in base_probs.items():
            variation = random.uniform(-0.05, 0.05)
            new_prob = max(0.0, min(1.0, prob + (prob * variation)))
            varied_probs[condition] = new_prob
        
        # Response structure matching the required format
        response = {
            "heatmap_gradcam_api_version": "4.5.0",
            "prediction": {
                "abnormality": {
                    "lung_opacity": {
                        "prob": varied_probs["lung_opacity"],
                        "thr_conf_score": 1 if varied_probs["lung_opacity"] > 0.5 else 0,
                    },
                    "mass": {
                        "prob": varied_probs["mass"],
                        "thr_conf_score": 1 if varied_probs["mass"] > 0.5 else 0,
                    },
                    "nodule": {
                        "prob": varied_probs["nodule"],
                        "thr_conf_score": 1 if varied_probs["nodule"] > 0.5 else 0,
                    },
                    "edema": {
                        "prob": varied_probs["edema"],
                        "thr_conf_score": 1 if varied_probs["edema"] > 0.5 else 0,
                    },
                    "atelectasis": {
                        "prob": varied_probs["atelectasis"],
                        "thr_conf_score": 1 if varied_probs["atelectasis"] > 0.5 else 0,
                    },
                    "cardiomegaly": {
                        "prob": varied_probs["cardiomegaly"],
                        "thr_conf_score": 1 if varied_probs["cardiomegaly"] > 0.5 else 0,
                    },
                    "pleural_effusion": {
                        "prob": varied_probs["pleural_effusion"],
                        "thr_conf_score": 1 if varied_probs["pleural_effusion"] > 0.5 else 0,
                    },
                    "api_version": "3.1.0",
                }
            },
            "errors": {
                "error_code": "HTM0000",
                "error_message": "Abnormality conditions success response.",
            },
            "code": "200",
            "message": "Request complete and the result is available",
            "heatmap_image": img_base64
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            "errors": {
                "error_code": "HTM0500",
                "error_message": f"Internal server error: {str(e)}",
            },
            "code": "500",
            "message": "Internal Server Error"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "api_version": "4.5.0",
        "message": "Medical AI Prediction Service is running"
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "service": "Medical AI Prediction API",
        "version": "4.5.0",
        "endpoints": {
            "/predict": "POST - Medical image prediction",
            "/health": "GET - Health check",
        },
        "description": "Upload medical images to get AI-powered abnormality predictions"
    }), 200

if __name__ == '__main__':
    # Ensure sample.png exists
    if not os.path.exists('sample.png'):
        print("Warning: sample.png not found. Heatmap image will be null in responses.")
    
    app.run(debug=True, host='0.0.0.0', port=50011) 