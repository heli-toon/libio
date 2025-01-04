from app import db, create_app  # Import your app factory if you're using one
from app.models import Admin
from werkzeug.security import generate_password_hash

# Add test data function
def add_test_data():
    admin = Admin(
        username="admin",
        email="admin@example.com",  # Provide an email value
        password_hash=generate_password_hash("adminpassword", method='scrypt')
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user added successfully!")

# Main block
if __name__ == "__main__":
    app = create_app()  # Call your app factory if applicable
    with app.app_context():  # Push the app context
        add_test_data()
