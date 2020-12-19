from flasktts.text_to_speech import TextToSpeech

TextToSpeech.text_to_speech(
    text='This is a test.',
    path='test.aac',
    voice_id_or_address='http://localhost:5005',
    words_per_minute=130,
    debug=True
)