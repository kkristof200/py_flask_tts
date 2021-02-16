from flasktts import TextToSpeech, Secret

Secret.KEY = 'OVERRIDE_SECRET_KEY'

TextToSpeech.text_to_speech(
    text='This is a test.',
    path='test.aac',
    address='localhost:5005',
    # words_per_minute=130,
    # voice_id='com.apple.speech.synthesis.voice.daniel.premium',
    debug=True
)