# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import os

# Pip
from flask import Flask, request, send_file, abort

# Local
from .text_to_speech import TextToSpeech
from ._constants import Constants, Keys
from ._utils import verify_hash, get_temp_path

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- Public properties ----------------------------------------------------------- #

app = Flask(__name__)

# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

@app.route('/tts', methods=['GET', 'POST'])
def tts():
    text = request.headers[Keys.TEXT]
    hash = request.headers[Keys.HASH]

    if not verify_hash(text, hash):
        return 'Unauth', 400

    wpm_str = request.headers.get(Keys.WPM)
    if wpm_str:
        try:
            wpm = int(wpm_str)
        except:
            wpm = None
    else:
        wpm = None

    audio_path = get_temp_path(request.headers.get(Keys.EXTENISON, 'm4a'))

    if os.path.exists(audio_path):
        os.remove(audio_path)

    TextToSpeech.text_to_speech(
        text=text,
        path=audio_path,
        voice_id=request.headers.get(
            Keys.VOICE_ID,
            Constants.TTS_DEFAULT_VOICE_ID
        ),
        words_per_minute=wpm,
        debug=True
    )

    if os.path.exists(audio_path):
        try:
            return send_file(
                audio_path,
                attachment_filename=audio_path.split(os.sep)[-1]
            )
        except Exception as e:
            return str(e), 400

        os.remove(audio_path)
    else:
        return 'Could not create tts', 400

@app.route('/ping')
def ping():
    return 'pong'

def start_tts_server(
    host: str = '0.0.0.0',
    port: int = 5005,
    debug: bool = False
) -> None:
    app.debug = debug
    app.run(host=host, port=port)


# ---------------------------------------------------------------------------------------------------------------------------------------- #