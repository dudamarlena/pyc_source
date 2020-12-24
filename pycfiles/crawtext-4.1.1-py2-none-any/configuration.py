# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/c24b/projets/crawtext/newspaper/configuration.py
# Compiled at: 2014-11-17 11:14:10
"""
This class holds configuration objects, which can be thought of
as settings.py but dynamic and changing for whatever parent object
holds them. For example, pass in a config object to an Article
object, Source object, or even network methods, and it just works.
"""
__title__ = 'newspaper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
import logging
from .parsers import Parser, ParserSoup
from .text import StopWords, StopWordsArabic, StopWordsChinese, StopWordsKorean
from .version import __version__
log = logging.getLogger(__name__)

class Configuration(object):

    def __init__(self):
        """
        Modify any of these Article / Source properties
        TODO: Have a seperate ArticleConfig and SourceConfig extend this!
        """
        self.MIN_WORD_COUNT = 300
        self.MIN_SENT_COUNT = 7
        self.MAX_TITLE = 200
        self.MAX_TEXT = 100000
        self.MAX_KEYWORDS = 35
        self.MAX_AUTHORS = 10
        self.MAX_SUMMARY = 5000
        self.MAX_FILE_MEMO = 20000
        self.parser_class = 'lxml'
        self.memoize_articles = True
        self.fetch_images = True
        self.image_dimension_ration = 16 / 9.0
        self.use_meta_language = True
        self.keep_article_html = False
        self._language = 'en'
        self.stopwords_class = StopWords
        self.browser_user_agent = 'newspaper/%s' % __version__
        self.request_timeout = 7
        self.number_threads = 10
        self.verbose = False

    def get_language(self):
        return self._language

    def del_language(self):
        raise Exception('wtf are you doing?')

    def set_language(self, language):
        """Language setting must be set in this method b/c non-occidental
        (western) langauges require a seperate stopwords class.
        """
        if not language or len(language) != 2:
            raise Exception('Your input language must be a 2 char langauge code,                 for example: english-->en \n and german-->de')
        self.use_meta_language = False
        self._language = language
        self.stopwords_class = self.get_stopwords_class(language)

    language = property(get_language, set_language, del_language, 'langauge prop')

    def get_stopwords_class(self, language):
        if language == 'ko':
            return StopWordsKorean
        if language == 'zh':
            return StopWordsChinese
        if language == 'ar':
            return StopWordsArabic
        return StopWords

    def get_parser(self):
        if self.parser_class == 'lxml':
            return Parser
        return ParserSoup


class ArticleConfiguration(Configuration):
    pass


class SourceConfiguration(Configuration):
    pass