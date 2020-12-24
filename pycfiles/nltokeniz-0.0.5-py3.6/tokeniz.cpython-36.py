# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nltokeniz/tokeniz.py
# Compiled at: 2017-07-16 09:18:23
# Size of source mod 2**32: 1443 bytes
import iso639, langdetect, nltk, MeCab, nlnormaliz
__all__ = [
 'tokenize']

def tokenize(document, language=None):
    if language is not None:
        if not iso639.is_valid639_1(language):
            raise ValueError('"{}" is not a valid ISO 639-1 code.'.format(language))
    document = nlnormaliz.normalize(document)
    return {'en':tokenize_english, 
     'ja':tokenize_japanese}.get(language or detect_language(document), tokenize_english)(document)


def detect_language(document):
    try:
        return langdetect.detect(document)
    except:
        return


def tokenize_english(document):
    return [nltk.tokenize.word_tokenize(sentence.strip()) for sentence in nltk.tokenize.sent_tokenize(document.strip())]


def tokenize_japanese(document):
    sentence_tokenizer = nltk.RegexpTokenizer('[^{0}]+(?:[{0}]+|$)'.format('!?.！？。．'))
    return [list(sentence_to_words_in_japanese(sentence.strip())) for sentence in sentence_tokenizer.tokenize(document.strip())]


def sentence_to_words_in_japanese(sentence):
    tagger = MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(sentence)
    while node is not None:
        if node.surface != '':
            yield node.surface
        node = node.next

    raise StopIteration()