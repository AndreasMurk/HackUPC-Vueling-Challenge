from openai import OpenAI
client = OpenAI()

audio_file = open("./garbage/laia.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)

print(transcription.text)

class WhisperService:
    def __init__(self):

    def get_text
