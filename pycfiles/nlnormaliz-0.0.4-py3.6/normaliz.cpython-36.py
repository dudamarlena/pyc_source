# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nlnormaliz/normaliz.py
# Compiled at: 2017-07-16 09:36:06
# Size of source mod 2**32: 955 bytes
import functools, unicodedata, iso639, langdetect, neologdn
__all__ = [
 'normalize']

def normalize(document, language=None):
    if language is not None:
        if not iso639.is_valid639_1(language):
            raise ValueError('"{}" is not a valid ISO 639-1 code.'.format(language))
    return {'en':normalize_english,  'ja':normalize_japanese}.get(language or detect_language(document), normalize_english)(document)


def detect_language(document):
    try:
        return langdetect.detect(document)
    except:
        return


def common_normalization(func):

    @functools.wraps(func)
    def wrapper(document):
        return func(unicodedata.normalize('NFKC', document.strip()))

    return wrapper


@common_normalization
def normalize_english(document):
    return document


@common_normalization
def normalize_japanese(document):
    return neologdn.normalize(document)