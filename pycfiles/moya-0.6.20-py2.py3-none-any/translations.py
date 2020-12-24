# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/translations.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
import gettext, logging
log = logging.getLogger(b'moya.startup')

class Translations(object):

    def __init__(self):
        self._translations = {}
        self._null = gettext.NullTranslations()

    def read(self, domain, localedir, languages):
        for lang in languages:
            try:
                translations = gettext.translation(domain, localedir, [
                 lang])
            except IOError:
                log.warning((b"no translations found for language code '{}'").format(lang))
                translations = None

            if translations is not None:
                self._translations[lang] = translations

        return

    def get(self, languages):
        for lang in languages:
            if lang in self._translations:
                return self._translations[lang]

        return self._null