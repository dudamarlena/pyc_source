# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_captcha/settings.py
# Compiled at: 2014-06-13 14:34:59
# Size of source mod 2**32: 1344 bytes
import os
from flask import current_app
DEBUG = True
CAPTCHA_FONT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), 'fonts/Vera.ttf'))
CAPTCHA_FONT_SIZE = 22
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_CHALLENGE_FUNCT = 'flask.ext.captcha.helpers.random_char_challenge'
CAPTCHA_NOISE_FUNCTIONS = ('flask.ext.captcha.helpers.noise_arcs', 'flask.ext.captcha.helpers.noise_dots')
CAPTCHA_FILTER_FUNCTIONS = ('flask.ext.captcha.helpers.post_smooth', )
CAPTCHA_WORDS_DICTIONARY = '/usr/share/dict/words'
CAPTCHA_PUNCTUATION = '_"\',.;:-'
CAPTCHA_FLITE_PATH = None
CAPTCHA_TIMEOUT = 5
CAPTCHA_LENGTH = int(4)
CAPTCHA_IMAGE_BEFORE_FIELD = True
CAPTCHA_DICTIONARY_MIN_LENGTH = 0
CAPTCHA_DICTIONARY_MAX_LENGTH = 99
if CAPTCHA_IMAGE_BEFORE_FIELD:
    CAPTCHA_OUTPUT_FORMAT = '%(image)s %(hidden_field)s %(text_field)s'
else:
    CAPTCHA_OUTPUT_FORMAT = '%(hidden_field)s %(text_field)s %(image)s'
CAPTCHA_TEST_MODE = False
if CAPTCHA_DICTIONARY_MIN_LENGTH > CAPTCHA_DICTIONARY_MAX_LENGTH:
    CAPTCHA_DICTIONARY_MIN_LENGTH, CAPTCHA_DICTIONARY_MAX_LENGTH = CAPTCHA_DICTIONARY_MAX_LENGTH, CAPTCHA_DICTIONARY_MIN_LENGTH
CAPTCHA_PREGEN = True
CAPTCHA_PREGEN_PATH = '/tmp/flask-captcha'
CAPTCHA_PREGEN_MAX = 10