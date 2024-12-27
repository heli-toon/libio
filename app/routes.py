from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Admin, Book

main = Blueprint('main', __name__)

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', title="Login")

# Logout route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# Dashboard (protected route)
@main.route('/dashboard')
@login_required
def dashboard():
    books = Book.query.all()  # Fetch all books
    return render_template('dashboard.html', title="Dashboard", books=books)

@main.route('/')
def home():
    return render_template('index.html', title="home")

@main.route('/add-book', methods=['POST'])
def add_book():
    try:
        title = request.form['title']
        author = request.form['author']

        # Create a new book object
        new_book = Book(
            title=title,
            author=author,)

        db.session.add(new_book)
        db.session.commit()

        flash("Book added successfully!", "success")
        return redirect(url_for('main.dashboard'))
    except KeyError as e:
        flash(f'Missing field: {e.args[0]}', 'danger')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard'))


@main.route('/search-books', methods=['GET'])
def search_books():
    query = request.args.get('query')
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) |
        (Book.author.ilike(f"%{query}%")) |
        (Book.genre.ilike(f"%{query}%"))
    ).all()
    return render_template('dashboard.html', books=books)

@main.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        db.session.commit()
        flash("Book updated successfully!", "success")
        return redirect(url_for('main.dashboard'))
    return render_template('edit_book.html', book=book)

@main.route('/delete-book/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully!", "success")
    return redirect(url_for('main.dashboard'))