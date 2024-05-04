from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return 'No audio file part', 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'No selected audio file', 400

    # Save the uploaded audio file
    audio_file.save(audio_file.filename)

    return 'Audio file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
