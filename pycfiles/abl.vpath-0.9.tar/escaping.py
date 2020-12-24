# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/errorreporter/util/escaping.py
# Compiled at: 2012-01-03 09:44:45
import re, cgi, urllib, htmlentitydefs, codecs
from StringIO import StringIO
xml_escapes = {'&': '&amp;', 
   '>': '&gt;', 
   '<': '&lt;', 
   '"': '&#34;', 
   "'": '&#39;'}

def html_escape(string):
    return cgi.escape(string, True)


def xml_escape(string):
    return re.sub('([&<"\\\'>])', lambda m: xml_escapes[m.group()], string)


def url_escape(string):
    string = string.encode('utf8')
    return urllib.quote_plus(string)


def url_unescape(string):
    text = urllib.unquote_plus(string)
    if not is_ascii_str(text):
        text = text.decode('utf8')
    return text


def trim(string):
    return string.strip()


def safe_to_unicode(text, multibyte_encodings=[
 'utf-8', 'shift-jis'], eight_bit_encoding='latin1'):
    """
    Attempts a heuristic to convert bytestrings
    to unicode. Not very clever. The 
    """
    if isinstance(text, unicode):
        return text
    for mbe in multibyte_encodings:
        try:
            return text.decode(mbe)
        except UnicodeDecodeError:
            pass

    return text.decode(eight_bit_encoding)


class Decode(object):

    def __getattr__(self, key):

        def decode(x):
            if isinstance(x, unicode):
                return x
            elif not isinstance(x, str):
                return unicode(str(x), encoding=key)
            else:
                return unicode(x, encoding=key)

        return decode


decode = Decode()
_ASCII_re = re.compile('\\A[\\x00-\\x7f]*\\Z')

def is_ascii_str(text):
    return isinstance(text, str) and _ASCII_re.match(text)


class XMLEntityEscaper(object):

    def __init__(self, codepoint2name, name2codepoint):
        self.codepoint2entity = dict([ (c, '&%s;' % n) for (c, n) in codepoint2name.iteritems()
                                     ])
        self.name2codepoint = name2codepoint

    def escape_entities(self, text):
        """Replace characters with their character entity references.

        Only characters corresponding to a named entity are replaced.
        """
        return unicode(text).translate(self.codepoint2entity)

    def __escape(self, m):
        codepoint = ord(m.group())
        try:
            return self.codepoint2entity[codepoint]
        except (KeyError, IndexError):
            return '&#x%X;' % codepoint

    __escapable = re.compile('["&<>]|[^\\x00-\\x7f]')

    def escape(self, text):
        """Replace characters with their character references.

        Replace characters by their named entity references.
        Non-ASCII characters, if they do not have a named entity reference,
        are replaced by numerical character references.

        The return value is guaranteed to be ASCII.
        """
        return self.__escapable.sub(self.__escape, unicode(text)).encode('ascii')

    __characterrefs = re.compile('& (?:\n                                          \\#(\\d+)\n                                          | \\#x([\\da-f]+)\n                                          | ( (?!\\d) [:\\w] [-.:\\w]+ )\n                                          ) ;', re.X | re.UNICODE)

    def __unescape(self, m):
        (dval, hval, name) = m.groups()
        if dval:
            codepoint = int(dval)
        elif hval:
            codepoint = int(hval, 16)
        else:
            codepoint = self.name2codepoint.get(name, 65533)
        if codepoint < 128:
            return chr(codepoint)
        return unichr(codepoint)

    def unescape(self, text):
        """Unescape character references.

        All character references (both entity references and numerical
        character references) are unescaped.
        """
        return self.__characterrefs.sub(self.__unescape, text)


_html_entities_escaper = XMLEntityEscaper(htmlentitydefs.codepoint2name, htmlentitydefs.name2codepoint)
html_entities_escape = _html_entities_escaper.escape_entities
html_entities_unescape = _html_entities_escaper.unescape

def htmlentityreplace_errors(ex):
    r"""An encoding error handler.

    This python `codecs`_ error handler replaces unencodable
    characters with HTML entities, or, if no HTML entity exists for
    the character, XML character references.

    >>> u'The cost was \u20ac12.'.encode('latin1', 'htmlentityreplace')
    'The cost was &euro;12.'
    """
    if isinstance(ex, UnicodeEncodeError):
        bad_text = ex.object[ex.start:ex.end]
        text = _html_entities_escaper.escape(bad_text)
        return (
         unicode(text), ex.end)
    raise ex


codecs.register_error('htmlentityreplace', htmlentityreplace_errors)
DEFAULT_ESCAPES = {'x': 'filters.xml_escape', 
   'h': 'filters.html_escape', 
   'u': 'filters.url_escape', 
   'trim': 'filters.trim', 
   'entity': 'filters.html_entities_escape', 
   'unicode': 'unicode', 
   'decode': 'decode', 
   'str': 'str', 
   'n': 'n'}
ILLEGAL_LOW_CHARS = '[\x01-\x08\x0b-\x0c\x0e-\x1f]'
ILLEGAL_HIGH_CHARS = b'\xef\xbf[\xbe\xbf]'
XML_ILLEGAL_CHAR_PATTERN = re.compile('%s|%s' % (ILLEGAL_LOW_CHARS, ILLEGAL_HIGH_CHARS))
g_cdataCharPatternReq = re.compile('[&<]|]]>')
g_charToEntityReq = {'&': '&amp;', 
   '<': '&lt;', 
   ']]>': ']]&gt;'}
g_cdataCharPattern = re.compile('[&<>"\']|]]>')
g_charToEntity = {'&': '&amp;', 
   '<': '&lt;', 
   '>': '&gt;', 
   '"': '&quot;', 
   "'": '&apos;', 
   ']]>': ']]&gt;'}

def removeIllegalChars(characters):
    if XML_ILLEGAL_CHAR_PATTERN.search(characters):
        characters = XML_ILLEGAL_CHAR_PATTERN.subn(lambda m: '&#%i;' % ord(m.group()), characters)[0]
    return characters


def translateCdata(characters, allEntRefs=None):
    """Translate characters into a legal format."""
    if not characters:
        return ''
    if allEntRefs:
        if g_cdataCharPattern.search(characters):
            new_string = g_cdataCharPattern.subn(lambda m, d=g_charToEntity: d[m.group()], characters)[0]
        else:
            new_string = characters
    elif g_cdataCharPatternReq.search(characters):
        new_string = g_cdataCharPatternReq.subn(lambda m, d=g_charToEntityReq: d[m.group()], characters)[0]
    else:
        new_string = characters
    if XML_ILLEGAL_CHAR_PATTERN.search(new_string):
        new_string = XML_ILLEGAL_CHAR_PATTERN.subn(lambda m: '&#%i;' % ord(m.group()), new_string)[0]
    return new_string