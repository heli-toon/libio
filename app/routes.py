from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html', title="home")

@main.route('/login')
def login():
    return render_template('login.html', title="login")

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title="dashboard")