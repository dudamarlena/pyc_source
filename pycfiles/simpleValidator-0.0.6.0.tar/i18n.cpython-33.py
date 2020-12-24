# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kenmartel/Development/Python/simpleValidator/simplevalidator/i18n.py
# Compiled at: 2014-01-28 15:14:31
# Size of source mod 2**32: 740 bytes
import os
from . import settings
import gettext
APP_NAME = 'simpleValidator'
LOCALE_DIR = path = os.path.join(os.path.dirname(__file__), 'lang')
DEFAULT_LANGUAGE = settings.LOCALE
defaultlang = gettext.translation(APP_NAME, LOCALE_DIR, languages=DEFAULT_LANGUAGE, fallback=True)

def switch_language(lang):
    global defaultlang
    defaultlang = gettext.translation(APP_NAME, LOCALE_DIR, languages=[lang], fallback=True)