# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: smart_mirror/pywit.py
# Compiled at: 2018-09-24 17:55:38
# Size of source mod 2**32: 896 bytes
import json, sys
from smart_mirror.recorder import record_audio, read_audio
from wit import Wit
access_token = 'K6ZAK63RQWSYWIQYOWAUVQ7PWVRMD66R'
client = Wit(access_token=access_token)

def RecognizeSpeech(AUDIO_FILENAME, num_seconds=5):
    record_audio(num_seconds, AUDIO_FILENAME)
    audio = read_audio(AUDIO_FILENAME)
    resp = None
    resp = client.speech(audio, None, {'Content-Type': 'audio/wav'})
    print('Yay, got Wit.ai response: ' + str(resp))
    text = resp['_text']
    return resp


if __name__ == '__main__':
    text = RecognizeSpeech('myspeech.wav', 4)
    print('\nYou said: {}'.format(text))