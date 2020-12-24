# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/translations.py
# Compiled at: 2018-04-22 16:57:43
import gettext, locale, os

def get_translations(language):
    mo_filename = os.path.join(os.path.dirname(__file__), 'translations', language + '.mo')
    if os.path.exists(mo_filename):
        mo_file = open(mo_filename, 'rb')
        translations = gettext.GNUTranslations(mo_file)
        mo_file.close()
        return translations
    else:
        return


language = locale.getdefaultlocale()[0]
translations = None
if language:
    if language in ('ru_RU', 'Russian_Russia'):
        language = 'ru'
    translations = get_translations(language)
if translations is None:
    translations = gettext.NullTranslations()