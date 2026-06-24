from flask import Blueprint, request, jsonify
import os
from app.crop_recommendation import predict_crop, get_districts_and_seasons, get_seasonal_climate
from app.ai_chat import chat_with_ai, get_disease_context

# Create a blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/crop-recommendation', methods=['POST'])
def crop_recommendation_api():
    """API endpoint for crop recommendations - Enhanced version"""
    if request.method == 'POST':
        try:
            # Get JSON data from request
            data = request.get_json()
            
            # Process the data and get predictions
            response, status_code = predict_crop(data)
            
            return jsonify(response), status_code
        except Exception as e:
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid request method"}), 405

@api_bp.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for crop recommendations - Original crop-old format"""
    try:
        data = request.get_json(force=True)

        # Input flags
        include_soil = bool(data.get("include_soil", False))
        use_seasonal = bool(data.get("use_seasonal", True))

        # Process the data and get predictions
        response, status_code = predict_crop(data)
        
        if status_code == 200:
            # Return in original crop-old format
            return jsonify({
                "used": response["used"],
                "top": response["top"],
                "poly": response["poly"]
            })
        else:
            return jsonify(response), status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/districts')
def api_districts():
    """API endpoint to get available districts and seasons"""
    try:
        return jsonify(get_districts_and_seasons())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/seasonal')
def api_seasonal():
    """API endpoint to get seasonal climate data"""
    try:
        district = request.args.get("district", "")
        season = request.args.get("season", "")
        
        result = get_seasonal_climate(district, season)
        if result["ok"]:
            return jsonify(result)
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "BaaliMitra Crop Recommendation API is running"})

@api_bp.route('/api/model-info')
def model_info():
    """Get information about the ML model"""
    try:
        from app.crop_recommendation import _model, _districts, _seasons
        return jsonify({
            "model_loaded": _model is not None,
            "districts_count": len(_districts) if _districts else 0,
            "seasons": _seasons,
            "available_districts": _districts[:10] if _districts else []  # First 10 districts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/disease-detection', methods=['POST'])
def disease_detection_api():
    """API endpoint for disease detection with multi-model workflow"""
    try:
        from app.disease_detection import analyze_plant_image
        import base64
        import tempfile
        from PIL import Image
        import io
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract image data and selected crop
        image_data = data.get('image')
        selected_crop = data.get('crop_type')
        
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400
        
        # Process base64 image data
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        
        # Create temporary file for image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Process disease detection
            result = analyze_plant_image(temp_file_path, selected_crop)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
    except Exception as e:
        return jsonify({
            "success": False,
            "stage": "api_error",
            "result": {"error": str(e)},
            "message": f"❌ Server error: {str(e)}"
        }), 500

@api_bp.route('/api/crop-recommendation/districts', methods=['GET'])
def get_districts_api():
    """API endpoint to get available districts and seasons"""
    from app.crop_recommendation import get_districts_and_seasons
    try:
        data = get_districts_and_seasons()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/crop-recommendation/climate', methods=['POST'])
def get_climate_api():
    """Get climate data for specific district and season"""
    from app.crop_recommendation import get_seasonal_climate
    try:
        data = request.get_json()
        district = data.get('district')
        season = data.get('season')
        result = get_seasonal_climate(district, season)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@api_bp.route('/api/disease-detection/models-status')
def disease_models_status():
    """Get status of all disease detection models"""
    try:
        from app.disease_detection import get_detector
        detector = get_detector()
        
        model_files = {
            "leaf_detector": "leaf_nonleaf_detector.h5",
            "species_detector": "plant_species_model.h5",
            "potato_disease": "potato_model.h5",
            "rice_disease": "rice_model.h5", 
            "tomato_disease": "tomato_model.h5"
        }
        
        model_status = {}
        for model_name, filename in model_files.items():
            model_path = os.path.join("models", filename)
            model_status[model_name] = {
                "path": model_path,
                "exists": os.path.exists(model_path),
                "loaded": model_name in detector.models,
                "file_size_mb": round(os.path.getsize(model_path) / (1024*1024), 2) if os.path.exists(model_path) else 0
            }
        
        return jsonify({
            "models": model_status,
            "total_models": len(model_files),
            "loaded_models": len(detector.models),
            "supported_crops": ["potato", "rice", "tomato"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/ai-chat', methods=['POST'])
def ai_chat_api():
    """API endpoint for AI chat about diseases"""
    try:
        data = request.get_json()
        
        # Get parameters
        disease_name = data.get('disease_name', '')
        crop_type = data.get('crop_type', '')
        user_question = data.get('question', '')
        is_initial = data.get('is_initial', False)
        
        # Get disease context
        disease_info = get_disease_context(disease_name, crop_type)
        
        # Add custom symptoms/treatment if provided
        if 'symptoms' in data:
            disease_info['symptoms'] = data['symptoms']
        if 'treatment' in data:
            disease_info['treatment'] = data['treatment']
        
        # Get AI response
        response = chat_with_ai(disease_info, user_question, is_initial)
        
        return jsonify({
            "success": True,
            "answer": response['answer'],
            "is_off_topic": response['is_off_topic'],
            "disease": disease_name
        })
        
    except Exception as e:
        print(f"Error in AI chat API: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "answer": "Sorry, I'm having trouble right now. Please try again."
        }), 500