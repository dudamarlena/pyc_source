# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/nltk.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 3385 bytes
__doc__ = 'PyAMS_catalog.nltk module\n\n'
import nltk
from hypatia.text.interfaces import IPipelineElement
from zope.interface import implementer
from pyams_i18n.language import BASE_LANGUAGES
from pyams_utils.unicode import translate_string
__docformat__ = 'restructuredtext'

@implementer(IPipelineElement)
class NltkStemmedTextProcessor:
    """NltkStemmedTextProcessor"""

    def __init__(self, language='english'):
        if language in BASE_LANGUAGES:
            language = BASE_LANGUAGES[language].lower()
        self.language = language
        self.stemmer = nltk.stem.SnowballStemmer(language, ignore_stopwords=True)

    def process(self, lst):
        """Main process method"""
        result = []
        for s in lst:
            translated = translate_string(s, keep_chars="'-").replace("'", ' ')
            tokens = nltk.word_tokenize(translated, self.language)
            result += [stem for stem in [self.stemmer.stem(token) for token in tokens if token not in self.stemmer.stopwords] if stem and len(stem) > 1 and stem not in self.stemmer.stopwords]

        return result

    def processGlob(self, lst):
        """Globs processing method"""
        result = []
        for s in lst:
            translated = translate_string(s, keep_chars="'-*?").replace("'", ' ')
            tokens = nltk.word_tokenize(translated, self.language)
            result += [stem for stem in [self.stemmer.stem(token) for token in tokens if token not in self.stemmer.stopwords] if stem and len(stem) > 1 and stem not in self.stemmer.stopwords]

        return result


@implementer(IPipelineElement)
class NltkFullTextProcessor:
    """NltkFullTextProcessor"""

    def __init__(self, language='english'):
        if language in BASE_LANGUAGES:
            language = BASE_LANGUAGES[language].lower()
        self.language = language

    def process(self, lst):
        """Main processing method"""
        result = []
        for s in lst:
            translated = translate_string(s, keep_chars="'-").replace("'", ' ')
            result += [token for token in nltk.word_tokenize(translated, self.language) if token and len(token) > 1]

        return result

    def processGlob(self, lst):
        """Globs processing method"""
        result = []
        for s in lst:
            translated = translate_string(s, keep_chars="'-*?").replace("'", ' ')
            result += [token for token in nltk.word_tokenize(translated, self.language) if token and len(token) > 1]

        return result