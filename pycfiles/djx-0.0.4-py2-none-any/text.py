# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/text.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import re, unicodedata
from gzip import GzipFile
from io import BytesIO
from django.utils import six
from django.utils.encoding import force_text
from django.utils.functional import SimpleLazyObject, keep_lazy, keep_lazy_text, lazy
from django.utils.safestring import SafeText, mark_safe
from django.utils.six.moves import html_entities
from django.utils.translation import pgettext, ugettext as _, ugettext_lazy
if six.PY2:
    from django.utils.encoding import force_unicode

@keep_lazy_text
def capfirst(x):
    """Capitalize the first letter of a string."""
    return x and force_text(x)[0].upper() + force_text(x)[1:]


re_words = re.compile(b'<.*?>|((?:\\w[-\\w]*|&.*?;)+)', re.U | re.S)
re_chars = re.compile(b'<.*?>|(.)', re.U | re.S)
re_tag = re.compile(b'<(/)?(\\S+?)(?:(\\s*/)|\\s.*?)?>', re.S)
re_newlines = re.compile(b'\\r\\n|\\r')
re_camel_case = re.compile(b'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')

@keep_lazy_text
def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks. Expects that
    existing line breaks are posix newlines.

    All white space is preserved except added line breaks consume the space on
    which they break the line.

    Long words are not wrapped, so the output text may have lines longer than
    ``width``.
    """
    text = force_text(text)

    def _generator():
        for line in text.splitlines(True):
            max_width = min(line.endswith(b'\n') and width + 1 or width, width)
            while len(line) > max_width:
                space = line[:max_width + 1].rfind(b' ') + 1
                if space == 0:
                    space = line.find(b' ') + 1
                    if space == 0:
                        yield line
                        line = b''
                        break
                yield b'%s\n' % line[:space - 1]
                line = line[space:]
                max_width = min(line.endswith(b'\n') and width + 1 or width, width)

            if line:
                yield line

    return (b'').join(_generator())


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

    def chars(self, num, truncate=None, html=False):
        """
        Returns the text truncated to be no longer than the specified number
        of characters.

        Takes an optional argument of what should be used to notify that the
        string has been truncated, defaulting to a translatable string of an
        ellipsis (...).
        """
        self._setup()
        length = int(num)
        text = unicodedata.normalize(b'NFC', self._wrapped)
        truncate_len = length
        for char in self.add_truncation_text(b'', truncate):
            if not unicodedata.combining(char):
                truncate_len -= 1
                if truncate_len == 0:
                    break

        if html:
            return self._truncate_html(length, truncate, text, truncate_len, False)
        return self._text_chars(length, truncate, text, truncate_len)

    def _text_chars(self, length, truncate, text, truncate_len):
        """
        Truncates a string after a certain number of chars.
        """
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

    def words(self, num, truncate=None, html=False):
        """
        Truncates a string after a certain number of words. Takes an optional
        argument of what should be used to notify that the string has been
        truncated, defaulting to ellipsis (...).
        """
        self._setup()
        length = int(num)
        if html:
            return self._truncate_html(length, truncate, self._wrapped, length, True)
        return self._text_words(length, truncate)

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

    def _truncate_html(self, length, truncate, text, truncate_len, words):
        """
        Truncates HTML to a certain number of chars (not counting tags and
        comments), or, if words is True, then to a certain number of words.
        Closes opened tags if they were correctly closed in the given HTML.

        Newlines in the HTML are preserved.
        """
        if words and length <= 0:
            return b''
        html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr',
                          'input')
        pos = 0
        end_text_pos = 0
        current_len = 0
        open_tags = []
        regex = re_words if words else re_chars
        while current_len <= length:
            m = regex.search(text, pos)
            if not m:
                break
            pos = m.end(0)
            if m.group(1):
                current_len += 1
                if current_len == truncate_len:
                    end_text_pos = pos
                continue
            tag = re_tag.match(m.group(0))
            if not tag or current_len >= truncate_len:
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

        if current_len <= length:
            return text
        out = text[:end_text_pos]
        truncate_text = self.add_truncation_text(b'', truncate)
        if truncate_text:
            out += truncate_text
        for tag in open_tags:
            out += b'</%s>' % tag

        return out


@keep_lazy_text
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


@keep_lazy_text
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
     _(b', ').join(force_text(i) for i in list_[:-1]),
     force_text(last_word), force_text(list_[(-1)]))


@keep_lazy_text
def normalize_newlines(text):
    """Normalizes CRLF and CR newlines to just LF."""
    text = force_text(text)
    return re_newlines.sub(b'\n', text)


@keep_lazy_text
def phone2numeric(phone):
    """Converts a phone number with letters into its numeric equivalent."""
    char2number = {b'a': b'2', 
       b'b': b'2', b'c': b'2', b'd': b'3', b'e': b'3', b'f': b'3', b'g': b'4', b'h': b'4', 
       b'i': b'4', b'j': b'5', b'k': b'5', b'l': b'5', b'm': b'6', b'n': b'6', b'o': b'6', 
       b'p': b'7', b'q': b'7', b'r': b'7', b's': b'7', b't': b'8', b'u': b'8', b'v': b'8', 
       b'w': b'9', b'x': b'9', b'y': b'9', b'z': b'9'}
    return (b'').join(char2number.get(c, c) for c in phone.lower())


def compress_string(s):
    zbuf = BytesIO()
    with GzipFile(mode=b'wb', compresslevel=6, fileobj=zbuf, mtime=0) as (zfile):
        zfile.write(s)
    return zbuf.getvalue()


class StreamingBuffer(object):

    def __init__(self):
        self.vals = []

    def write(self, val):
        self.vals.append(val)

    def read(self):
        if not self.vals:
            return b''
        ret = (b'').join(self.vals)
        self.vals = []
        return ret

    def flush(self):
        pass

    def close(self):
        pass


def compress_sequence(sequence):
    buf = StreamingBuffer()
    with GzipFile(mode=b'wb', compresslevel=6, fileobj=buf, mtime=0) as (zfile):
        yield buf.read()
        for item in sequence:
            zfile.write(item)
            data = buf.read()
            if data:
                yield data

    yield buf.read()


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

@keep_lazy_text
def unescape_entities(text):
    return _entity_re.sub(_replace_entity, force_text(text))


@keep_lazy_text
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


@keep_lazy(six.text_type, SafeText)
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = force_text(value)
    if allow_unicode:
        value = unicodedata.normalize(b'NFKC', value)
        value = re.sub(b'[^\\w\\s-]', b'', value, flags=re.U).strip().lower()
        return mark_safe(re.sub(b'[-\\s]+', b'-', value, flags=re.U))
    value = unicodedata.normalize(b'NFKD', value).encode(b'ascii', b'ignore').decode(b'ascii')
    value = re.sub(b'[^\\w\\s-]', b'', value).strip().lower()
    return mark_safe(re.sub(b'[-\\s]+', b'-', value))


def camel_case_to_spaces(value):
    """
    Splits CamelCase and converts to lower case. Also strips leading and
    trailing whitespace.
    """
    return re_camel_case.sub(b' \\1', value).strip().lower()


def _format_lazy(format_string, *args, **kwargs):
    """
    Apply str.format() on 'format_string' where format_string, args,
    and/or kwargs might be lazy.
    """
    return format_string.format(*args, **kwargs)


format_lazy = lazy(_format_lazy, six.text_type)