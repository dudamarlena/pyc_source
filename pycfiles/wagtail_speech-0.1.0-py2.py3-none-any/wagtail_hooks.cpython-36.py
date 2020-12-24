# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robmoorman/Developer/moori/wagtail-speech/src/wagtailspeech/wagtail_hooks.py
# Compiled at: 2017-05-23 06:27:26
# Size of source mod 2**32: 221 bytes
from wagtail.wagtailcore import hooks
from wagtailspeech.utils import synthesize_speech_from_page

@hooks.register('after_edit_page')
def synthesize_speech(request, page):
    synthesize_speech_from_page(request, page)