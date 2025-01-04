from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import db, Admin, User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.loginAdmin'

    # Register blueprints
    from .routes import main, admin
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader

@login_manager.user_loader
def load_user(user_id):
    # Try to load user as Admin first, then as regular User
    return Admin.query.get(int(user_id)) or User.query.get(int(user_id))