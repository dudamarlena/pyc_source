# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/translate.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 7181 bytes
import gettext, pkg_resources, six
from babel import localedata
from babel.support import LazyProxy
from mediagoblin import mg_globals
AVAILABLE_LOCALES = None
TRANSLATIONS_PATH = pkg_resources.resource_filename('mediagoblin', 'i18n')
KNOWN_RTL = set(['ar', 'fa', 'he', 'iw', 'ur', 'yi', 'ji'])

def is_rtl(lang):
    """Returns true when the local language is right to left"""
    return lang in KNOWN_RTL


def set_available_locales():
    """Set available locales for which we have translations"""
    global AVAILABLE_LOCALES
    locales = [
     'en', 'en_US']
    for locale in localedata.locale_identifiers():
        if gettext.find('mediagoblin', TRANSLATIONS_PATH, [locale]):
            locales.append(locale)
            continue

    AVAILABLE_LOCALES = locales


class ReallyLazyProxy(LazyProxy):
    __doc__ = "\n    Like LazyProxy, except that it doesn't cache the value ;)\n    "

    def __init__(self, func, *args, **kwargs):
        super(ReallyLazyProxy, self).__init__(func, *args, **kwargs)
        object.__setattr__(self, '_is_cache_enabled', False)

    def __repr__(self):
        return '<%s for %s(%r, %r)>' % (
         self.__class__.__name__,
         self._func,
         self._args,
         self._kwargs)


def locale_to_lower_upper(locale):
    """
    Take a locale, regardless of style, and format it like "en_US"
    """
    if '-' in locale:
        lang, country = locale.split('-', 1)
        return '%s_%s' % (lang.lower(), country.upper())
    else:
        if '_' in locale:
            lang, country = locale.split('_', 1)
            return '%s_%s' % (lang.lower(), country.upper())
        return locale.lower()


def locale_to_lower_lower(locale):
    """
    Take a locale, regardless of style, and format it like "en_us"
    """
    if '_' in locale:
        lang, country = locale.split('_', 1)
        return '%s-%s' % (lang.lower(), country.lower())
    else:
        return locale.lower()


def get_locale_from_request(request):
    """
    Return most appropriate language based on prefs/request request
    """
    request_args = (
     request.args, request.form)[(request.method == 'POST')]
    if 'lang' in request_args:
        target_lang = locale_to_lower_upper(request_args['lang'])
    else:
        if 'target_lang' in request.session:
            target_lang = request.session['target_lang']
        else:
            target_lang = request.accept_languages.best_match(AVAILABLE_LOCALES) or 'en_US'
    return target_lang


SETUP_GETTEXTS = {}

def get_gettext_translation(locale):
    """
    Return the gettext instance based on this locale
    """
    if locale in SETUP_GETTEXTS:
        this_gettext = SETUP_GETTEXTS[locale]
    else:
        this_gettext = gettext.translation('mediagoblin', TRANSLATIONS_PATH, [locale], fallback=True)
    if localedata.exists(locale):
        SETUP_GETTEXTS[locale] = this_gettext
    return this_gettext


def set_thread_locale(locale):
    """Set the current translation for this thread"""
    mg_globals.thread_scope.translations = get_gettext_translation(locale)


def pass_to_ugettext(*args, **kwargs):
    """
    Pass a translation on to the appropriate ugettext method.

    The reason we can't have a global ugettext method is because
    mg_globals gets swapped out by the application per-request.
    """
    if six.PY2:
        return mg_globals.thread_scope.translations.ugettext(*args, **kwargs)
    return mg_globals.thread_scope.translations.gettext(*args, **kwargs)


def pass_to_ungettext(*args, **kwargs):
    """
    Pass a translation on to the appropriate ungettext method.

    The reason we can't have a global ugettext method is because
    mg_globals gets swapped out by the application per-request.
    """
    if six.PY2:
        return mg_globals.thread_scope.translations.ungettext(*args, **kwargs)
    return mg_globals.thread_scope.translations.ngettext(*args, **kwargs)


def lazy_pass_to_ugettext(*args, **kwargs):
    """
    Lazily pass to ugettext.

    This is useful if you have to define a translation on a module
    level but you need it to not translate until the time that it's
    used as a string. For example, in:
        def func(self, message=_('Hello boys and girls'))

    you would want to use the lazy version for _.
    """
    return ReallyLazyProxy(pass_to_ugettext, *args, **kwargs)


def pass_to_ngettext(*args, **kwargs):
    """
    Pass a translation on to the appropriate ngettext method.

    The reason we can't have a global ngettext method is because
    mg_globals gets swapped out by the application per-request.
    """
    return mg_globals.thread_scope.translations.ngettext(*args, **kwargs)


def lazy_pass_to_ngettext(*args, **kwargs):
    """
    Lazily pass to ngettext.

    This is useful if you have to define a translation on a module
    level but you need it to not translate until the time that it's
    used as a string.
    """
    return ReallyLazyProxy(pass_to_ngettext, *args, **kwargs)


def lazy_pass_to_ungettext(*args, **kwargs):
    """
    Lazily pass to ungettext.

    This is useful if you have to define a translation on a module
    level but you need it to not translate until the time that it's
    used as a string.
    """
    return ReallyLazyProxy(pass_to_ungettext, *args, **kwargs)


def fake_ugettext_passthrough(string):
    """
    Fake a ugettext call for extraction's sake ;)

    In wtforms there's a separate way to define a method to translate
    things... so we just need to mark up the text so that it can be
    extracted, not so that it's actually run through gettext.
    """
    return string