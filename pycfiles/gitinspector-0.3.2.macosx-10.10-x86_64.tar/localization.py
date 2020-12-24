# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/localization.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
import basedir, gettext, locale, os, sys, time
__enabled__ = False
__installed__ = False
__translation__ = None

def N_(message):
    return message


def init():
    global __enabled__
    global __installed__
    global __translation__
    if not __installed__:
        try:
            locale.setlocale(locale.LC_ALL, b'')
        except locale.Error:
            __translation__ = gettext.NullTranslations()

        lang = locale.getlocale()
        if os.getenv(b'LANG') is None:
            lang = locale.getdefaultlocale()
            if lang[0]:
                os.environ[b'LANG'] = lang[0]
        if lang[0] is not None:
            filename = basedir.get_basedir() + b'/translations/messages_%s.mo' % lang[0][0:2]
            try:
                __translation__ = gettext.GNUTranslations(open(filename, b'rb'))
            except IOError:
                __translation__ = gettext.NullTranslations()

        else:
            print(b'WARNING: Localization disabled because the system language could not be determined.', file=sys.stderr)
            __translation__ = gettext.NullTranslations()
        __enabled__ = True
        __installed__ = True
        __translation__.install(True)
    return


def get_date():
    if __enabled__ and isinstance(__translation__, gettext.GNUTranslations):
        date = time.strftime(b'%x')
        if hasattr(date, b'decode'):
            date = date.decode(b'utf-8', b'replace')
        return date
    return time.strftime(b'%Y/%m/%d')


def enable():
    global __enabled__
    if isinstance(__translation__, gettext.GNUTranslations):
        __translation__.install(True)
        __enabled__ = True


def disable():
    global __enabled__
    __enabled__ = False
    if __installed__:
        gettext.NullTranslations().install(True)