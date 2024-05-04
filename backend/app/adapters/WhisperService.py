from openai import OpenAI

class WhisperService:
    def __init__(self, client=OpenAI):
        self.client = client()

    def get_text(path):
        audio_file = open(path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        return transcription
