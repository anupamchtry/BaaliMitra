from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Register blueprints
    from app.routes import api_bp
    from app.forum import forum_bp
    from app.equipment_store import equipment_bp
    
    app.register_blueprint(api_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(equipment_bp)
    
    # Route for crop recommendation page
    @app.route('/crop-recommendation')
    def crop_recommendation():
        return render_template('crop-recommendation.html')
    
    # Route for disease detection page
    @app.route('/disease-detection')
    def disease_detection():
        return render_template('disease-detection.html')
    
    # Routes handled by blueprints - no need for separate routes here
    
    # Home route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

# Create an app instance
app = create_app()