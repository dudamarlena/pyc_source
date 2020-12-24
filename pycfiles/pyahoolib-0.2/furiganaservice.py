# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyahooapis\jlp\furiganaservice.py
# Compiled at: 2011-05-16 12:40:27
from pyahooapis.service import Service, BaseObject

class FuriganaService(Service):
    url = 'http://jlp.yahooapis.jp/FuriganaService/V1/furigana'

    def get_words(self, sentence, grade=None, json=False):
        u"""
        詳しくは
        http://developer.yahoo.co.jp/webapi/jlp/furigana/v1/furigana.html
        
        Args:
            sentence: ルビ振りする文章
            grade: 学年(0~7)
            json: JSON形式で返すかどうか
        Returns:
            そのうち
        """
        params = {}
        params['sentence'] = sentence
        if grade is not None:
            params['grade'] = grade
        dom = self._get_dom(params)
        words = []
        for w in dom.getElementsByTagName('Word'):
            words.append(Word(self._get_text(w, 'Surface'), self._get_text(w, 'Furigana'), self._get_text(w, 'Roman'), [ SubWord(self._get_text(sw, 'Surface'), self._get_text(sw, 'Furigana'), self._get_text(sw, 'Roman')) for sw in w.getElementsByTagName('SubWord')
                                                                                                                       ]))

        return self.py2json(words) if json else words


class Word(BaseObject):

    def __init__(self, surface, furigana, roman, subwords=None):
        self.surface = surface
        self.furigana = furigana
        self.roman = roman
        self.subwords = subwords

    def __str__(self):
        return self.encode(self.surface)


class SubWord(BaseObject):

    def __init__(self, surface, furigana, roman):
        self.surface = surface
        self.furigana = furigana
        self.roman = roman

    def __str__(self):
        return self.encode(self.surface)