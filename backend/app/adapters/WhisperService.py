class WhisperService:
    def __init__(self, client):
        self.client = client

    def get_text_from_path(self, path: str):
        audio_file = open(path, "rb")
        return self.get_text_from_file(audio_file)

    def get_text_from_file(self, file):
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )

        return transcription.text
