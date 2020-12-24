# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/slu/cognitive_luis.py
# Compiled at: 2018-01-07 13:01:17
# Size of source mod 2**32: 769 bytes
from luis_sdk import LUISClient
import logging
logging.basicConfig()
logger = logging.getLogger('pi-assistant')

class CognitiveLuis:

    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        if self.appid == '':
            logger.warning('COGNITIVE_LUIS_APPID is empty')
        if self.appkey == '':
            logger.warning('COGNITIVE_LUIS_APPKEY is empty')

    def understand(self, text):
        client = LUISClient(self.appid, self.appkey, True)
        res = client.predict(text)
        top = res.get_top_intent()
        entities = res.get_entities()
        entities = [(x.get_type(), x.get_name()) for x in entities]
        intent = top.get_name()
        result = (intent, entities)
        return result