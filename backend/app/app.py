from flask import Flask, request, Response
from flask_cors import CORS

from openai import OpenAI
import tempfile

from adapters.WhisperService import WhisperService
from adapters.TextToSpeech import TextToSpeech

app = Flask(__name__)
app.config.from_pyfile('settings.py')
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return 'No audio file part', 400

    audio_file = request.files['audio']

    if audio_file.filename == '':
        return 'No selected audio file', 400

    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
        temp_file.write(audio_file.read())

    whisper = WhisperService(OpenAI())
    transcribed_text = whisper.get_text_from_path(temp_file.name)
    textToSpeech = TextToSpeech(OpenAI())
    audio_chunks = textToSpeech.get_speech_from_text(transcribed_text)
    return Response(audio_chunks, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True)
