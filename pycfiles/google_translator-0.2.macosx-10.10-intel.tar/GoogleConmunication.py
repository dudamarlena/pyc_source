# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/google_translator/GoogleConmunication.py
# Compiled at: 2015-04-23 23:14:30
import urllib2, urllib
from Lang import *
TIME_OUT = 5

class GoogleConmunication(object):

    def translate(self, source_lang=Lang.auto, target_lang=Lang.chinese_simplified, content=None):
        if not content:
            return content
        data = {'client': 't', 'sl': source_lang, 'tl': target_lang, 'dt': 't', 'ie': 'UTF-8', 'q': content}
        data = urllib.urlencode(data)
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(self.__baseUrl, data, headers)
        raw = urllib2.urlopen(req, timeout=TIME_OUT).read()
        return self.parse_resutlt(raw)

    def parse_resutlt(self, raw=None):
        if not raw:
            return raw
        index = raw.rfind(']],')
        raw = raw[1:index + 2] + ''
        result_list = eval(raw)
        result = ''
        for i in result_list:
            result += i[0]

        return result

    def __init__(self):
        self.__baseUrl = 'https://translate.google.com/translate_a/single'