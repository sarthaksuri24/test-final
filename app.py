from flask import Flask, request, render_template, send_file
import os
import shutil
import face_recognition
import zipfile
import time
from mega import Mega

app = Flask(__name__)

mega = Mega()

# Replace these with your Mega credentials
MEGA_EMAIL = '8esarthaksuri+1234@gmail.com'
MEGA_PASSWORD = 'kcis@school'

def login_to_mega():
    m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    return m

def download_from_mega(file_name, output_folder):
    m = login_to_mega()
    file = m.find(file_name)
    if file:
        m.download(file, output_folder)

def extract_face_encodings(image_path):

    """
    Extracts face encodings from the given image.

    Args:
    - image_path (str): Path to the image file.

    Returns:
    - List of numpy arrays representing face encodings.
    """
    # Load the image
    face_image = face_recognition.load_image_file(image_path)

    # Extract face encodings
    face_encodings = face_recognition.face_encodings(face_image)
    
    return face_encodings

def compare_faces(input_image, database_folder, output_folder):
    """
    Compares faces in the input image with faces in the database folder.

    Args:
    - input_image (str): Path to the input image file.
    - database_folder (str): Path to the folder containing database images.
    - output_folder (str): Path to the folder where matched images will be saved.

    Returns:
    - List of matches for the input image.
    """
    
    matches = []

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract encodings of faces in input image
    input_face_encodings = extract_face_encodings(input_image)

    # Iterate over database images
    for filename in os.listdir(database_folder):
        # Extract encodings of faces in database image
        database_image_path = os.path.join(database_folder, filename)
        database_face_encodings = extract_face_encodings(database_image_path)

        # Compare face encodings between input image and database image
        for input_encoding in input_face_encodings:
            for database_encoding in database_face_encodings:
                # Compare the current pair of encodings
                match = face_recognition.compare_faces([input_encoding], database_encoding)
                if match[0]:
                    # Copy the matched image to the output folder
                    shutil.copy(database_image_path, output_folder)
                matches.append(match[0])  # Append the match result to the list

    return matches

# Your existing route for the Flask web app

# Add a new route for downloading images from Mega and providing as a zip file
@app.route('/download_faces', methods=['GET'])
def download_faces():
    zip_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'matched_images.zip')

    # Download images from Mega
    download_from_mega('your_file_name.jpg', app.config['OUTPUT_FOLDER'])  # Replace 'your_file_name.jpg' with actual filename

    # Create a zip file
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, dirs, files in os.walk(app.config['OUTPUT_FOLDER']):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):  # Only add image files
                    zipf.write(os.path.join(root, file), file)

    # Provide zip file as downloadable link
    return send_file(zip_file_path, as_attachment=True)

# Your existing code for running the Flask app

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['DATABASE_FOLDER'] = "database"
    app.config['OUTPUT_FOLDER'] = 'matched_images'
    app.run(debug=True)
