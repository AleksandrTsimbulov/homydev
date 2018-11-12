import requests
from alias import db
from alias.models import Translems


def synthesize_word_via_yandex(text,
                               key='f0beeec3-8e78-40af-841f-3be467eefcbf',
                               audio_format='mp3',
                               quality=None,
                               lang='en-US',
                               speaker='zahar',
                               speed=None,
                               emotion=None,
                               ):
    parameters = {'key': key,
                  'text': text,
                  'format': audio_format,
                  'quality': quality,
                  'lang': lang,
                  'speaker': speaker,
                  'speed': speed,
                  'emotion': emotion,
                  }
    return requests.get('https://tts.voicetech.yandex.net/generate', params=parameters).content


def synthesize_several_words_and_save_as_files_and_commit_to_database(number_of_words):
    translems = Translems.query.filter(Translems.voice.is_(None)).limit(number_of_words).all()
    for translem in translems:
        word = translem.english
        print(word)
        binary_voice = synthesize_word_via_yandex(word)
        translem.voice = binary_voice
        db.session.commit()
        if '/' in word:
            word = word.replace('/', 'or')
        with open(f'./voices/{word}.mp3', 'wb') as ps:
            ps.write(binary_voice)


number_or_words = 300
synthesize_several_words_and_save_as_files_and_commit_to_database(number_or_words)
