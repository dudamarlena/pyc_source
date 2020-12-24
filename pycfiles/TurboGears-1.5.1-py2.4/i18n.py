# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\i18n.py
# Compiled at: 2011-07-14 06:57:44
"""Internationalization support for TurboGears widgets"""
__all__ = [
 'LocalizableJSLink', 'CalendarLangFileLink']
import os, codecs
from cherrypy import request
from turbogears.i18n import get_locale
from turbogears import startup, config
from turbogears.util import parse_http_accept_header
from turbogears.widgets.base import JSLink, CoreWD, RenderOnlyWD

class LocalizableJSLink(JSLink):
    """Provides a simple way to include language-specific data in your JS code.

    Language file to use is determined from the user's locale or from the 'language'
    parameter. If there is no language file for the language (determined via
    'supported_languages' parameter) than 'default_language' is used.

    """
    __module__ = __name__
    default_language = 'en'
    supported_languages = ['en']
    params = ['default_language', 'language', 'supported_languages']
    params_doc = {'language': 'language code to use  (overrides user locale setting which is the default)', 'default_language': 'language code to use if specified language is not supported', 'supported_languages': 'list of supported language codes (which means corresponding language files exist)'}

    def update_params(self, d):
        super(LocalizableJSLink, self).update_params(d)
        language = d.get('language') or get_locale()
        if language not in self.supported_languages:
            language = self.default_language
        d['link'] = d['link'] % {'lang': language}


class LocalizableJSLinkDesc(CoreWD, RenderOnlyWD):
    __module__ = __name__
    name = 'Localizable JS Link'
    for_widget = LocalizableJSLink('turbogears', 'js/yourscript-%(lang)s.js')


_norm_tag = ('').join([ (c.islower() or c.isdigit() or c == '-') and c or c.isupper() and c.lower() or ' ' for c in map(chr, xrange(256)) ])

def norm_tag(tag):
    """Normalize string to alphanumeric ascii chars, hyphens and underscores.

    The length is limited to 16 characters and other characters are
    collapsed to single underscore, or ignored at the start or end.

    """
    if tag is not None:
        return ('_').join(str(tag)[:16].translate(_norm_tag).split())
    return


def norm_charset(charset):
    """Normalize the name of a character set."""
    if charset is not None:
        charset = norm_tag(charset)
        try:
            charset = norm_tag(codecs.lookup(charset).name)
        except (LookupError, AttributeError):
            pass
        else:
            return charset
    return


class CalendarLangFileLink(LocalizableJSLink):
    """Links to proper calendar.js language file depending on HTTP info."""
    __module__ = __name__
    default_charset = 'utf-8'

    def update_params(self, d):
        languages = parse_http_accept_header(request.headers.get('Accept-Language')) or []
        language = d.get('language')
        if language and language != '*':
            languages.insert(0, language)
        languages = map(norm_tag, languages)
        default_language = norm_tag(self.default_language)
        languages.append(default_language)
        charsets = parse_http_accept_header(request.headers.get('Accept-Charset')) or []
        charsets = map(norm_charset, charsets)
        default_charset = norm_charset(self.default_charset)
        charset = norm_charset(config.get(self.engine_name == 'kid' and 'kid.encoding' or 'genshi.default_encoding'))
        if charset and charset != default_charset:
            charsets.append(charset)
        charsets.append(default_charset)
        path = '/tg_widgets/%s' % self.mod
        base_dir = config.app[path].get('tools.staticdir.dir')
        base_name = 'calendar/lang/calendar-'

        def find_link():
            for lang in languages:
                if not lang or lang == '*':
                    lang = default_language
                base_lang = base_name + lang.replace('-', '_')
                for charset in charsets:
                    if not charset or charset == '*':
                        charset = default_charset
                    file_name = base_lang
                    if charset != default_charset:
                        file_name += '-' + charset.replace('-', '_')
                    file_name += '.js'
                    if os.path.exists(os.path.join(base_dir, file_name)):
                        path = '%s/tg_widgets/%s' % (startup.webpath, self.mod)
                        link = '%s/%s' % (path, file_name)
                        return (link, language, charset)
                    if charset == default_charset:
                        break

        (d['link'], d['language'], d['charset']) = find_link()