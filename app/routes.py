from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.models import db, Admin, Book, User

# Blueprint definitions
main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# Custom Decorators
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Admin):
            flash("Access restricted to administrators only!", "danger")
            return redirect(url_for("admin.loginAdmin"))
        return func(*args, **kwargs)
    return decorated_view

def user_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, User):
            flash("Access restricted to users only!", "danger")
            return redirect(url_for("main.login"))
        return func(*args, **kwargs)
    return decorated_view

# Admin Login
@admin.route('/login', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        
        # Validate admin credentials
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        
        # Show error message for invalid credentials
        flash('Invalid admin credentials.', 'danger')
        return redirect(url_for('admin.loginAdmin'))  # Reload login page
    
    return render_template('admin_login.html', title="Admin Login")


# User Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # Validate user credentials
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.userhome'))
        
        # Show error message for invalid credentials
        flash('Invalid user credentials.', 'danger')
        return redirect(url_for('main.login'))  # Reload login page
    
    return render_template('login.html', title="User Login")


# Logout
@main.route('/logout')
@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Admin Dashboard (protected)
@admin.route('/dashboard')
@admin_required
def dashboard():
    books = Book.query.all()
    user_count = User.query.count()
    book_count = Book.query.count()
    return render_template('dashboard.html', title="Admin Dashboard", books=books, user_count=user_count, book_count=book_count)

# User Home Page (protected)
@main.route('/home')
@user_required
def userhome():
    books = Book.query.all()
    return render_template('home.html', title="User Home", books=books)

# Public Home
@main.route('/')
def home():
    return render_template('index.html', title="Home")

# Add Book (admin only)
@admin.route('/add-book', methods=['POST'])
@admin_required
def add_book():
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    description = request.form['description']
    copies_available = int(request.form['copies_available'])

    new_book = Book(
        title=title,
        author=author,
        genre=genre,
        description=description,
        copies_available=copies_available,
    )
    db.session.add(new_book)
    db.session.commit()
    flash('Book added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Edit Book (admin only)
@admin.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.description = request.form['description']
        book.copies_available = int(request.form['copies_available'])
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_book.html', book=book)

# Delete Book (admin only)
@admin.route('/delete-book/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Search Books (admin only)
@admin.route('/search-books', methods=['GET'])
@admin_required
def search_books():
    query = request.args.get('query', '')
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) |
        (Book.author.ilike(f"%{query}%")) |
        (Book.genre.ilike(f"%{query}%"))
    ).all()
    user_count = User.query.count()
    book_count = Book.query.count()
    return render_template('dashboard.html', books=books, user_count=user_count, book_count=book_count)

# User Signup
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.signup'))

        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Signup successful! Welcome to the platform.', 'success')
        return redirect(url_for('main.userhome'))

    return render_template('signup.html', title="Signup")
