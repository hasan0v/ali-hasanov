# filepath: c:\Users\alien\Desktop\Test Projects\Port-1\app\__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_caching import Cache
from datetime import datetime
import os

login_manager = LoginManager()
csrf = CSRFProtect()
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    csrf.init_app(app)
    cache.init_app(app)
    
    # Import and configure user loader
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.get_by_id(int(user_id))
        except:
            return None
    
    # Add context processor to make datetime available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    # Initialize database tables
    from .models import init_db
    with app.app_context():
        init_db()
    
    return app
