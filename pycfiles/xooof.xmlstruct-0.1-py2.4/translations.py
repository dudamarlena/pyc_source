# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmlstruct/translations.py
# Compiled at: 2008-10-01 11:16:13
try:
    import os, gettext, locale
    translationDir = os.path.join(os.path.dirname(__file__), 'locale')
    if hasattr(locale, 'LC_MESSAGES'):
        language = locale.getlocale(locale.LC_MESSAGES)[0]
    else:
        language = locale.getlocale(locale.LC_ALL)[0]
    _ = gettext.translation('xmlstruct', translationDir, [language]).gettext
except:

    def _(msg):
        return msg