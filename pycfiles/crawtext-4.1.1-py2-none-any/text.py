# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/c24b/projets/crawtext/newspaper/text.py
# Compiled at: 2014-11-06 08:50:33
"""
Stopword extraction and stopword classes.
"""
__title__ = 'newspaper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
import os, re, string
from .utils import FileHelper
TABSSPACE = re.compile('[\\s\\t]+')

def innerTrim(value):
    if isinstance(value, (unicode, str)):
        value = re.sub(TABSSPACE, ' ', value)
        value = ('').join(value.splitlines())
        return value.strip()
    return ''


class WordStats(object):

    def __init__(self):
        self.stop_word_count = 0
        self.word_count = 0
        self.stop_words = []

    def get_stop_words(self):
        return self.stop_words

    def set_stop_words(self, words):
        self.stop_words = words

    def get_stopword_count(self):
        return self.stop_word_count

    def set_stopword_count(self, wordcount):
        self.stop_word_count = wordcount

    def get_word_count(self):
        return self.word_count

    def set_word_count(self, cnt):
        self.word_count = cnt


class StopWords(object):
    PUNCTUATION = re.compile('[^\\p{Ll}\\p{Lu}\\p{Lt}\\p{Lo}\\p{Nd}\\p{Pc}\\s]')
    TRANS_TABLE = string.maketrans('', '')
    _cached_stop_words = {}

    def __init__(self, language='en'):
        if language not in self._cached_stop_words:
            path = os.path.join('text', 'stopwords-%s.txt' % language)
            self._cached_stop_words[language] = set(FileHelper.loadResourceFile(path).splitlines())
        self.STOP_WORDS = self._cached_stop_words[language]

    def remove_punctuation(self, content):
        content_is_unicode = isinstance(content, unicode)
        if content_is_unicode:
            content = content.encode('utf-8')
        stripped_input = content.translate(self.TRANS_TABLE, string.punctuation)
        if content_is_unicode:
            return stripped_input.decode('utf-8')
        return stripped_input

    def candidate_words(self, stripped_input):
        return stripped_input.split(' ')

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        ws = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        c = 0
        for w in candidate_words:
            c += 1
            if w.lower() in self.STOP_WORDS:
                overlapping_stopwords.append(w.lower())

        ws.set_word_count(c)
        ws.set_stopword_count(len(overlapping_stopwords))
        ws.set_stop_words(overlapping_stopwords)
        return ws


class StopWordsChinese(StopWords):
    """Chinese segmentation
    """

    def __init__(self, language='zh'):
        super(StopWordsChinese, self).__init__(language='zh')

    def candidate_words(self, stripped_input):
        from .packages import jieba
        return jieba.cut(stripped_input, cut_all=True)


class StopWordsArabic(StopWords):
    """Arabic segmentation
    """

    def __init__(self, language='ar'):
        super(StopWordsArabic, self).__init__(language='ar')

    def remove_punctuation(self, content):
        return content

    def candidate_words(self, stripped_input):
        import nltk
        s = nltk.stem.isri.ISRIStemmer()
        words = []
        for word in nltk.tokenize.wordpunct_tokenize(stripped_input):
            words.append(s.stem(word))

        return words


class StopWordsKorean(StopWords):
    """Korean segmentation
    """

    def __init__(self, language='ko'):
        super(StopWordsKorean, self).__init__(language='ko')

    def get_stopword_count(self, content):
        if not content:
            return WordStats()
        ws = WordStats()
        stripped_input = self.remove_punctuation(content)
        candidate_words = self.candidate_words(stripped_input)
        overlapping_stopwords = []
        c = 0
        for w in candidate_words:
            c += 1
            for stop_word in self.STOP_WORDS:
                overlapping_stopwords.append(stop_word)

        ws.set_word_count(c)
        ws.set_stopword_count(len(overlapping_stopwords))
        ws.set_stop_words(overlapping_stopwords)
        return ws