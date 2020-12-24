# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/i18n.py
# Compiled at: 2010-02-26 13:28:00
"""
Functions to manage internationalisation (i18n):
- initLocale(): setup locales and install Unicode compatible stdout and
  stderr ;
- getTerminalCharset(): guess terminal charset ;
- gettext(text) translate a string to current language. The function always
  returns Unicode string. You can also use the alias: _() ;
- ngettext(singular, plural, count): translate a sentence with singular and
  plural form. The function always returns Unicode string.

WARNING: Loading this module indirectly calls initLocale() which sets
         locale LC_ALL to ''. This is needed to get user preferred locale
         settings.
"""
import hachoir_core.config as config, hachoir_core, locale
from os import path
import sys
from codecs import BOM_UTF8, BOM_UTF16_LE, BOM_UTF16_BE

def _getTerminalCharset():
    """
    Function used by getTerminalCharset() to get terminal charset.

    @see getTerminalCharset()
    """
    try:
        charset = locale.getpreferredencoding()
        if charset:
            return charset
    except (locale.Error, AttributeError):
        pass

    try:
        charset = locale.nl_langinfo(locale.CODESET)
        if charset:
            return charset
    except (locale.Error, AttributeError):
        pass

    if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding:
        return sys.stdout.encoding
    return 'ASCII'


def getTerminalCharset():
    """
    Guess terminal charset using differents tests:
    1. Try locale.getpreferredencoding()
    2. Try locale.nl_langinfo(CODESET)
    3. Try sys.stdout.encoding
    4. Otherwise, returns "ASCII"

    WARNING: Call initLocale() before calling this function.
    """
    try:
        return getTerminalCharset.value
    except AttributeError:
        getTerminalCharset.value = _getTerminalCharset()
        return getTerminalCharset.value


class UnicodeStdout(object):
    __module__ = __name__

    def __init__(self, old_device, charset):
        self.device = old_device
        self.charset = charset

    def flush(self):
        self.device.flush()

    def write(self, text):
        if isinstance(text, unicode):
            text = text.encode(self.charset, 'replace')
        self.device.write(text)

    def writelines(self, lines):
        for text in lines:
            self.write(text)


def initLocale():
    if initLocale.is_done:
        return getTerminalCharset()
    initLocale.is_done = True
    try:
        locale.setlocale(locale.LC_ALL, '')
    except (locale.Error, IOError):
        pass

    charset = getTerminalCharset()
    if config.unicode_stdout and 'readline' not in sys.modules:
        sys.stdout = UnicodeStdout(sys.stdout, charset)
        sys.stderr = UnicodeStdout(sys.stderr, charset)
    return charset


initLocale.is_done = False

def _dummy_gettext(text):
    return unicode(text)


def _dummy_ngettext(singular, plural, count):
    if 1 < abs(count) or not count:
        return unicode(plural)
    else:
        return unicode(singular)


def _initGettext():
    charset = initLocale()
    if config.use_i18n:
        try:
            import gettext
            ok = True
        except ImportError:
            ok = False

    else:
        ok = False
    if not ok:
        return (
         _dummy_gettext, _dummy_ngettext)
    package = hachoir_core.PACKAGE
    locale_dir = path.join(path.dirname(__file__), '..', 'locale')
    gettext.bindtextdomain(package, locale_dir)
    gettext.textdomain(package)
    translate = gettext.gettext
    ngettext = gettext.ngettext
    unicode_gettext = lambda text: unicode(translate(text), charset)
    unicode_ngettext = lambda singular, plural, count: unicode(ngettext(singular, plural, count), charset)
    return (
     unicode_gettext, unicode_ngettext)


UTF_BOMS = (
 (
  BOM_UTF8, 'UTF-8'), (BOM_UTF16_LE, 'UTF-16-LE'), (BOM_UTF16_BE, 'UTF-16-BE'))
CHARSET_CHARACTERS = (
 (
  set(('©®éêèàç').encode('ISO-8859-1')), 'ISO-8859-1'), (set(('©®éêèàç€').encode('ISO-8859-15')), 'ISO-8859-15'), (set(('©®').encode('MacRoman')), 'MacRoman'), (set(('εδηιθκμοΡσςυΈί').encode('ISO-8859-7')), 'ISO-8859-7'))

def guessBytesCharset(bytes, default=None):
    r"""
    >>> guessBytesCharset("abc")
    'ASCII'
    >>> guessBytesCharset("\xEF\xBB\xBFabc")
    'UTF-8'
    >>> guessBytesCharset("abc\xC3\xA9")
    'UTF-8'
    >>> guessBytesCharset("File written by Adobe Photoshop\xA8 4.0\0")
    'MacRoman'
    >>> guessBytesCharset("\xE9l\xE9phant")
    'ISO-8859-1'
    >>> guessBytesCharset("100 \xA4")
    'ISO-8859-15'
    >>> guessBytesCharset('Word \xb8\xea\xe4\xef\xf3\xe7 - Microsoft Outlook 97 - \xd1\xf5\xe8\xec\xdf\xf3\xe5\xe9\xf2 e-mail')
    'ISO-8859-7'
    """
    for (bom_bytes, charset) in UTF_BOMS:
        if bytes.startswith(bom_bytes):
            return charset

    try:
        text = unicode(bytes, 'ASCII', 'strict')
        return 'ASCII'
    except UnicodeDecodeError:
        pass

    try:
        text = unicode(bytes, 'UTF-8', 'strict')
        return 'UTF-8'
    except UnicodeDecodeError:
        pass

    non_ascii_set = set((byte for byte in bytes if ord(byte) >= 128))
    for (characters, charset) in CHARSET_CHARACTERS:
        if characters.issuperset(non_ascii_set):
            return charset

    return default


(gettext, ngettext) = _initGettext()
_ = gettext