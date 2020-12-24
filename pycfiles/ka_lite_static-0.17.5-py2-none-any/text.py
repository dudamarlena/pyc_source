# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/text.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import re, unicodedata, warnings
from gzip import GzipFile
from io import BytesIO
from django.utils.encoding import force_text
from django.utils.functional import allow_lazy, SimpleLazyObject
from django.utils import six
from django.utils.six.moves import html_entities
from django.utils.translation import ugettext_lazy, ugettext as _, pgettext
from django.utils.safestring import mark_safe
if not six.PY3:
    from django.utils.encoding import force_unicode
capfirst = lambda x: x and force_text(x)[0].upper() + force_text(x)[1:]
capfirst = allow_lazy(capfirst, six.text_type)
re_words = re.compile(b'&.*?;|<.*?>|(\\w[\\w-]*)', re.U | re.S)
re_tag = re.compile(b'<(/)?([^ ]+?)(?: (/)| .*?)?>', re.S)

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks and most spaces in
    the text. Expects that existing line breaks are posix newlines.
    """
    text = force_text(text)

    def _generator():
        it = iter(text.split(b' '))
        word = next(it)
        yield word
        pos = len(word) - word.rfind(b'\n') - 1
        for word in it:
            if b'\n' in word:
                lines = word.split(b'\n')
            else:
                lines = (
                 word,)
            pos += len(lines[0]) + 1
            if pos > width:
                yield b'\n'
                pos = len(lines[(-1)])
            else:
                yield b' '
                if len(lines) > 1:
                    pos = len(lines[(-1)])
            yield word

    return (b'').join(_generator())


wrap = allow_lazy(wrap, six.text_type)

class Truncator(SimpleLazyObject):
    """
    An object used to truncate text, either by characters or words.
    """

    def __init__(self, text):
        super(Truncator, self).__init__(lambda : force_text(text))

    def add_truncation_text(self, text, truncate=None):
        if truncate is None:
            truncate = pgettext(b'String to return when truncating text', b'%(truncated_text)s...')
        truncate = force_text(truncate)
        if b'%(truncated_text)s' in truncate:
            return truncate % {b'truncated_text': text}
        else:
            if text.endswith(truncate):
                return text
            return b'%s%s' % (text, truncate)

    def chars(self, num, truncate=None):
        """
        Returns the text truncated to be no longer than the specified number
        of characters.

        Takes an optional argument of what should be used to notify that the
        string has been truncated, defaulting to a translatable string of an
        ellipsis (...).
        """
        length = int(num)
        text = unicodedata.normalize(b'NFC', self._wrapped)
        truncate_len = length
        for char in self.add_truncation_text(b'', truncate):
            if not unicodedata.combining(char):
                truncate_len -= 1
                if truncate_len == 0:
                    break

        s_len = 0
        end_index = None
        for i, char in enumerate(text):
            if unicodedata.combining(char):
                continue
            s_len += 1
            if end_index is None and s_len > truncate_len:
                end_index = i
            if s_len > length:
                return self.add_truncation_text(text[:end_index or 0], truncate)

        return text

    chars = allow_lazy(chars)

    def words(self, num, truncate=None, html=False):
        """
        Truncates a string after a certain number of words. Takes an optional
        argument of what should be used to notify that the string has been
        truncated, defaulting to ellipsis (...).
        """
        length = int(num)
        if html:
            return self._html_words(length, truncate)
        return self._text_words(length, truncate)

    words = allow_lazy(words)

    def _text_words(self, length, truncate):
        """
        Truncates a string after a certain number of words.

        Newlines in the string will be stripped.
        """
        words = self._wrapped.split()
        if len(words) > length:
            words = words[:length]
            return self.add_truncation_text((b' ').join(words), truncate)
        return (b' ').join(words)

    def _html_words(self, length, truncate):
        """
        Truncates HTML to a certain number of words (not counting tags and
        comments). Closes opened tags if they were correctly closed in the
        given HTML.

        Newlines in the HTML are preserved.
        """
        if length <= 0:
            return b''
        html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr',
                          'input')
        pos = 0
        end_text_pos = 0
        words = 0
        open_tags = []
        while words <= length:
            m = re_words.search(self._wrapped, pos)
            if not m:
                break
            pos = m.end(0)
            if m.group(1):
                words += 1
                if words == length:
                    end_text_pos = pos
                continue
            tag = re_tag.match(m.group(0))
            if not tag or end_text_pos:
                continue
            closing_tag, tagname, self_closing = tag.groups()
            tagname = tagname.lower()
            if self_closing or tagname in html4_singlets:
                pass
            elif closing_tag:
                try:
                    i = open_tags.index(tagname)
                except ValueError:
                    pass
                else:
                    open_tags = open_tags[i + 1:]

            else:
                open_tags.insert(0, tagname)

        if words <= length:
            return self._wrapped
        out = self._wrapped[:end_text_pos]
        truncate_text = self.add_truncation_text(b'', truncate)
        if truncate_text:
            out += truncate_text
        for tag in open_tags:
            out += b'</%s>' % tag

        return out


def truncate_words(s, num, end_text=b'...'):
    warnings.warn(b'This function has been deprecated. Use the Truncator class in django.utils.text instead.', category=DeprecationWarning)
    truncate = end_text and b' %s' % end_text or b''
    return Truncator(s).words(num, truncate=truncate)


truncate_words = allow_lazy(truncate_words, six.text_type)

def truncate_html_words(s, num, end_text=b'...'):
    warnings.warn(b'This function has been deprecated. Use the Truncator class in django.utils.text instead.', category=DeprecationWarning)
    truncate = end_text and b' %s' % end_text or b''
    return Truncator(s).words(num, truncate=truncate, html=True)


truncate_html_words = allow_lazy(truncate_html_words, six.text_type)

def get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = force_text(s).strip().replace(b' ', b'_')
    return re.sub(b'(?u)[^-\\w.]', b'', s)


get_valid_filename = allow_lazy(get_valid_filename, six.text_type)

def get_text_list(list_, last_word=ugettext_lazy(b'or')):
    """
    >>> get_text_list(['a', 'b', 'c', 'd'])
    'a, b, c or d'
    >>> get_text_list(['a', 'b', 'c'], 'and')
    'a, b and c'
    >>> get_text_list(['a', 'b'], 'and')
    'a and b'
    >>> get_text_list(['a'])
    'a'
    >>> get_text_list([])
    ''
    """
    if len(list_) == 0:
        return b''
    if len(list_) == 1:
        return force_text(list_[0])
    return b'%s %s %s' % (
     _(b', ').join([ force_text(i) for i in list_ ][:-1]),
     force_text(last_word), force_text(list_[(-1)]))


get_text_list = allow_lazy(get_text_list, six.text_type)

def normalize_newlines(text):
    return force_text(re.sub(b'\\r\\n|\\r|\\n', b'\n', text))


normalize_newlines = allow_lazy(normalize_newlines, six.text_type)

def recapitalize(text):
    """Recapitalizes text, placing caps after end-of-sentence punctuation."""
    text = force_text(text).lower()
    capsRE = re.compile(b'(?:^|(?<=[\\.\\?\\!] ))([a-z])')
    text = capsRE.sub(lambda x: x.group(1).upper(), text)
    return text


recapitalize = allow_lazy(recapitalize)

def phone2numeric(phone):
    """Converts a phone number with letters into its numeric equivalent."""
    char2number = {b'a': b'2', b'b': b'2', b'c': b'2', b'd': b'3', b'e': b'3', b'f': b'3', b'g': b'4', 
       b'h': b'4', b'i': b'4', b'j': b'5', b'k': b'5', b'l': b'5', b'm': b'6', b'n': b'6', 
       b'o': b'6', b'p': b'7', b'q': b'7', b'r': b'7', b's': b'7', b't': b'8', b'u': b'8', 
       b'v': b'8', b'w': b'9', b'x': b'9', b'y': b'9', b'z': b'9'}
    return (b'').join(char2number.get(c, c) for c in phone.lower())


phone2numeric = allow_lazy(phone2numeric)

def compress_string(s):
    zbuf = BytesIO()
    zfile = GzipFile(mode=b'wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    return zbuf.getvalue()


class StreamingBuffer(object):

    def __init__(self):
        self.vals = []

    def write(self, val):
        self.vals.append(val)

    def read(self):
        ret = (b'').join(self.vals)
        self.vals = []
        return ret

    def flush(self):
        pass

    def close(self):
        pass


def compress_sequence(sequence):
    buf = StreamingBuffer()
    zfile = GzipFile(mode=b'wb', compresslevel=6, fileobj=buf)
    yield buf.read()
    for item in sequence:
        zfile.write(item)
        zfile.flush()
        yield buf.read()

    zfile.close()
    yield buf.read()


ustring_re = re.compile(b'([\x80-\uffff])')

def javascript_quote(s, quote_double_quotes=False):

    def fix(match):
        return b'\\u%04x' % ord(match.group(1))

    if type(s) == bytes:
        s = s.decode(b'utf-8')
    elif type(s) != six.text_type:
        raise TypeError(s)
    s = s.replace(b'\\', b'\\\\')
    s = s.replace(b'\r', b'\\r')
    s = s.replace(b'\n', b'\\n')
    s = s.replace(b'\t', b'\\t')
    s = s.replace(b"'", b"\\'")
    if quote_double_quotes:
        s = s.replace(b'"', b'&quot;')
    return str(ustring_re.sub(fix, s))


javascript_quote = allow_lazy(javascript_quote, six.text_type)
smart_split_re = re.compile(b'\n    ((?:\n        [^\\s\'"]*\n        (?:\n            (?:"(?:[^"\\\\]|\\\\.)*" | \'(?:[^\'\\\\]|\\\\.)*\')\n            [^\\s\'"]*\n        )+\n    ) | \\S+)\n', re.VERBOSE)

def smart_split(text):
    r"""
    Generator that splits a string by spaces, leaving quoted phrases together.
    Supports both single and double quotes, and supports escaping quotes with
    backslashes. In the output, strings will keep their initial and trailing
    quote marks and escaped quotes will remain escaped (the results can then
    be further processed with unescape_string_literal()).

    >>> list(smart_split(r'This is "a person\'s" test.'))
    ['This', 'is', '"a person\\\'s"', 'test.']
    >>> list(smart_split(r"Another 'person\'s' test."))
    ['Another', "'person\\'s'", 'test.']
    >>> list(smart_split(r'A "\"funky\" style" test.'))
    ['A', '"\\"funky\\" style"', 'test.']
    """
    text = force_text(text)
    for bit in smart_split_re.finditer(text):
        yield bit.group(0)


smart_split = allow_lazy(smart_split, six.text_type)

def _replace_entity(match):
    text = match.group(1)
    if text[0] == b'#':
        text = text[1:]
        try:
            if text[0] in b'xX':
                c = int(text[1:], 16)
            else:
                c = int(text)
            return six.unichr(c)
        except ValueError:
            return match.group(0)

    else:
        try:
            return six.unichr(html_entities.name2codepoint[text])
        except (ValueError, KeyError):
            return match.group(0)


_entity_re = re.compile(b'&(#?[xX]?(?:[0-9a-fA-F]+|\\w{1,8}));')

def unescape_entities(text):
    return _entity_re.sub(_replace_entity, text)


unescape_entities = allow_lazy(unescape_entities, six.text_type)

def unescape_string_literal(s):
    r"""
    Convert quoted string literals to unquoted strings with escaped quotes and
    backslashes unquoted::

        >>> unescape_string_literal('"abc"')
        'abc'
        >>> unescape_string_literal("'abc'")
        'abc'
        >>> unescape_string_literal('"a \"bc\""')
        'a "bc"'
        >>> unescape_string_literal("'\'ab\' c'")
        "'ab' c"
    """
    if s[0] not in b'"\'' or s[(-1)] != s[0]:
        raise ValueError(b'Not a string literal: %r' % s)
    quote = s[0]
    return s[1:-1].replace(b'\\%s' % quote, quote).replace(b'\\\\', b'\\')


unescape_string_literal = allow_lazy(unescape_string_literal)

def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize(b'NFKD', value).encode(b'ascii', b'ignore').decode(b'ascii')
    value = re.sub(b'[^\\w\\s-]', b'', value).strip().lower()
    return mark_safe(re.sub(b'[-\\s]+', b'-', value))


slugify = allow_lazy(slugify, six.text_type)