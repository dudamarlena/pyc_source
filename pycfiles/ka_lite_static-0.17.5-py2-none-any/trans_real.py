# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/translation/trans_real.py
# Compiled at: 2018-07-11 18:15:30
"""Translation helper functions."""
from __future__ import unicode_literals
import locale, os, re, sys, gettext as gettext_module
from threading import local
from django.utils.importlib import import_module
from django.utils.encoding import force_str, force_text
from django.utils._os import upath
from django.utils.safestring import mark_safe, SafeData
from django.utils import six
from django.utils.six import StringIO
_translations = {}
_active = local()
_default = None
_accepted = {}
CONTEXT_SEPARATOR = b'\x04'
accept_language_re = re.compile(b'\n        ([A-Za-z]{1,8}(?:-[A-Za-z0-9]{1,8})*|\\*)      # "en", "en-au", "x-y-z", "es-419", "*"\n        (?:\\s*;\\s*q=(0(?:\\.\\d{,3})?|1(?:.0{,3})?))?   # Optional "q=1.00", "q=0.8"\n        (?:\\s*,\\s*|$)                                 # Multiple accepts per header.\n        ', re.VERBOSE)
language_code_prefix_re = re.compile(b'^/([\\w-]+)(/|$)')

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
    """

    def __init__(self, *args, **kw):
        gettext_module.GNUTranslations.__init__(self, *args, **kw)
        self.set_output_charset(b'utf-8')
        self.django_output_charset = b'utf-8'
        self.__language = b'??'

    def merge(self, other):
        self._catalog.update(other._catalog)

    def set_language(self, language):
        self.__language = language
        self.__to_language = to_language(language)

    def language(self):
        return self.__language

    def to_language(self):
        return self.__to_language

    def __repr__(self):
        return b'<DjangoTranslation lang:%s>' % self.__language


def translation(language):
    """
    Returns a translation object.

    This translation object will be constructed out of multiple GNUTranslations
    objects by merging their catalogs. It will construct a object for the
    requested language and add a fallback to the default language, if it's
    different from the requested language.
    """
    global _translations
    t = _translations.get(language, None)
    if t is not None:
        return t
    else:
        from django.conf import settings
        globalpath = os.path.join(os.path.dirname(upath(sys.modules[settings.__module__].__file__)), b'locale')

        def _fetch(lang, fallback=None):
            res = _translations.get(lang, None)
            if res is not None:
                return res
            else:
                loc = to_locale(lang)

                def _translation(path):
                    try:
                        t = gettext_module.translation(b'django', path, [loc], DjangoTranslation)
                        t.set_language(lang)
                        return t
                    except IOError:
                        return

                    return

                res = _translation(globalpath)
                base_lang = lambda x: x.split(b'-', 1)[0]
                if base_lang(lang) in [ base_lang(trans) for trans in _translations ]:
                    res._info = res._info.copy()
                    res._catalog = res._catalog.copy()

                def _merge(path):
                    t = _translation(path)
                    if t is not None:
                        if res is None:
                            return t
                        res.merge(t)
                    return res

                for appname in reversed(settings.INSTALLED_APPS):
                    app = import_module(appname)
                    apppath = os.path.join(os.path.dirname(upath(app.__file__)), b'locale')
                    if os.path.isdir(apppath):
                        res = _merge(apppath)

                for localepath in reversed(settings.LOCALE_PATHS):
                    if os.path.isdir(localepath):
                        res = _merge(localepath)

                if res is None:
                    if fallback is not None:
                        res = fallback
                    else:
                        return gettext_module.NullTranslations()
                _translations[lang] = res
                return res

        default_translation = _fetch(settings.LANGUAGE_CODE)
        current_translation = _fetch(language, fallback=default_translation)
        return current_translation


def activate(language):
    """
    Fetches the translation object for a given tuple of application name and
    language and installs it as the current translation object for the current
    thread.
    """
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


def get_language():
    """Returns the currently selected language."""
    t = getattr(_active, b'value', None)
    if t is not None:
        try:
            return t.to_language()
        except AttributeError:
            pass

    from django.conf import settings
    return settings.LANGUAGE_CODE


def get_language_bidi():
    """
    Returns selected language's BiDi layout.

    * False = left-to-right layout
    * True = right-to-left layout
    """
    from django.conf import settings
    base_lang = get_language().split(b'-')[0]
    return base_lang in settings.LANGUAGES_BIDI


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
            from django.conf import settings
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
    t = getattr(_active, b'value', None)
    if t is not None:
        result = getattr(t, translation_function)(eol_message)
    else:
        if _default is None:
            from django.conf import settings
            _default = translation(settings.LANGUAGE_CODE)
        result = getattr(_default, translation_function)(eol_message)
    if isinstance(message, SafeData):
        return mark_safe(result)
    else:
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
        result = message
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
            from django.conf import settings
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
    msgs_with_ctxt = (b'%s%s%s' % (context, CONTEXT_SEPARATOR, singular),
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
    from django.conf import settings
    globalpath = os.path.join(os.path.dirname(upath(sys.modules[settings.__module__].__file__)), b'locale')
    return [globalpath] + list(settings.LOCALE_PATHS)


def check_for_language(lang_code):
    """
    Checks whether there is a global language file for the given language
    code. This is used to decide whether a user-provided language is
    available. This is only used for language codes from either the cookies
    or session and during format localization.
    """
    for path in all_locale_paths():
        if gettext_module.find(b'django', path, [to_locale(lang_code)]) is not None:
            return True

    return False


def get_language_from_path(path, supported=None):
    """
    Returns the language-code if there is a valid language-code
    found in the `path`.
    """
    if supported is None:
        from django.conf import settings
        supported = dict(settings.LANGUAGES)
    regex_match = language_code_prefix_re.match(path)
    if regex_match:
        lang_code = regex_match.group(1)
        if lang_code in supported and check_for_language(lang_code):
            return lang_code
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
    global _accepted
    from django.conf import settings
    supported = dict(settings.LANGUAGES)
    if check_path:
        lang_code = get_language_from_path(request.path_info, supported)
        if lang_code is not None:
            return lang_code
    if hasattr(request, b'session'):
        lang_code = request.session.get(b'django_language', None)
        if lang_code in supported and lang_code is not None and check_for_language(lang_code):
            return lang_code
    lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if lang_code and lang_code not in supported:
        lang_code = lang_code.split(b'-')[0]
    if lang_code and lang_code in supported and check_for_language(lang_code):
        return lang_code
    else:
        accept = request.META.get(b'HTTP_ACCEPT_LANGUAGE', b'')
        for accept_lang, unused in parse_accept_lang_header(accept):
            if accept_lang == b'*':
                break
            normalized = locale.locale_alias.get(to_locale(accept_lang, True))
            if not normalized:
                continue
            normalized = normalized.split(b'.')[0]
            if normalized in _accepted:
                return _accepted[normalized]
            for lang, dirname in ((accept_lang, normalized),
             (
              accept_lang.split(b'-')[0], normalized.split(b'_')[0])):
                if lang.lower() not in supported:
                    continue
                for path in all_locale_paths():
                    if os.path.exists(os.path.join(path, dirname, b'LC_MESSAGES', b'django.mo')):
                        _accepted[normalized] = lang
                        return lang

        return settings.LANGUAGE_CODE


dot_re = re.compile(b'\\S')

def blankout(src, char):
    """
    Changes every non-whitespace character to the given char.
    Used in the templatize function.
    """
    return dot_re.sub(char, src)


context_re = re.compile(b'^\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\'))\\s*')
inline_re = re.compile(b'^\\s*trans\\s+((?:"[^"]*?")|(?:\'[^\']*?\'))(\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\')))?\\s*')
block_re = re.compile(b'^\\s*blocktrans(\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\')))?(?:\\s+|$)')
endblock_re = re.compile(b'^\\s*endblocktrans$')
plural_re = re.compile(b'^\\s*plural$')
constant_re = re.compile(b'_\\(((?:".*?")|(?:\'.*?\'))\\)')
one_percent_re = re.compile(b'(?<!%)%(?!%)')

def templatize(src, origin=None):
    """
    Turns a Django template into something that is understood by xgettext. It
    does so by translating the Django translation tags into standard gettext
    function invocations.
    """
    from django.conf import settings
    from django.template import Lexer, TOKEN_TEXT, TOKEN_VAR, TOKEN_BLOCK, TOKEN_COMMENT, TRANSLATOR_COMMENT_MARK
    src = force_text(src, settings.FILE_CHARSET)
    out = StringIO()
    message_context = None
    intrans = False
    inplural = False
    singular = []
    plural = []
    incomment = False
    comment = []
    for t in Lexer(src, origin).tokenize():
        if incomment:
            if t.token_type == TOKEN_BLOCK and t.contents == b'endcomment':
                content = (b'').join(comment)
                translators_comment_start = None
                for lineno, line in enumerate(content.splitlines(True)):
                    if line.lstrip().startswith(TRANSLATOR_COMMENT_MARK):
                        translators_comment_start = lineno

                for lineno, line in enumerate(content.splitlines(True)):
                    if translators_comment_start is not None and lineno >= translators_comment_start:
                        out.write(b' # %s' % line)
                    else:
                        out.write(b' #\n')

                incomment = False
                comment = []
            else:
                comment.append(t.contents)
        elif intrans:
            if t.token_type == TOKEN_BLOCK:
                endbmatch = endblock_re.match(t.contents)
                pluralmatch = plural_re.match(t.contents)
                if endbmatch:
                    if inplural:
                        if message_context:
                            out.write(b' npgettext(%r, %r, %r,count) ' % (message_context, (b'').join(singular), (b'').join(plural)))
                        else:
                            out.write(b' ngettext(%r, %r, count) ' % ((b'').join(singular), (b'').join(plural)))
                        for part in singular:
                            out.write(blankout(part, b'S'))

                        for part in plural:
                            out.write(blankout(part, b'P'))

                    else:
                        if message_context:
                            out.write(b' pgettext(%r, %r) ' % (message_context, (b'').join(singular)))
                        else:
                            out.write(b' gettext(%r) ' % (b'').join(singular))
                        for part in singular:
                            out.write(blankout(part, b'S'))

                    message_context = None
                    intrans = False
                    inplural = False
                    singular = []
                    plural = []
                elif pluralmatch:
                    inplural = True
                else:
                    filemsg = b''
                    if origin:
                        filemsg = b'file %s, ' % origin
                    raise SyntaxError(b'Translation blocks must not include other block tags: %s (%sline %d)' % (t.contents, filemsg, t.lineno))
            elif t.token_type == TOKEN_VAR:
                if inplural:
                    plural.append(b'%%(%s)s' % t.contents)
                else:
                    singular.append(b'%%(%s)s' % t.contents)
            elif t.token_type == TOKEN_TEXT:
                contents = one_percent_re.sub(b'%%', t.contents)
                if inplural:
                    plural.append(contents)
                else:
                    singular.append(contents)
        elif t.token_type == TOKEN_BLOCK:
            imatch = inline_re.match(t.contents)
            bmatch = block_re.match(t.contents)
            cmatches = constant_re.findall(t.contents)
            if imatch:
                g = imatch.group(1)
                if g[0] == b'"':
                    g = g.strip(b'"')
                elif g[0] == b"'":
                    g = g.strip(b"'")
                g = one_percent_re.sub(b'%%', g)
                if imatch.group(2):
                    context_match = context_re.match(imatch.group(2))
                    message_context = context_match.group(1)
                    if message_context[0] == b'"':
                        message_context = message_context.strip(b'"')
                    elif message_context[0] == b"'":
                        message_context = message_context.strip(b"'")
                    out.write(b' pgettext(%r, %r) ' % (message_context, g))
                    message_context = None
                else:
                    out.write(b' gettext(%r) ' % g)
            elif bmatch:
                for fmatch in constant_re.findall(t.contents):
                    out.write(b' _(%s) ' % fmatch)

                if bmatch.group(1):
                    context_match = context_re.match(bmatch.group(1))
                    message_context = context_match.group(1)
                    if message_context[0] == b'"':
                        message_context = message_context.strip(b'"')
                    elif message_context[0] == b"'":
                        message_context = message_context.strip(b"'")
                intrans = True
                inplural = False
                singular = []
                plural = []
            elif cmatches:
                for cmatch in cmatches:
                    out.write(b' _(%s) ' % cmatch)

            elif t.contents == b'comment':
                incomment = True
            else:
                out.write(blankout(t.contents, b'B'))
        elif t.token_type == TOKEN_VAR:
            parts = t.contents.split(b'|')
            cmatch = constant_re.match(parts[0])
            if cmatch:
                out.write(b' _(%s) ' % cmatch.group(1))
            for p in parts[1:]:
                if p.find(b':_(') >= 0:
                    out.write(b' %s ' % p.split(b':', 1)[1])
                else:
                    out.write(blankout(p, b'F'))

        elif t.token_type == TOKEN_COMMENT:
            out.write(b' # %s' % t.contents)
        else:
            out.write(blankout(t.contents, b'X'))

    return force_str(out.getvalue())


def parse_accept_lang_header(lang_string):
    """
    Parses the lang_string, which is the body of an HTTP Accept-Language
    header, and returns a list of (lang, q-value), ordered by 'q' values.

    Any format errors in lang_string results in an empty list being returned.
    """
    result = []
    pieces = accept_language_re.split(lang_string)
    if pieces[(-1)]:
        return []
    for i in range(0, len(pieces) - 1, 3):
        first, lang, priority = pieces[i:i + 3]
        if first:
            return []
        priority = priority and float(priority) or 1.0
        result.append((lang, priority))

    result.sort(key=lambda k: k[1], reverse=True)
    return result