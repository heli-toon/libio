
---

# Libio Library Management System

This is a simple Library Management System built using Flask, HTML, CSS, Bootstrap, and Bootstrap Icons. The project allows admins and students to manage and interact with library resources effectively.

---

## Features

1. **Homepage (Public View)**
   - Welcome message.
   - Quick links (e.g., Login, Register).
   - Library announcements or events.

2. **Login Page**
   - Authenticate users (Admin/Students).
   - Username and Password fields.
   - Role selection (Admin or Student).

3. **Dashboard (After Login)**
   - Central hub for features:
     - **Admin**:
       - Manage Books.
       - View Borrow Requests.
       - View Users.
     - **Students**:
       - Search Books.
       - View Borrowed Books.
       - Request to Borrow.

4. **Book Management (Admin Only)**
   - CRUD (Create, Read, Update, Delete) operations for books.
   - Sorting and filtering options.

5. **Search and View Books**
   - Search bar with filters (title, author, genre, etc.).
   - View book details (availability, description, etc.).

6. **About Page**
   - Library information:
     - History of the library.
     - Contact details.

7. **Error Pages**
    - Custom 404 (Page Not Found) and 500 (Server Error) pages.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- Virtual Environment (optional but recommended)
- Flask and required dependencies (listed in `requirements.txt`)

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/heli-toon/libio.git
   cd libio
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python main.py
   ```

4. Open your browser and visit:
   ```
   http://127.0.0.1:5000
   ```

---

## Deployment

### Hosting on Railway
1. Push the project to a GitHub repository.
2. Link your GitHub repository to [Railway](https://railway.app/).
3. Ensure you have a `requirements.txt` and a `Procfile`:
   - `requirements.txt`:
     ```
     Flask==2.3.2
     Gunicorn==20.1.0
     ```
   - `Procfile`:
     ```
     web: gunicorn main:app
     ```
4. Deploy the project and get your live URL.

---

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap, Bootstrap Icons
- **Hosting**: Railway
- **Font**: Roboto

---

## Customization
- To change primary colors, update the CSS file located at `app/static/css/main.css`.
- Add or modify routes in `app/routes.py`.

---

## License
This project is open-source and free to use. Modify and adapt as needed!

---

Let me know if you want further customization for the README or any other help!