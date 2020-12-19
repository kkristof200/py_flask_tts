# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
import os

# Pip
from flask import Flask, request, send_file, abort

# Local
from .text_to_speech import TextToSpeech
from .utils import verify_hash

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ---------------------------------------------------------- Public properties ----------------------------------------------------------- #

app = Flask(__name__)

# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

@app.route('/tts', methods=['GET', 'POST'])
def tts():
    text = request.headers['text'] if 'text' in request.headers else None
    wpm = int(request.headers['wpm']) if 'wpm' in request.headers else None
    hash = request.headers['hash'] if 'hash' in request.headers else None
    extenison = request.headers['extenison'] if 'extenison' in request.headers else '.m4a'

    if not verify_hash(text, hash):
        return 'Unauth', 400

    audio_name = 'temp.{}'.format(extenison.lstrip('.'))
    audio_path = os.path.join(os.getcwd(), audio_name)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    TextToSpeech.text_to_speech(text, audio_path, 'com.apple.speech.synthesis.voice.daniel.premium', debug=True)

    if os.path.exists(audio_path):
        try:
            return send_file(audio_path, attachment_filename=audio_name)
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