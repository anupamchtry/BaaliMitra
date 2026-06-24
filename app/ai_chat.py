"""
AI Chat functionality for disease explanation using Gemini API
"""
import google.generativeai as genai
import os
import traceback

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyAims0-oZd6WQkQmiincklCDpGacIaDsSw"

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize model - using models/gemini-1.5-flash-latest for v1beta compatibility
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    print("[INFO] Gemini API initialized successfully with gemini-1.5-flash-latest")
except Exception as e:
    print(f"[ERROR] Failed to initialize Gemini API: {str(e)}")
    traceback.print_exc()
    model = None

# System prompt template
SYSTEM_PROMPT = """You are an agricultural expert assistant for BaaliMitra, helping farmers understand crop diseases.

Current Disease Context:
- Disease Name: {disease_name}
- Crop Type: {crop_type}
- Symptoms: {symptoms}
- Treatment Available: {treatment}

Your Role:
1. Explain disease information in SIMPLE, FARMER-FRIENDLY language (avoid complex terms)
2. Answer ONLY questions related to THIS disease, its symptoms, treatment, or prevention
3. Be encouraging and supportive to farmers
4. Give practical, actionable advice
5. If asked about unrelated topics, politely redirect: "I can only help with questions about {disease_name}. Please ask about symptoms, treatment, or prevention."

Important Guidelines:
- Use simple words (like explaining to a friend)
- Give step-by-step instructions when needed
- Mention affordable/local treatments when possible
- Keep responses concise (2-3 short paragraphs max)
"""

def is_relevant_question(question, disease_name):
    """Check if question is relevant to the disease topic"""
    question_lower = question.lower()
    disease_lower = disease_name.lower()
    
    # Disease-related keywords
    relevant_keywords = [
        disease_lower.split()[0] if disease_lower else "",
        "symptom", "treatment", "cure", "prevent", "spray",
        "fungicide", "disease", "infection", "spread",
        "damage", "crop", "plant", "leaf", "medicine",
        "organic", "chemical", "how", "what", "when", "why"
    ]
    
    # Check if any relevant keyword is present
    is_relevant = any(keyword in question_lower for keyword in relevant_keywords if keyword)
    
    # Check for obviously off-topic
    off_topic_keywords = ["weather", "politics", "movie", "song", "game", "sports", 
                          "news", "celebrity", "recipe", "car", "phone"]
    is_off_topic = any(keyword in question_lower for keyword in off_topic_keywords)
    
    return is_relevant and not is_off_topic

def generate_initial_message(disease_info):
    """Generate initial AI greeting about the disease"""
    disease_name = disease_info.get('disease_name', 'Unknown')
    crop_type = disease_info.get('crop_type', 'plant')
    
    if model is None:
        return f"Hello! I detected {disease_name} on your {crop_type}. I'm here to help you understand and treat this disease. What would you like to know?"
    
    prompt = f"""
    A farmer just discovered {disease_name} on their {crop_type}. 
    Write a brief, friendly greeting (2-3 sentences) that:
    1. Acknowledges the disease detection
    2. Reassures the farmer that treatment is available
    3. Offers to answer their questions
    
    Keep it simple and encouraging!
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[ERROR] Gemini API error in initial message: {str(e)}")
        traceback.print_exc()
        return f"Hello! I detected {disease_name} on your {crop_type}. Don't worry, I'm here to help you understand and treat this disease. What would you like to know?"

def chat_with_ai(disease_info, user_question, is_initial=False):
    """
    Main chat function
    
    Args:
        disease_info: dict with disease details (disease_name, crop_type, symptoms, treatment)
        user_question: farmer's question (string)
        is_initial: if True, generate initial greeting
    
    Returns:
        dict with 'answer' and 'is_off_topic' flag
    """
    print(f"[DEBUG] chat_with_ai called - is_initial: {is_initial}")
    print(f"[DEBUG] disease_info: {disease_info}")
    print(f"[DEBUG] user_question: {user_question}")
    print(f"[DEBUG] model status: {'initialized' if model else 'NOT INITIALIZED'}")
    
    # Generate initial greeting
    if is_initial:
        return {
            'answer': generate_initial_message(disease_info),
            'is_off_topic': False
        }
    
    # Check if question is relevant
    if not is_relevant_question(user_question, disease_info.get('disease_name', '')):
        return {
            'answer': f"I can only help with questions about {disease_info.get('disease_name', 'this disease')}. Please ask about symptoms, treatment, prevention, or how to care for your crop.",
            'is_off_topic': True
        }
    
    # Build full prompt
    full_prompt = SYSTEM_PROMPT.format(
        disease_name=disease_info.get('disease_name', 'Unknown'),
        crop_type=disease_info.get('crop_type', 'plant'),
        symptoms=disease_info.get('symptoms', 'Not available'),
        treatment=disease_info.get('treatment', 'Consult an expert')
    )
    
    full_prompt += f"\n\nFarmer's Question: {user_question}\n\nYour Response:"
    
    try:
        print(f"[DEBUG] Sending prompt to Gemini API...")
        response = model.generate_content(full_prompt)
        print(f"[DEBUG] Received response from Gemini API")
        return {
            'answer': response.text,
            'is_off_topic': False
        }
    except Exception as e:
        print(f"[ERROR] Error in AI chat: {str(e)}")
        print("[ERROR] Full traceback:")
        traceback.print_exc()
        return {
            'answer': "I'm having trouble connecting right now. Please try asking your question again.",
            'is_off_topic': False
        }

# Disease information templates (you can expand this based on your disease detection results)
DISEASE_INFO_TEMPLATES = {
    'Potato Late Blight': {
        'symptoms': 'Dark brown spots on leaves with yellow borders, white fungal growth on leaf undersides in humid conditions, rapid spread in wet weather',
        'treatment': 'Remove infected plants immediately, apply copper-based fungicide or chlorothalonil, improve air circulation, avoid overhead watering'
    },
    'Tomato Early Blight': {
        'symptoms': 'Dark concentric spots on older leaves, yellowing around spots, leaf drop, affects fruit quality',
        'treatment': 'Remove affected leaves, apply fungicide with chlorothalonil or copper, mulch soil, practice crop rotation'
    },
    'Rice Leaf Blast': {
        'symptoms': 'Diamond-shaped lesions on leaves, gray centers with brown borders, can affect stems and grain',
        'treatment': 'Apply fungicides like tricyclazole, maintain proper water management, use resistant varieties'
    }
}

def get_disease_context(disease_name, crop_type=''):
    """Get disease information for context"""
    # Check if we have template
    if disease_name in DISEASE_INFO_TEMPLATES:
        template = DISEASE_INFO_TEMPLATES[disease_name]
        return {
            'disease_name': disease_name,
            'crop_type': crop_type or disease_name.split()[0],
            'symptoms': template['symptoms'],
            'treatment': template['treatment']
        }
    
    # Generic fallback
    return {
        'disease_name': disease_name,
        'crop_type': crop_type or 'plant',
        'symptoms': 'Visible disease symptoms detected on the plant',
        'treatment': 'Consult agricultural expert for specific treatment recommendations'
    }
