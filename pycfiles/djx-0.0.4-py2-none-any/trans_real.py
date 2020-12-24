# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/translation/trans_real.py
# Compiled at: 2019-02-14 00:35:17
"""Translation helper functions."""
from __future__ import unicode_literals
import gettext as gettext_module, os, re, sys, warnings
from collections import OrderedDict
from threading import local
from django.apps import apps
from django.conf import settings
from django.conf.locale import LANG_INFO
from django.core.exceptions import AppRegistryNotReady
from django.core.signals import setting_changed
from django.dispatch import receiver
from django.utils import lru_cache, six
from django.utils._os import upath
from django.utils.encoding import force_text
from django.utils.safestring import SafeData, mark_safe
from django.utils.translation import LANGUAGE_SESSION_KEY
_translations = {}
_active = local()
_default = None
CONTEXT_SEPARATOR = b'\x04'
accept_language_re = re.compile(b'\n        ([A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*|\\*)      # "en", "en-au", "x-y-z", "es-419", "*"\n        (?:\\s*;\\s*q=(0(?:\\.\\d{,3})?|1(?:\\.0{,3})?))?  # Optional "q=1.00", "q=0.8"\n        (?:\\s*,\\s*|$)                                 # Multiple accepts per header.\n        ', re.VERBOSE)
language_code_re = re.compile(b'^[a-z]{1,8}(?:-[a-z0-9]{1,8})*(?:@[a-z0-9]{1,20})?$', re.IGNORECASE)
language_code_prefix_re = re.compile(b'^/(\\w+([@-]\\w+)?)(/|$)')

@receiver(setting_changed)
def reset_cache(**kwargs):
    """
    Reset global state when LANGUAGES setting has been changed, as some
    languages should no longer be accepted.
    """
    if kwargs[b'setting'] in ('LANGUAGES', 'LANGUAGE_CODE'):
        check_for_language.cache_clear()
        get_languages.cache_clear()
        get_supported_language_variant.cache_clear()


def to_locale(language, to_lower=False):
    """
    Turns a language name (en-us) into a locale name (en_US). If 'to_lower' is
    True, the last component is lower-cased (en_us).
    """
    p = language.find(b'-')
    if p >= 0:
        if to_lower:
            return language[:p].lower() + b'_' + language[p + 1:].lower()
        else:
            if len(language[p + 1:]) > 2:
                return language[:p].lower() + b'_' + language[(p + 1)].upper() + language[p + 2:].lower()
            return language[:p].lower() + b'_' + language[p + 1:].upper()

    else:
        return language.lower()


def to_language(locale):
    """Turns a locale name (en_US) into a language name (en-us)."""
    p = locale.find(b'_')
    if p >= 0:
        return locale[:p].lower() + b'-' + locale[p + 1:].lower()
    else:
        return locale.lower()


