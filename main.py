from app import create_app, db  # Import your app factory and database setup
from app.models import Admin  # Import your Admin model
from werkzeug.security import generate_password_hash

# Function to ensure test data exists
def ensure_test_data():
    # Check if the admin user already exists
    existing_admin = Admin.query.filter_by(username="admin").first()
    if not existing_admin:
        # Add the admin user if it doesn't exist
        admin = Admin(
            username="admin",
            email="admin@example.com",  # Ensure this matches your model
            password_hash=generate_password_hash("adminpassword", method="pbkdf2:sha256")
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user added successfully!")
    else:
        print("Admin user already exists. No changes made.")

app = create_app()

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    # Add test data at startup
    with app.app_context():  # Push the app context for database operations
        ensure_test_data()
    # Run the app
    app.run(debug=True)
