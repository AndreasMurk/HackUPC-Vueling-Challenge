from pathlib import Path


class TextToSpeech:
    def __init__(self, client):
        self.client = client

    def save_speech_from_text(self, text: str):
        return self.get_speech_from_text(text)

    def get_speech_from_text(self, text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content