class DjangoTranslation(gettext_module.GNUTranslations):
    """
    This class sets up the GNUTranslations context with regard to output
    charset.

    This translation object will be constructed out of multiple GNUTranslations
    objects by merging their catalogs. It will construct an object for the
    requested language and add a fallback to the default language, if it's
    different from the requested language.
    """
    domain = b'django'

    def __init__(self, language, domain=None, localedirs=None):
        """Create a GNUTranslations() using many locale directories"""
        gettext_module.GNUTranslations.__init__(self)
        if domain is not None:
            self.domain = domain
        self.set_output_charset(b'utf-8')
        self.__language = language
        self.__to_language = to_language(language)
        self.__locale = to_locale(language)
        self._catalog = None
        self.plural = lambda n: int(n != 1)
        if self.domain == b'django':
            if localedirs is not None:
                warnings.warn(b"localedirs is ignored when domain is 'django'.", RuntimeWarning)
                localedirs = None
            self._init_translation_catalog()
        if localedirs:
            for localedir in localedirs:
                translation = self._new_gnu_trans(localedir)
                self.merge(translation)

        else:
            self._add_installed_apps_translations()
        self._add_local_translations()
        if self.__language == settings.LANGUAGE_CODE and self.domain == b'django' and self._catalog is None:
            raise IOError(b'No translation files found for default language %s.' % settings.LANGUAGE_CODE)
        self._add_fallback(localedirs)
        if self._catalog is None:
            self._catalog = {}
        return

    def __repr__(self):
        return b'<DjangoTranslation lang:%s>' % self.__language

    def _new_gnu_trans(self, localedir, use_null_fallback=True):
        """
        Returns a mergeable gettext.GNUTranslations instance.

        A convenience wrapper. By default gettext uses 'fallback=False'.
        Using param `use_null_fallback` to avoid confusion with any other
        references to 'fallback'.
        """
        return gettext_module.translation(domain=self.domain, localedir=localedir, languages=[
         self.__locale], codeset=b'utf-8', fallback=use_null_fallback)

    def _init_translation_catalog(self):
        """Creates a base catalog using global django translations."""
        settingsfile = upath(sys.modules[settings.__module__].__file__)
        localedir = os.path.join(os.path.dirname(settingsfile), b'locale')
        translation = self._new_gnu_trans(localedir)
        self.merge(translation)

    def _add_installed_apps_translations(self):
        """Merges translations from each installed app."""
        try:
            app_configs = reversed(list(apps.get_app_configs()))
        except AppRegistryNotReady:
            raise AppRegistryNotReady(b"The translation infrastructure cannot be initialized before the apps registry is ready. Check that you don't make non-lazy gettext calls at import time.")

        for app_config in app_configs:
            localedir = os.path.join(app_config.path, b'locale')
            if os.path.exists(localedir):
                translation = self._new_gnu_trans(localedir)
                self.merge(translation)

    def _add_local_translations(self):
        """Merges translations defined in LOCALE_PATHS."""
        for localedir in reversed(settings.LOCALE_PATHS):
            translation = self._new_gnu_trans(localedir)
            self.merge(translation)

    def _add_fallback(self, localedirs=None):
        """Sets the GNUTranslations() fallback with the default language."""
        if self.__language == settings.LANGUAGE_CODE or self.__language.startswith(b'en'):
            return
        if self.domain == b'django':
            default_translation = translation(settings.LANGUAGE_CODE)
        else:
            default_translation = DjangoTranslation(settings.LANGUAGE_CODE, domain=self.domain, localedirs=localedirs)
        self.add_fallback(default_translation)

    def merge(self, other):
        """Merge another translation into this catalog."""
        if not getattr(other, b'_catalog', None):
            return
        else:
            if self._catalog is None:
                self.plural = other.plural
                self._info = other._info.copy()
                self._catalog = other._catalog.copy()
            else:
                self._catalog.update(other._catalog)
            return

    def language(self):
        """Returns the translation language."""
        return self.__language

    def to_language(self):
        """Returns the translation language name."""
        return self.__to_language


def translation(language):
    """
    Returns a translation object in the default 'django' domain.
    """
    global _translations
    if language not in _translations:
        _translations[language] = DjangoTranslation(language)
    return _translations[language]


def activate(language):
    """
    Fetches the translation object for a given language and installs it as the
    current translation object for the current thread.
    """
    if not language:
        return
    _active.value = translation(language)


def deactivate():
    """
    Deinstalls the currently active translation object so that further _ calls
    will resolve against the default translation object, again.
    """
    if hasattr(_active, b'value'):
        del _active.value


def deactivate_all():
    """
    Makes the active translation object a NullTranslations() instance. This is
    useful when we want delayed translations to appear as the original string
    for some reason.
    """
    _active.value = gettext_module.NullTranslations()
    _active.value.to_language = lambda *args: None


def get_language():
    """Returns the currently selected language."""
    t = getattr(_active, b'value', None)
    if t is not None:
        try:
            return t.to_language()
        except AttributeError:
            pass

    return settings.LANGUAGE_CODE


