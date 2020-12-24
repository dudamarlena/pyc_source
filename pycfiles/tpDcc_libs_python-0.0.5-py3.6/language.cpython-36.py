# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/language.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 869 bytes
"""
Utility methods related to languages
"""
from __future__ import print_function, division, absolute_import
import re, os, locale

class Language(object):

    def __init__(self, en='', es='', jp=''):
        self.en = en
        self.es = es
        self.jp = jp

    def output(self):
        lang = 'en'
        env = re.sub('_.+', '', os.environ.get('MAYA_UI_LANGUAGE', ''))
        loc = re.sub('_.+', '', locale.getdefaultlocale()[0])
        env = re.sub('-.+', '', env)
        loc = re.sub('-.+', '', loc)
        if loc != '':
            lang = loc
        if env != '':
            lang = env
        if lang == 'ja' or lang == 'jp':
            return self.jp
        if lang == 'en':
            return self.en
        else:
            if lang == 'es':
                return self.es
            return self.en