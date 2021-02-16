# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import os, shutil

# Pip
from unidecode import unidecode
from kcu import request, kpath
import pyttsx3
from kffmpeg import ffmpeg

# Local
from ._constants import Constants, Keys
from ._utils import sign, get_temp_path

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: TextToSpeech ---------------------------------------------------------- #

class TextToSpeech:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def text_to_speech(
        cls,
        text: str,
        path: str,
        voice_id: Optional[str] = None,
        address: Optional[str] = None,
        words_per_minute: Optional[int] = None,
        debug: bool = False
    ) -> bool:
        text = unidecode(text.strip())

        if address and not address.startswith(Constants.ADDRESS_PREFIX):
            address = '{}{}'.format(Constants.ADDRESS_PREFIX, address)

        if not address and voice_id and voice_id.startswith(Constants.ADDRESS_PREFIX):
            address = voice_id
            voice_id = None

        if address:
            return cls.__tts_from_url(
                text=text,
                path=path,
                url=address,
                voice_id=voice_id,
                words_per_minute=words_per_minute,
                debug=debug
            )
        else:
            return cls.__tts_local(
                text=text,
                path=path,
                voice_id=voice_id or Constants.TTS_DEFAULT_VOICE_ID,
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
        temp_path = get_temp_path(Constants.LOCAL_AUDIO_EXTENSION)

        engine = pyttsx3.init()
        engine.setProperty('voice', voice_id)

        if words_per_minute:
            engine.setProperty('rate', words_per_minute)

        engine.save_to_file(text=text, filename=temp_path)
        engine.runAndWait()

        if not os.path.exists(temp_path):
            return False

        if path.endswith('.mp3'):
            ffmpeg.reencode_mp3(temp_path, path, debug=False)
        elif path.endswith(Constants.LOCAL_AUDIO_EXTENSION):
            shutil.copy2(temp_path, path)
        else:
            ffmpeg.reencode_aac(temp_path, path, debug=False)

        kpath.remove(temp_path)

        return os.path.exists(path)

    @staticmethod
    def __tts_from_url(
        text: str,
        path: str,
        url: str,
        voice_id: Optional[str] = None,
        words_per_minute: Optional[int] = None,
        debug: bool = False
    ) -> bool:
        url = url.strip('/')

        if not url.endswith('/tts'):
            url += '/tts'

        response = request.post(
            url,
            headers={k:v  for k, v in {
                Keys.TEXT: text,
                Keys.HASH: sign(text),
                Keys.WPM: str(words_per_minute) if words_per_minute else None,
                Keys.VOICE_ID: voice_id,
                Keys.EXTENISON: path.split('.')[-1]
            }.items() if v},
            max_request_try_count=2,
            debug=debug
        )

        print('TTS - response: \'{}\''.format(response))

        if not response or response.status_code != 200 or not response.content:
            return False

        with open(path, 'wb') as f:
            f.write(response.content)

        return os.path.exists(path)


# ---------------------------------------------------------------------------------------------------------------------------------------- #