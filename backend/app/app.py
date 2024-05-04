from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, AUDIO

app = Flask(__name__)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'

# Limit to audio files and 25MB max
audio_files = UploadSet('audio', AUDIO)
configure_uploads(app, (audio_files,))

@app.route('/upload', methods=['POST'])
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
