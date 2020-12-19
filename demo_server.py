from flasktts.server import start_tts_server
from flasktts.constants import Constants

Constants.SECRET_KEY = 'test'

start_tts_server(
    host='localhost',
    port=5005,
    debug=True,
)