def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    lang = get_language()
    if lang is None:
        return False
    else:
        base_lang = get_language().split(b'-')[0]
        return base_lang in settings.LANGUAGES_BIDI
        return


def catalog():
    """
    Returns the current active catalog for further processing.
    This can be used if you need to modify the catalog or want to access the
    whole message catalog instead of just translating one string.
    """
    global _default
    t = getattr(_active, b'value', None)
    if t is not None:
        return t
    else:
        if _default is None:
            _default = translation(settings.LANGUAGE_CODE)
        return _default


def do_translate(message, translation_function):
    """
    Translates 'message' using the given 'translation_function' name -- which
    will be either gettext or ugettext. It uses the current thread to find the
    translation object to use. If no current translation is activated, the
    message will be run through the default translation object.
    """
    global _default
    eol_message = message.replace(str(b'\r\n'), str(b'\n')).replace(str(b'\r'), str(b'\n'))
    if len(eol_message) == 0:
        result = type(message)(b'')
    else:
        _default = _default or translation(settings.LANGUAGE_CODE)
        translation_object = getattr(_active, b'value', _default)
        result = getattr(translation_object, translation_function)(eol_message)
    if isinstance(message, SafeData):
        return mark_safe(result)
    return result


def gettext(message):
    """
    Returns a string of the translation of the message.

    Returns a string on Python 3 and an UTF-8-encoded bytestring on Python 2.
    """
    return do_translate(message, b'gettext')


if six.PY3:
    ugettext = gettext
else:

    def ugettext(message):
        return do_translate(message, b'ugettext')


def pgettext(context, message):
    msg_with_ctxt = b'%s%s%s' % (context, CONTEXT_SEPARATOR, message)
    result = ugettext(msg_with_ctxt)
    if CONTEXT_SEPARATOR in result:
        result = force_text(message)
    return result


def gettext_noop(message):
    """
    Marks strings for translation but doesn't translate them now. This can be
    used to store strings in global variables that should stay in the base
    language (because they might be used externally) and will be translated
    later.
    """
    return message


def do_ntranslate(singular, plural, number, translation_function):
    global _default
    t = getattr(_active, b'value', None)
    if t is not None:
        return getattr(t, translation_function)(singular, plural, number)
    else:
        if _default is None:
            _default = translation(settings.LANGUAGE_CODE)
        return getattr(_default, translation_function)(singular, plural, number)


def ngettext(singular, plural, number):
    """
    Returns a string of the translation of either the singular or plural,
    based on the number.

    Returns a string on Python 3 and an UTF-8-encoded bytestring on Python 2.
    """
    return do_ntranslate(singular, plural, number, b'ngettext')


if six.PY3:
    ungettext = ngettext
else:

    def ungettext(singular, plural, number):
        """
        Returns a unicode strings of the translation of either the singular or
        plural, based on the number.
        """
        return do_ntranslate(singular, plural, number, b'ungettext')


def npgettext(context, singular, plural, number):
    msgs_with_ctxt = (
     b'%s%s%s' % (context, CONTEXT_SEPARATOR, singular),
     b'%s%s%s' % (context, CONTEXT_SEPARATOR, plural),
     number)
    result = ungettext(*msgs_with_ctxt)
    if CONTEXT_SEPARATOR in result:
        result = ungettext(singular, plural, number)
    return result


def all_locale_paths():
    """
    Returns a list of paths to user-provides languages files.
    """
    globalpath = os.path.join(os.path.dirname(upath(sys.modules[settings.__module__].__file__)), b'locale')
    return [globalpath] + list(settings.LOCALE_PATHS)


@lru_cache.lru_cache(maxsize=1000)
def check_for_language(lang_code):
    """
    Checks whether there is a global language file for the given language
    code. This is used to decide whether a user-provided language is
    available.

    lru_cache should have a maxsize to prevent from memory exhaustion attacks,
    as the provided language codes are taken from the HTTP request. See also
    <https://www.djangoproject.com/weblog/2007/oct/26/security-fix/>.
    """
    if lang_code is None or not language_code_re.search(lang_code):
        return False
    for path in all_locale_paths():
        if gettext_module.find(b'django', path, [to_locale(lang_code)]) is not None:
            return True

    return False


