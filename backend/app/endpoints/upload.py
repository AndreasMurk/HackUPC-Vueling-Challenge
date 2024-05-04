from flask import Blueprint, request
from flask_uploads import UploadSet, configure_uploads, AUDIO

# Create a blueprint
upload_bp = Blueprint('upload', __name__)

# Configure Flask-Uploads
audio_files = UploadSet('audio', AUDIO)

# Configure upload destination and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'}

# Configure Flask-Uploads
configure_uploads(upload_bp, (audio_files,))

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and audio_files.extension_allowed(file.filename) and file.content_length <= 25 * 1024 * 1024:
        # Save the file
        filename = audio_files.save(file)
        return 'File uploaded successfully'
    else:
        return 'Invalid file or file size exceeds 25MB'
