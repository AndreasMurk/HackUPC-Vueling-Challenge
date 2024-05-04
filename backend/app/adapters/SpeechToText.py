from pathlib import Path


class SpeechToText:
    def __init__(self, client):
        self.client = client
        self.speech_file_path = Path(__file__).parent / "speech.mp3"

    def save_speech_from_text(self, text: str):
        return self.get_speech_from_text(text)

    def get_speech_from_text(self, text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(self.speech_file_path)
