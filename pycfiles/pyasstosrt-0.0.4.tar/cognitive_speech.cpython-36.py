# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/asr/cognitive_speech.py
# Compiled at: 2018-01-07 13:01:17
# Size of source mod 2**32: 1477 bytes
import urllib.request as request, uuid, json, logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')

class CognitiveSpeech:

    def __init__(self, key):
        self.key = key
        if self.key == '':
            logger.warning('COGNITIVE_SPEECH_KEY is empty')
        self.lang = 'ja-JP'
        self.sampling_rate = 16000

    def recognize(self, file):
        url = 'https://api.cognitive.microsoft.com/sts/v1.0/issueToken'
        req = request.Request(url)
        req.add_header('Ocp-Apim-Subscription-Key', self.key)
        with request.urlopen(req, data=(''.encode('utf-8'))) as (res):
            token = res.read().decode('utf-8')
        with open(file, 'rb') as (f):
            audio = f.read()
        url = 'https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1'
        url += '?Version=3.0'
        url += '&language=' + self.lang
        url += '&format=json'
        url += '&requestid=' + str(uuid.uuid4())
        req = request.Request(url)
        req.add_header('Authorization', 'Bearser ' + token)
        req.add_header('Content-Type', 'audio/wav; codec="audio/pcm"; samplerate=' + str(self.sampling_rate))
        with request.urlopen(req, data=audio) as (res):
            result = res.read().decode('utf-8')
        result = json.loads(result)
        if 'DisplayText' in result:
            text = result['DisplayText']
        else:
            text = None
        return text