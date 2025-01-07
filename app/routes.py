from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app.models import db, Admin, Book, User, BorrowRequest
import os
from werkzeug.utils import secure_filename

# Blueprint definitions
main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

from flask import current_app

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
@main.route('/home', methods=['GET'])
@user_required
def userhome():
    query = request.args.get('query', '')
    # Filter books based on the search query
    if query:
        books = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) |
            (Book.author.ilike(f"%{query}%")) |
            (Book.genre.ilike(f"%{query}%"))
        ).all()
    else:
        books = Book.query.all()
    return render_template('home.html', title="User Home", books=books, query=query)

# Public Home
@main.route('/')
def home():
    return render_template('index.html', title="Home")

# Add Book (admin only)
@admin.route('/add-book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']
        copies_available = int(request.form['copies_available'])
        
        # Handle image upload
        file = request.files.get('book_cover')
        image_url = None
        if file:
            try:
                upload_folder = os.path.join(current_app.root_path, 'static/uploads/books')
                os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                image_url = f'static/uploads/books/{filename}'  # Relative path for accessing the file
            except Exception as e:
                flash(f"Image upload failed: {e}", "danger")
                return redirect(url_for('admin.dashboard'))

        # Create a new book
        new_book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
            copies_available=copies_available,
            image_url=image_url,
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_book.html', title="Add Book")


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
        # Handle optional image upload
        file = request.files.get('book_cover')
        if file:
            try:
                upload_folder = os.path.join(current_app.root_path, 'static/uploads/books')
                os.makedirs(upload_folder, exist_ok=True)  # Ensure the directory exists
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                book.image_url = f'static/uploads/books/{filename}'  # Update image URL
            except Exception as e:
                flash(f"Image upload failed: {e}", "danger")
                return redirect(url_for('admin.edit_book', book_id=book_id))

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_book.html', book=book, title="Edit Book")

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

# Add User (admin only)
@admin.route('/add-user', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('admin.add_user'))

        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('admin.user_management'))
    return render_template('add_user.html', title="Add User")

# Edit User (admin only)
@admin.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        password = request.form['password']
        if password:
            user.set_password(password)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.user_management'))
    return render_template('edit_user.html', user=user, title="Edit User")

# Delete User (admin only)
@admin.route('/delete-user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.user_management'))

# User Management (admin only)
@admin.route('/user-management')
@admin_required
def user_management():
    users = User.query.all()
    return render_template('user_management.html', users=users, title="User Management")

@main.route('/request_borrow/<int:book_id>', methods=['POST'])
@login_required
def request_borrow(book_id):
    book = Book.query.get(book_id)
    if book and book.copies_available > 0:
        borrower_name = request.form.get('borrower_name')
        new_request = BorrowRequest(book_id=book_id, borrower_name=borrower_name)
        db.session.add(new_request)
        book.copies_available -= 1  # Reduce the number of copies available
        db.session.commit()
        flash('Borrow request submitted!', 'success')
    else:
        flash('Sorry, this book is currently unavailable.', 'danger')
    return redirect(url_for('main.userhome'))

@admin.route('/approve_request/<int:request_id>')
@admin_required
def approve_request(request_id):
    # Logic to approve the borrow request
    borrow_request = BorrowRequest.query.get(request_id)
    if borrow_request:
        borrow_request.status = 'Approved'
        db.session.commit()
    return redirect(url_for('admin.manage_borrow_requests'))

@admin.route('/reject_request/<int:request_id>')
@admin_required
def reject_request(request_id):
    # Logic to reject the borrow request
    borrow_request = BorrowRequest.query.get(request_id)
    if borrow_request:
        borrow_request.status = 'Rejected'
        db.session.commit()
    return redirect(url_for('admin.manage_borrow_requests'))

@admin.route('/manage-borrow-requests')
@admin_required
def manage_borrow_requests():
    borrow_requests = BorrowRequest.query.all()
    return render_template('manage_borrow_requests.html', borrow_requests=borrow_requests)
