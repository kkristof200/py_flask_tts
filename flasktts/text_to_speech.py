# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import os

# Pip
from unidecode import unidecode
from kcu import request, kpath
import pyttsx3
from kffmpeg import ffmpeg

# Local
from .utils import sign

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: TextToSpeech ---------------------------------------------------------- #

class TextToSpeech:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def text_to_speech(
        cls,
        text: str,
        path: str,
        voice_id_or_address: str,
        words_per_minute: Optional[int] = None,
        debug: bool = False
    ):
        text = unidecode(text.strip())

        if voice_id_or_address.startswith('http'):
            return cls.__tts_from_url(
                text=text,
                path=path,
                url=voice_id_or_address,
                words_per_minute=words_per_minute,
                debug=debug
            )
        else:
            return cls.__tts_local(
                text=text,
                path=path,
                voice_id=voice_id_or_address,
                words_per_minute=words_per_minute,
                debug=debug
            )


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __tts_local(
        text: str,
        path: str,
        voice_id: str,
        words_per_minute: Optional[int] = None,
        debug: bool = False
    ) -> bool:
        temp_path = os.path.join(os.getcwd(), 'temp.aiff')

        engine = pyttsx3.init()
        engine.setProperty('voice', voice_id)

        if words_per_minute is not None:
            engine.setProperty('rate', words_per_minute)

        engine.save_to_file(text=text, filename=temp_path)
        engine.runAndWait()

        if path.endswith('.mp3'):
            ffmpeg.reencode_mp3(temp_path, path)
        else:
            ffmpeg.reencode_aac(temp_path, path, debug=False)

        kpath.remove(temp_path)

        return os.path.exists(path)

    @staticmethod
    def __tts_from_url(
        text: str,
        path: str,
        url: str,
        words_per_minute: Optional[int] = None,
        debug: bool = False
    ) -> bool:
        url = url.strip('/')

        if not url.endswith('/tts'):
            url += '/tts'

        response = request.post(
            url,
            headers={
                'text': text,
                'hash': sign(text),
                'wpm': str(words_per_minute),
                'extenison': path.split('.')[-1]
            },
            max_request_try_count=2,
            debug=debug
        )

        print('response', response)

        if not response or response.status_code != 200 or not response.content:
            return False

        with open(path, 'wb') as f:
            f.write(response.content)

        return os.path.exists(path)


# ---------------------------------------------------------------------------------------------------------------------------------------- #