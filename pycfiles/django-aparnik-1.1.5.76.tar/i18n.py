# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/humanize/i18n.py
# Compiled at: 2018-11-05 07:19:14
import gettext as gettext_module
from threading import local
import os.path
__all__ = [
 'activate', 'deactivate', 'gettext', 'ngettext']
_TRANSLATIONS = {None: gettext_module.NullTranslations()}
_CURRENT = local()
_DEFAULT_LOCALE_PATH = os.path.join(os.path.dirname(__file__), 'locale')

def get_translation():
    try:
        return _TRANSLATIONS[_CURRENT.locale]
    except (AttributeError, KeyError):
        return _TRANSLATIONS[None]

    return


def activate(locale, path=None):
    """Set 'locale' as current locale. Search for locale in directory 'path'
    @param locale: language name, eg 'en_GB'"""
    if path is None:
        path = _DEFAULT_LOCALE_PATH
    if locale not in _TRANSLATIONS:
        translation = gettext_module.translation('humanize', path, [locale])
        _TRANSLATIONS[locale] = translation
    _CURRENT.locale = locale
    return _TRANSLATIONS[locale]


def deactivate():
    _CURRENT.locale = None
    return


def gettext(message):
    return get_translation().gettext(message)


def pgettext(msgctxt, message):
    """'Particular gettext' function.
    It works with 'msgctxt' .po modifiers and allow duplicate keys with
    different translations.
    Python 2 don't have support for this GNU gettext function, so we
    reimplement it. It works by joining msgctx and msgid by '4' byte."""
    key = msgctxt + '\x04' + message
    translation = get_translation().gettext(key)
    if translation == key:
        return message
    return translation


def ngettext(message, plural, num):
    return get_translation().ngettext(message, plural, num)


def gettext_noop(message):
    """Example usage:
    CONSTANTS = [gettext_noop('first'), gettext_noop('second')]
    def num_name(n):
        return gettext(CONSTANTS[n])"""
    return message