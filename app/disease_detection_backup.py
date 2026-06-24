"""
Disease Detection Module for BaaliMitra
Handles the disease detection workflow with multiple models
"""
import os
import numpy as np
from PIL import Image
import json
from typing import Optional, Dict, Any, Tuple

# Lazy import TensorFlow to avoid loading issues
tf = None

def load_tensorflow():
    """Lazy load TensorFlow when needed"""
    global tf
    if tf is None:
        try:
            import tensorflow as tf_module
            tf = tf_module
            print("[INFO] TensorFlow loaded successfully")
            return True
        except Exception as e:
            print(f"[WARNING] Could not load TensorFlow: {e}")
            tf = None
            return False
    return True

class DiseaseDetector:
    """Disease Detection System with multi-model workflow"""
    
    def __init__(self):
        self.models_dir = "models"
        self.models = {}
        self.model_loaded = False
        
        # Confidence thresholds for each model
        self.confidence_thresholds = {
            "leaf_detector": 0.7,      # 70% confidence for leaf detection
            "species_detector": 0.6,   # 60% confidence for species detection
            "potato_disease": 0.6,     # 60% confidence for potato disease detection
            "rice_disease": 0.6,       # 60% confidence for rice disease detection
            "tomato_disease": 0.6      # 60% confidence for tomato disease detection
        }
        
        # Disease information database
        self.disease_info = {
            # Potato diseases
            "potato_early_blight": {
                "name": "Early Blight",
                "symptoms": "Dark brown spots with concentric rings on leaves",
                "treatment": "Apply fungicide containing chlorothalonil or mancozeb",
                "prevention": "Ensure good air circulation, avoid overhead watering"
            },
            "potato_late_blight": {
                "name": "Late Blight", 
                "symptoms": "Water-soaked spots on leaves, white mold on leaf undersides",
                "treatment": "Apply copper-based fungicides immediately",
                "prevention": "Plant resistant varieties, ensure good drainage"
            },
            "potato_healthy": {
                "name": "Healthy Potato",
                "symptoms": "No disease symptoms visible",
                "treatment": "No treatment needed",
                "prevention": "Maintain good agricultural practices"
            },
            
            # Rice diseases
            "rice_blast": {
                "name": "Rice Blast",
                "symptoms": "Lesions on leaves, stems, and panicles",
                "treatment": "Apply tricyclazole or propiconazole fungicides",
                "prevention": "Use resistant varieties, manage nitrogen fertilization"
            },
            "rice_brown_spot": {
                "name": "Brown Spot",
                "symptoms": "Brown oval spots on leaves and grains",
                "treatment": "Apply mancozeb or copper oxychloride",
                "prevention": "Ensure balanced nutrition, avoid water stress"
            },
            "rice_bacterial_blight": {
                "name": "Bacterial Blight",
                "symptoms": "Water-soaked lesions on leaf edges, turning yellow then brown",
                "treatment": "Apply copper-based bactericides, remove infected plants",
                "prevention": "Use certified disease-free seeds, avoid overhead irrigation"
            },
            "rice_leaf_smut": {
                "name": "Leaf Smut",
                "symptoms": "Black powdery spores on leaves and leaf sheaths",
                "treatment": "Apply systemic fungicides containing carbendazim",
                "prevention": "Use resistant varieties, maintain field hygiene"
            },
            "rice_healthy": {
                "name": "Healthy Rice",
                "symptoms": "No disease symptoms visible", 
                "treatment": "No treatment needed",
                "prevention": "Continue good crop management"
            },
            
            # Tomato diseases
            "tomato_bacterial_spot": {
                "name": "Bacterial Spot",
                "symptoms": "Small dark spots with yellow halos on leaves",
                "treatment": "Apply copper-based bactericides",
                "prevention": "Use disease-free seeds, avoid overhead watering"
            },
            "tomato_early_blight": {
                "name": "Early Blight",
                "symptoms": "Dark spots with concentric rings on older leaves",
                "treatment": "Apply chlorothalonil or copper-based fungicides",
                "prevention": "Improve air circulation, avoid wetting leaves"
            },
            "tomato_late_blight": {
                "name": "Late Blight",
                "symptoms": "Water-soaked lesions on leaves and fruits",
                "treatment": "Apply metalaxyl or dimethomorph fungicides",
                "prevention": "Use resistant varieties, ensure good ventilation"
            },
            "tomato_leaf_mold": {
                "name": "Leaf Mold",
                "symptoms": "Yellow spots on upper leaf surface, fuzzy growth below",
                "treatment": "Apply fungicides containing chlorothalonil",
                "prevention": "Reduce humidity, improve air circulation"
            },
            "tomato_septoria_leaf_spot": {
                "name": "Septoria Leaf Spot",
                "symptoms": "Small circular spots with dark borders and light centers",
                "treatment": "Apply fungicides containing chlorothalonil or copper",
                "prevention": "Mulch plants, avoid overhead watering"
            },
            "tomato_spider_mites": {
                "name": "Spider Mites",
                "symptoms": "Tiny yellow or white spots on leaves, fine webbing",
                "treatment": "Apply miticides or insecticidal soap",
                "prevention": "Maintain proper humidity, regular monitoring"
            },
            "tomato_target_spot": {
                "name": "Target Spot",
                "symptoms": "Dark spots with concentric rings resembling targets",
                "treatment": "Apply fungicides containing azoxystrobin",
                "prevention": "Improve air circulation, remove plant debris"
            },
            "tomato_yellow_leaf_curl_virus": {
                "name": "Yellow Leaf Curl Virus",
                "symptoms": "Upward curling and yellowing of leaves",
                "treatment": "Remove infected plants, control whitefly vectors",
                "prevention": "Use virus-resistant varieties, control whiteflies"
            },
            "tomato_mosaic_virus": {
                "name": "Mosaic Virus",
                "symptoms": "Mottled light and dark green patches on leaves",
                "treatment": "Remove infected plants immediately",
                "prevention": "Use virus-free seeds, sanitize tools"
            },
            "tomato_healthy": {
                "name": "Healthy Tomato",
                "symptoms": "No disease symptoms visible",
                "treatment": "No treatment needed", 
                "prevention": "Maintain proper care practices"
            }
        }
        
        # Crop species that models can detect
        self.supported_crops = {
            "potato": "Potato",
            "rice": "Rice", 
            "tomato": "Tomato"
        }
        
        # Other crops that plant species model might detect
        self.other_crops = {
            "corn": "Corn/Maize",
            "wheat": "Wheat",
            "soybean": "Soybean",
            "cotton": "Cotton",
            "sugarcane": "Sugarcane",
            "pepper": "Pepper",
            "grape": "Grape",
            "apple": "Apple",
            "strawberry": "Strawberry"
        }
    
    def load_models(self):
        """Load all required models"""
        if not load_tensorflow():
            print("[WARNING] TensorFlow not available. Using fallback mode.")
            return False
            
        try:
            # Define custom object to handle 'groups' argument issue in older TF versions
            class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
                def __init__(self, **kwargs):
                    if 'groups' in kwargs:
                        kwargs.pop('groups')
                    super().__init__(**kwargs)

            model_files = {
                "leaf_detector": "leaf_nonleaf_detector.h5",
                "species_detector": "plant_species_model.h5", 
                "potato_disease": "potato_model.h5",
                "rice_disease": "rice_model.h5",
                "tomato_disease": "tomato_model.h5"
            }
            
            loaded_count = 0
            for model_name, filename in model_files.items():
                model_path = os.path.join(self.models_dir, filename)
                if os.path.exists(model_path):
                    try:
                        # Try loading with custom object scope to handle compatibility issues
                        custom_objects = {'DepthwiseConv2D': CustomDepthwiseConv2D}
                        self.models[model_name] = tf.keras.models.load_model(
                            model_path,
                            custom_objects=custom_objects,
                            compile=False  # Skip compilation to avoid version conflicts
                        )
                        print(f"[INFO] Loaded {model_name} model")
                        loaded_count += 1
                    except Exception as e:
                        print(f"[WARNING] Could not load {model_name}: {e}")
                        # Try loading without compile and with safe mode
                        try:
                            import h5py
                            # For models with compatibility issues, try loading just the weights
                            print(f"[INFO] Attempting alternative loading for {model_name}")
                            self.models[model_name] = tf.keras.models.load_model(
                                model_path,
                                custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D},
                                compile=False
                            )
                            print(f"[INFO] Loaded {model_name} model with alternative method")
                            loaded_count += 1
                        except Exception as e2:
                            print(f"[WARNING] Alternative loading also failed for {model_name}: {e2}")
                else:
            "potato_disease": 0.6,     # 60% confidence for potato disease detection
            "rice_disease": 0.6,       # 60% confidence for rice disease detection
            "tomato_disease": 0.6      # 60% confidence for tomato disease detection
        }
        
        # Disease information database
        self.disease_info = {
            # Potato diseases
            "potato_early_blight": {
                "name": "Early Blight",
                "symptoms": "Dark brown spots with concentric rings on leaves",
                "treatment": "Apply fungicide containing chlorothalonil or mancozeb",
                "prevention": "Ensure good air circulation, avoid overhead watering"
            },
            "potato_late_blight": {
                "name": "Late Blight", 
                "symptoms": "Water-soaked spots on leaves, white mold on leaf undersides",
                "treatment": "Apply copper-based fungicides immediately",
                "prevention": "Plant resistant varieties, ensure good drainage"
            },
            "potato_healthy": {
                "name": "Healthy Potato",
                "symptoms": "No disease symptoms visible",
                "treatment": "No treatment needed",
                "prevention": "Maintain good agricultural practices"
            },
            
            # Rice diseases
            "rice_blast": {
                "name": "Rice Blast",
                "symptoms": "Lesions on leaves, stems, and panicles",
                "treatment": "Apply tricyclazole or propiconazole fungicides",
                "prevention": "Use resistant varieties, manage nitrogen fertilization"
            },
            "rice_brown_spot": {
                "name": "Brown Spot",
                "symptoms": "Brown oval spots on leaves and grains",
                "treatment": "Apply mancozeb or copper oxychloride",
                "prevention": "Ensure balanced nutrition, avoid water stress"
            },
            "rice_bacterial_blight": {
                "name": "Bacterial Blight",
                "symptoms": "Water-soaked lesions on leaf edges, turning yellow then brown",
                "treatment": "Apply copper-based bactericides, remove infected plants",
                "prevention": "Use certified disease-free seeds, avoid overhead irrigation"
            },
            "rice_leaf_smut": {
                "name": "Leaf Smut",
                "symptoms": "Black powdery spores on leaves and leaf sheaths",
                "treatment": "Apply systemic fungicides containing carbendazim",
                "prevention": "Use resistant varieties, maintain field hygiene"
            },
            "rice_healthy": {
                "name": "Healthy Rice",
                "symptoms": "No disease symptoms visible", 
                "treatment": "No treatment needed",
                "prevention": "Continue good crop management"
            },
            
            # Tomato diseases
            "tomato_bacterial_spot": {
                "name": "Bacterial Spot",
                "symptoms": "Small dark spots with yellow halos on leaves",
                "treatment": "Apply copper-based bactericides",
                "prevention": "Use disease-free seeds, avoid overhead watering"
            },
            "tomato_early_blight": {
                "name": "Early Blight",
                "symptoms": "Dark spots with concentric rings on older leaves",
                "treatment": "Apply chlorothalonil or copper-based fungicides",
                "prevention": "Improve air circulation, avoid wetting leaves"
            },
            "tomato_late_blight": {
                "name": "Late Blight",
                "symptoms": "Water-soaked lesions on leaves and fruits",
                "treatment": "Apply metalaxyl or dimethomorph fungicides",
                "prevention": "Use resistant varieties, ensure good ventilation"
            },
            "tomato_leaf_mold": {
                "name": "Leaf Mold",
                "symptoms": "Yellow spots on upper leaf surface, fuzzy growth below",
                "treatment": "Apply fungicides containing chlorothalonil",
                "prevention": "Reduce humidity, improve air circulation"
            },
            "tomato_septoria_leaf_spot": {
                "name": "Septoria Leaf Spot",
                "symptoms": "Small circular spots with dark borders and light centers",
                "treatment": "Apply fungicides containing chlorothalonil or copper",
                "prevention": "Mulch plants, avoid overhead watering"
            },
            "tomato_spider_mites": {
                "name": "Spider Mites",
                "symptoms": "Tiny yellow or white spots on leaves, fine webbing",
                "treatment": "Apply miticides or insecticidal soap",
                "prevention": "Maintain proper humidity, regular monitoring"
            },
            "tomato_target_spot": {
                "name": "Target Spot",
                "symptoms": "Dark spots with concentric rings resembling targets",
                "treatment": "Apply fungicides containing azoxystrobin",
                "prevention": "Improve air circulation, remove plant debris"
            },
            "tomato_yellow_leaf_curl_virus": {
                "name": "Yellow Leaf Curl Virus",
                "symptoms": "Upward curling and yellowing of leaves",
                "treatment": "Remove infected plants, control whitefly vectors",
                "prevention": "Use virus-resistant varieties, control whiteflies"
            },
            "tomato_mosaic_virus": {
                "name": "Mosaic Virus",
                "symptoms": "Mottled light and dark green patches on leaves",
                "treatment": "Remove infected plants immediately",
                "prevention": "Use virus-free seeds, sanitize tools"
            },
            "tomato_healthy": {
                "name": "Healthy Tomato",
                "symptoms": "No disease symptoms visible",
                "treatment": "No treatment needed", 
                "prevention": "Maintain proper care practices"
            }
        }
        
        # Crop species that models can detect
        self.supported_crops = {
            "potato": "Potato",
            "rice": "Rice", 
            "tomato": "Tomato"
        }
        
        # Other crops that plant species model might detect
        self.other_crops = {
            "corn": "Corn/Maize",
            "wheat": "Wheat",
            "soybean": "Soybean",
            "cotton": "Cotton",
            "sugarcane": "Sugarcane",
            "pepper": "Pepper",
            "grape": "Grape",
            "apple": "Apple",
            "strawberry": "Strawberry"
        }
    
    def load_models(self):
        """Load all required models"""
        if not load_tensorflow():
            print("[WARNING] TensorFlow not available. Using fallback mode.")
            return False
            
        try:
            # Define custom object to handle 'groups' argument issue in older TF versions
            class CustomDepthwiseConv2D(tf.keras.layers.DepthwiseConv2D):
                def __init__(self, **kwargs):
                    if 'groups' in kwargs:
                        kwargs.pop('groups')
                    super().__init__(**kwargs)

            model_files = {
                "leaf_detector": "leaf_nonleaf_detector.h5",
                "species_detector": "plant_species_model.h5", 
                "potato_disease": "potato_model.h5",
                "rice_disease": "rice_model.h5",
                "tomato_disease": "tomato_model.h5"
            }
            
            loaded_count = 0
            for model_name, filename in model_files.items():
                model_path = os.path.join(self.models_dir, filename)
                if os.path.exists(model_path):
                    try:
                        # Try loading with custom object scope to handle compatibility issues
                        custom_objects = {'DepthwiseConv2D': CustomDepthwiseConv2D}
                        self.models[model_name] = tf.keras.models.load_model(
                            model_path,
                            custom_objects=custom_objects,
                            compile=False  # Skip compilation to avoid version conflicts
                        )
                        print(f"[INFO] Loaded {model_name} model")
                        loaded_count += 1
                    except Exception as e:
                        print(f"[WARNING] Could not load {model_name}: {e}")
                        # Try loading without compile and with safe mode
                        try:
                            import h5py
                            # For models with compatibility issues, try loading just the weights
                            print(f"[INFO] Attempting alternative loading for {model_name}")
                            self.models[model_name] = tf.keras.models.load_model(
                                model_path,
                                custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D},
                                compile=False
                            )
                            print(f"[INFO] Loaded {model_name} model with alternative method")
                            loaded_count += 1
                        except Exception as e2:
                            print(f"[WARNING] Alternative loading also failed for {model_name}: {e2}")
                else:
                    print(f"[WARNING] Model file not found: {filename}")
            
            self.model_loaded = loaded_count > 0
            print(f"[INFO] Loaded {loaded_count}/{len(model_files)} models")
            return self.model_loaded
            
        except Exception as e:
            print(f"[ERROR] Error loading models: {e}")
            return False
    
    def preprocess_image(self, image: Image.Image, target_size: tuple = (224, 224)) -> np.ndarray:
        """Preprocess image for model prediction"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(target_size)
            
            # Convert to array and normalize
            img_array = np.array(image) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"[ERROR] Error preprocessing image: {e}")
            return None
    
    def detect_leaf(self, image: Image.Image) -> Dict[str, Any]:
        """Step 1: Detect if image contains a leaf"""
        try:
            if not self.model_loaded or "leaf_detector" not in self.models:
                return {
                    "is_leaf": True,   # Assume it's a leaf if model not available
                    "confidence": 0.5,
                    "message": "Leaf detection model not available, proceeding with plant detection"
                }
            
            img_array = self.preprocess_image(image)
            if img_array is None:
                return {"is_leaf": False, "confidence": 0.0, "message": "Could not process image"}
            
            prediction = self.models["leaf_detector"].predict(img_array, verbose=0)
            raw_confidence = float(prediction[0][0])  # Single output value
            threshold = self.confidence_thresholds["leaf_detector"]
            
            # Since your model outputs are inverted, flip the interpretation
            # If raw output is high, it means Non_Leaf; if low, it means Leaf
            is_leaf = bool(raw_confidence < (1.0 - threshold))  # Inverted logic
            confidence = 1.0 - raw_confidence  # Convert to leaf confidence for display
            
            # Determine confidence level message
            if confidence >= 0.9:
                confidence_msg = "High confidence"
            elif confidence >= 0.7:
                confidence_msg = "Good confidence"
            elif confidence >= 0.5:
                confidence_msg = "Moderate confidence"
            else:
                confidence_msg = "Low confidence"
            
            if is_leaf:
                message = f"Leaf detected ({confidence_msg})"
            else:
                if confidence < 0.3:
                    message = "No leaf detected - image may not contain plant material"
                else:
                    message = f"Uncertain leaf detection ({confidence_msg}) - please try a clearer image"
            
            return {
                "is_leaf": is_leaf,
                "confidence": confidence,
                "threshold": threshold,
                "message": message
            }
            
        except Exception as e:
            print(f"[ERROR] Error in leaf detection: {e}")
            return {
                "is_leaf": True,  # Fallback to assume leaf
                "confidence": 0.5,
                "message": f"Leaf detection failed: {str(e)}, proceeding anyway"
            }
    
    def detect_plant_species(self, image: Image.Image) -> Dict[str, Any]:
        """Step 2: Detect plant species"""
        try:
            if not self.model_loaded or "species_detector" not in self.models:
                return {
                    "species": "unknown",
                    "confidence": 0.0,
                    "message": "Plant species detection model not available - please select crop manually"
                }
            
            img_array = self.preprocess_image(image)
            if img_array is None:
                return {"species": "unknown", "confidence": 0.0, "message": "Could not process image"}
            
            prediction = self.models["species_detector"].predict(img_array, verbose=0)
            species_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][species_idx])
            
            # Species mapping based on actual training data - this needs to be verified
            # Common plant species that models are typically trained on
            # Model output shape is 9, so we limit the map to 9 items
            species_map = ["potato", "tomato", "rice", "corn", "wheat", "soybean", "cotton", "pepper", "grape"]
            
            if species_idx < len(species_map):
                species = species_map[species_idx]
            else:
                species = "unknown"
            
            return {
                "species": species,
                "confidence": confidence,
                "message": f"Detected as {species}"
            }
            
        except Exception as e:
            print(f"[ERROR] Error in species detection: {e}")
            return {
                "species": "unknown",
                "confidence": 0.0,
                "message": f"Species detection failed: {str(e)} - please select crop manually"
            }

    def detect_disease(self, image: Image.Image, species: str) -> Dict[str, Any]:
        """Step 3: Detect disease for specific crop"""
        try:
            model_key = f"{species}_disease"
            
            if not self.model_loaded or model_key not in self.models:
                return {
                    "disease": f"{species}_healthy",
                    "confidence": 0.0,
                    "message": f"Disease detection model for {species} not available"
                }
            
            img_array = self.preprocess_image(image)
            if img_array is None:
                return {"disease": "unknown", "confidence": 0.0, "message": "Could not process image"}
            
            prediction = self.models[model_key].predict(img_array, verbose=0)
            disease_idx = int(np.argmax(prediction[0]))  # Ensure Python int
            confidence = float(prediction[0][disease_idx])
            threshold = self.confidence_thresholds[model_key]
            
            # Map prediction to disease (based on actual model outputs)
            disease_maps = {
                "potato": ["potato_early_blight", "potato_late_blight", "potato_healthy"],  # 3 classes
                "rice": ["rice_blast", "rice_brown_spot", "rice_bacterial_blight", "rice_leaf_smut", "rice_healthy"],  # 5 classes  
                "tomato": ["tomato_bacterial_spot", "tomato_early_blight", "tomato_late_blight", "tomato_leaf_mold", 
                          "tomato_septoria_leaf_spot", "tomato_spider_mites", "tomato_target_spot", 
                          "tomato_yellow_leaf_curl_virus", "tomato_mosaic_virus", "tomato_healthy"]  # 10 classes
            }
            
            if species in disease_maps and disease_idx < len(disease_maps[species]):
                disease = disease_maps[species][disease_idx]
            else:
                disease = f"{species}_healthy"
            
            # Determine reliability based on confidence
            if confidence >= threshold:
                reliability = "reliable"
                message = f"Disease detection completed with good confidence"
            else:
                reliability = "uncertain"
                message = f"Disease detection completed but with low confidence - results may be unreliable"
            
            return {
                "disease": disease,
                "confidence": confidence,
                "threshold": threshold,
                "reliability": reliability,
                "message": message
            }
            
        except Exception as e:
            print(f"[ERROR] Error in disease detection: {e}")
            return {
                "disease": f"{species}_healthy",
                "confidence": 0.0,
                "message": f"Disease detection failed: {str(e)}"
            }
    
    def analyze_image(self, image_path: str, selected_crop: str = None) -> Dict[str, Any]:
        """Complete disease detection workflow"""
        try:
            # Load image
            image = Image.open(image_path)
            
            result = {
                "workflow_steps": [],
                "final_result": {},
                "success": False
            }
            
            # If specific crop is selected, skip species detection
            if selected_crop and selected_crop.lower() in self.supported_crops:
                # Step 1: Leaf detection
                leaf_result = self.detect_leaf(image)
                result["workflow_steps"].append({"step": "leaf_detection", "result": leaf_result})
                
                if not leaf_result["is_leaf"]:
                    result["final_result"] = {
                        "error": "No leaf detected in the image. Please upload an image of a plant leaf.",
                        "suggestion": "Make sure the image clearly shows a plant leaf"
                    }
                    return result
                
                # Step 2: Disease detection for selected crop
                disease_result = self.detect_disease(image, selected_crop.lower())
                result["workflow_steps"].append({"step": "disease_detection", "result": disease_result})
                
                # Get disease information
                disease_key = disease_result["disease"]
                disease_info = self.disease_info.get(disease_key, {
                    "name": "Unknown Disease",
                    "symptoms": "Could not identify specific symptoms",
                    "treatment": "Consult local agricultural expert",
                    "prevention": "Follow general plant care guidelines"
                })
                
                # Add reliability warnings if needed
                reliability_warnings = []
                
                if leaf_result["confidence"] < self.confidence_thresholds["leaf_detector"]:
                    reliability_warnings.append("Leaf detection had low confidence - image quality may affect results")
                
                if disease_result.get("reliability") == "uncertain":
                    reliability_warnings.append("Disease detection has low confidence - consider taking another photo or consulting an expert")
                
                result["final_result"] = {
                    "crop": self.supported_crops[selected_crop.lower()],
                    "disease": disease_info["name"],
                    "confidence": disease_result["confidence"],
                    "symptoms": disease_info["symptoms"],
                    "treatment": disease_info["treatment"],
                    "prevention": disease_info["prevention"],
                    "is_healthy": "healthy" in disease_key,
                    "reliability_warnings": reliability_warnings
                }
                result["success"] = True
                
            else:
                # Full workflow: leaf detection → species detection → disease detection
                
                # Step 1: Leaf detection
                leaf_result = self.detect_leaf(image)
                result["workflow_steps"].append({"step": "leaf_detection", "result": leaf_result})
                
                if not leaf_result["is_leaf"]:
                    result["final_result"] = {
                        "error": "No leaf detected in the image. Please upload an image of a plant leaf.",
                        "suggestion": "Make sure the image clearly shows a plant leaf"
                    }
                    return result
                
                # Step 2: Species detection
                species_result = self.detect_plant_species(image)
                result["workflow_steps"].append({"step": "species_detection", "result": species_result})
                
                detected_species = species_result["species"]
                
                if detected_species in self.supported_crops:
                    # Step 3: Disease detection for supported crop
                    disease_result = self.detect_disease(image, detected_species)
                    result["workflow_steps"].append({"step": "disease_detection", "result": disease_result})
                    
                    # Get disease information
                    disease_key = disease_result["disease"]
                    disease_info = self.disease_info.get(disease_key, {
                        "name": "Unknown Disease",
                        "symptoms": "Could not identify specific symptoms",
                        "treatment": "Consult local agricultural expert",
                        "prevention": "Follow general plant care guidelines"
                    })
                    
                    result["final_result"] = {
                        "crop": self.supported_crops[detected_species],
                        "disease": disease_info["name"],
                        "confidence": disease_result["confidence"],
                        "symptoms": disease_info["symptoms"],
                        "treatment": disease_info["treatment"],
                        "prevention": disease_info["prevention"],
                        "is_healthy": "healthy" in disease_key
                    }
                    result["success"] = True
                    
                elif detected_species in self.other_crops:
                    # Crop detected but no disease model available
                    result["final_result"] = {
                        "crop": self.other_crops[detected_species],
                        "message": f"No disease detection model available for {self.other_crops[detected_species]}",
                        "suggestion": "Disease detection is currently available for Potato, Rice, and Tomato only. Please select one of these crops if your plant matches.",
                        "model_available": False,
                        "detected_species": detected_species
                    }
                    result["success"] = True
                    
                else:
                    # Unknown crop or species detection failed
                    result["final_result"] = {
                        "crop": "Unknown Plant",
                        "message": "Could not identify the plant species automatically",
                        "suggestion": "Please select the crop type manually (Potato, Rice, or Tomato) to get disease detection",
                        "model_available": False,
                        "show_crop_selection": True
                    }
                    result["success"] = True
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Error in image analysis: {e}")
            return {
                "workflow_steps": [],
                "final_result": {
                    "error": f"Analysis failed: {str(e)}",
                    "suggestion": "Please try again with a different image"
                },
                "success": False
            }

# Global detector instance
_detector = None

def get_detector():
    """Get global detector instance"""
    global _detector
    if _detector is None:
        _detector = DiseaseDetector()
        _detector.load_models()
    return _detector

def analyze_plant_image(image_path: str, selected_crop: str = None) -> Dict[str, Any]:
    """Analyze plant image for disease detection"""
    detector = get_detector()
    return detector.analyze_image(image_path, selected_crop)

def load_models():
    """Load all disease detection models"""
    detector = get_detector()
    return detector.load_models()

def get_supported_crops():
    """Get list of supported crops"""
    detector = get_detector()
    return list(detector.supported_crops.values())