

import speech_recognition as sr


class CustomRecognizer(sr.Recognizer):
    def __init__(self, language="fr-FR"):
        super().__init__()
        self.language = language

    def recognize_sphinx(self, audio_data,*args, **kwargs):
        # Custom implementation or modifications can be added here
        return super().recognize_sphinx(audio_data, language=self.language, **kwargs)
    def recognize_google(self, audio_data,*args, **kwargs):
        # Custom implementation or modifications can be added here
        return super().recognize_google(audio_data, language=self.language, **kwargs)
    def recognize_google_cloud(self, audio_data,*args, **kwargs):
        # Custom implementation or modifications can be added here
        return super().recognize_google_cloud(audio_data, language=self.language, **kwargs)
    
    def set_language(self, language):
        self.language = language
    
    def recognize(self, audio_data, *args, **kwargs):
        audio_to_text = None
        try:
            audio_to_text = self.recognize_google(audio_data, *args, **kwargs)
        except sr.RequestError:
            try:
                audio_to_text = self.recognize_sphinx(audio_data, *args, **kwargs)
            except sr.RequestError:
                try:
                    audio_to_text = self.recognize_google_cloud(audio_data, *args, **kwargs)
                except sr.RequestError:
                    audio_to_text = None
            else:
                return audio_to_text

        else:
            return audio_to_text
        
        if audio_to_text is None:
            raise sr.RequestError("All recognition services failed.")
    

class AudioInput:
    def __init__(self, language="fr-FR", microphone=None):
        self.recognizer = CustomRecognizer(language=language)
        self.microphone = microphone if microphone else sr.Microphone()

    def listen(self, timeout=2, phrase_time_limit=None):
        """Listen continuously and transcribe until the user stops speaking.

        Parameters:
        - timeout: maximum seconds to wait for the phrase to start (silence threshold)
        - phrase_time_limit: maximum seconds for each phrase chunk (None for unlimited)

        Returns:
        - full transcribed text (str)
        """
        text_parts = []
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                except sr.WaitTimeoutError:
                    break

                try:
                    chunk = self.recognizer.recognize(audio)
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    raise e

                if chunk and chunk.strip():
                    text_parts.append(chunk.strip())
        return " ".join(text_parts).strip()

    def recognize(self, audio_data, *args, **kwargs):
        return self.recognizer.recognize(audio_data, *args, **kwargs)
        


if __name__ == "__main__":

    pass