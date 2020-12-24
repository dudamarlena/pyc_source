# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christianschuermann/Documents/Repositories/django-translator/translator/context_processors.py
# Compiled at: 2020-01-22 10:12:27
# Size of source mod 2**32: 336 bytes
from translator.util import get_translation_for_key

class Translator(object):

    def __init__(self, request):
        self.request = request

    def __getattr__(self, item):
        return get_translation_for_key(item)


def translator(request):
    return {'translator': Translator(request)}