@lru_cache.lru_cache()
def get_languages():
    """
    Cache of settings.LANGUAGES in an OrderedDict for easy lookups by key.
    """
    return OrderedDict(settings.LANGUAGES)


@lru_cache.lru_cache(maxsize=1000)
def get_supported_language_variant(lang_code, strict=False):
    """
    Returns the language-code that's listed in supported languages, possibly
    selecting a more generic variant. Raises LookupError if nothing found.

    If `strict` is False (the default), the function will look for an alternative
    country-specific variant when the currently checked is not found.

    lru_cache should have a maxsize to prevent from memory exhaustion attacks,
    as the provided language codes are taken from the HTTP request. See also
    <https://www.djangoproject.com/weblog/2007/oct/26/security-fix/>.
    """
    if lang_code:
        possible_lang_codes = [lang_code]
        try:
            possible_lang_codes.extend(LANG_INFO[lang_code][b'fallback'])
        except KeyError:
            pass

        generic_lang_code = lang_code.split(b'-')[0]
        possible_lang_codes.append(generic_lang_code)
        supported_lang_codes = get_languages()
        for code in possible_lang_codes:
            if code in supported_lang_codes and check_for_language(code):
                return code

        if not strict:
            for supported_code in supported_lang_codes:
                if supported_code.startswith(generic_lang_code + b'-'):
                    return supported_code

    raise LookupError(lang_code)


def get_language_from_path(path, strict=False):
    """
    Returns the language-code if there is a valid language-code
    found in the `path`.

    If `strict` is False (the default), the function will look for an alternative
    country-specific variant when the currently checked is not found.
    """
    regex_match = language_code_prefix_re.match(path)
    if not regex_match:
        return
    else:
        lang_code = regex_match.group(1)
        try:
            return get_supported_language_variant(lang_code, strict=strict)
        except LookupError:
            return

        return


def get_language_from_request(request, check_path=False):
    """
    Analyzes the request to find what language the user wants the system to
    show. Only languages listed in settings.LANGUAGES are taken into account.
    If the user requests a sublanguage where we have a main language, we send
    out the main language.

    If check_path is True, the URL path prefix will be checked for a language
    code, otherwise this is skipped for backwards compatibility.
    """
    if check_path:
        lang_code = get_language_from_path(request.path_info)
        if lang_code is not None:
            return lang_code
    supported_lang_codes = get_languages()
    if hasattr(request, b'session'):
        lang_code = request.session.get(LANGUAGE_SESSION_KEY)
        if lang_code in supported_lang_codes and lang_code is not None and check_for_language(lang_code):
            return lang_code
    lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    try:
        return get_supported_language_variant(lang_code)
    except LookupError:
        pass

    accept = request.META.get(b'HTTP_ACCEPT_LANGUAGE', b'')
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == b'*':
            break
        if not language_code_re.search(accept_lang):
            continue
        try:
            return get_supported_language_variant(accept_lang)
        except LookupError:
            continue

    try:
        return get_supported_language_variant(settings.LANGUAGE_CODE)
    except LookupError:
        return settings.LANGUAGE_CODE

    return


def parse_accept_lang_header(lang_string):
    """
    Parses the lang_string, which is the body of an HTTP Accept-Language
    header, and returns a list of (lang, q-value), ordered by 'q' values.

    Any format errors in lang_string results in an empty list being returned.
    """
    result = []
    pieces = accept_language_re.split(lang_string.lower())
    if pieces[(-1)]:
        return []
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i:i + 3]
        if first:
            return []
        if priority:
            priority = float(priority)
        else:
            priority = 1.0
        result.append((lang, priority))

    result.sort(key=lambda k: k[1], reverse=True)
    return result