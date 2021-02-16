from flasktts import start_tts_server, Secret

Secret.KEY = 'OVERRIDE_SECRET_KEY'

start_tts_server(
    host='localhost',
    port=5005,
    debug=True,
)