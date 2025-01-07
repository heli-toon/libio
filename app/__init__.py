from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Admin, User
from flask_login import LoginManager
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Define and set the upload folder path
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads', 'books')

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .routes import main, admin
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id)) or User.query.get(int(user_id))