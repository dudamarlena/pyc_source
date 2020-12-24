# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/src/api_connections.py
# Compiled at: 2018-01-03 04:40:05
# Size of source mod 2**32: 461 bytes
from googletrans import Translator
translator = Translator()

def translate(text, src_lng=None, dest_lng=None):
    if src_lng and dest_lng:
        translated = translator.translate(text, src=src_lng, dest=dest_lng)
    else:
        if src_lng:
            translated = translator.translate(text, src=src_lng)
        else:
            if dest_lng:
                translated = translator.translate(text, dest=dest_lng)
            else:
                translated = translator.translate(text)
    return translated