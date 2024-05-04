from flask import Flask, request, Response
from flask_cors import CORS

from openai import OpenAI
import tempfile

from adapters.WhisperService import WhisperService
from adapters.TextToSpeech import TextToSpeech
from adapters.Assistant import Assistant

app = Flask(__name__)
app.config.from_pyfile('settings.py')
CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})


@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"


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

    assistant = Assistant(OpenAI())
    message = assistant.receive_message(transcribed_text)
    # import pdb; pdb.set_trace()

    textToSpeech = TextToSpeech(OpenAI())
    audio_chunks = textToSpeech.get_speech_from_text(message)
    return Response(audio_chunks, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
