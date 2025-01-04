from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Admin, Book, User

main = Blueprint('main', __name__)
admin = Blueprint('admin', __name__)

# Admin Login
# Admin Login
@admin.route('/login', methods=['GET', 'POST'])
def loginAdmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid admin credentials.', 'danger')
    return render_template('admin_login.html', title="Admin Login")

# User Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid user credentials.', 'danger')
    return render_template('login.html', title="User Login")


# Logout
@main.route('/logout')
@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Dashboard (protected)
@admin.route('/dashboard')
@login_required
def dashboard():
    books = Book.query.all()
    return render_template('dashboard.html', title="Dashboard", books=books)

# Home
@main.route('/')
def home():
    return render_template('index.html', title="Home")

# Add Book
@admin.route('/add-book', methods=['POST'])
@login_required
def add_book():
    if current_user.is_anonymous or current_user.__class__ != Admin:
        flash('Only admins can add books.', 'danger')
        return redirect(url_for('admin.dashboard'))

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

# Edit Book
@admin.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.description = request.form['description']
        book.copies_available = request.form['copies_available']
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_book.html', book=book)

# Delete Book
@admin.route('/delete-book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Search Books
@admin.route('/search-books', methods=['GET'])
@login_required
def search_books():
    query = request.args.get('query', '')
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) |
        (Book.author.ilike(f"%{query}%")) |
        (Book.genre.ilike(f"%{query}%"))
    ).all()
    return render_template('dashboard.html', books=books)

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
        return redirect(url_for('main.home'))

    return render_template('signup.html', title="Signup")
