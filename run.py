# Change from: from app import app
# To:
from app import app

if __name__ == '__main__':
    print("🌱 Starting BaaliMitra Flask Server...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🏠 Home Page: http://localhost:5000")
    print("🌾 Crop Recommendation: http://localhost:5000/crop-recommendation")
    print("🔍 Disease Detection: http://localhost:5000/disease-detection")
    print("💬 Forum: http://localhost:5000/forum")
    print("🛒 Equipment Store: http://localhost:5000/equipment-store")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)