from app import create_app
# from dotenv import load_dotenv
# import os

# load_dotenv()

# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# Cloudinary Configuration
# cloudinary.config(
#     cloud_name=os.getenv("CLOUD_NAME"),
#     api_key=os.getenv("API_KEY"),
#     api_secret=os.getenv("API_SECRET"),
#     secure=True
# )


app = create_app()


# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    app.run(debug=True)
