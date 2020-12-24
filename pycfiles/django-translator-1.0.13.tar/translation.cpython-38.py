# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/christianschuermann/Documents/Repositories/django-translator/translator/translation.py
# Compiled at: 2020-01-22 10:12:27
# Size of source mod 2**32: 292 bytes
from modeltranslation.translator import translator, TranslationOptions
from translator.models import Translation

class TranslationTranslationOptions(TranslationOptions):
    fields = ('description', )


translator.register(Translation, TranslationTranslationOptions)