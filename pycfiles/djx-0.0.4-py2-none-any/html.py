# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/html.py
# Compiled at: 2019-02-14 00:35:17
"""HTML utilities suitable for global use."""
from __future__ import unicode_literals
import re
from django.utils import six
from django.utils.encoding import force_str, force_text
from django.utils.functional import keep_lazy, keep_lazy_text
from django.utils.http import RFC3986_GENDELIMS, RFC3986_SUBDELIMS
from django.utils.safestring import SafeData, SafeText, mark_safe
from django.utils.six.moves.urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit
from django.utils.text import normalize_newlines
from .html_parser import HTMLParseError, HTMLParser
TRAILING_PUNCTUATION_CHARS = b'.,:;!'
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('[', ']'), ('&lt;', '&gt;'), ('"', '"'), ("'", "'")]
DOTS = [
 b'&middot;', b'*', b'•', b'&#149;', b'&bull;', b'&#8226;']
unencoded_ampersands_re = re.compile(b'&(?!(\\w+|#\\d+);)')
word_split_re = re.compile(b'([\\s<>"\']+)')
simple_url_re = re.compile(b'^https?://\\[?\\w', re.IGNORECASE)
simple_url_2_re = re.compile(b'^www\\.|^(?!http)\\w[^@]+\\.(com|edu|gov|int|mil|net|org)($|/.*)$', re.IGNORECASE)

@keep_lazy(six.text_type, SafeText)
def escape(text):
    """
    Returns the given text with ampersands, quotes and angle brackets encoded
    for use in HTML.

    This function always escapes its input, even if it's already escaped and
    marked as such. This may result in double-escaping. If this is a concern,
    use conditional_escape() instead.
    """
    return mark_safe(force_text(text).replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;').replace(b'"', b'&quot;').replace(b"'", b'&#39;'))


_js_escapes = {ord(b'\\'): b'\\u005C', 
   ord(b"'"): b'\\u0027', 
   ord(b'"'): b'\\u0022', 
   ord(b'>'): b'\\u003E', 
   ord(b'<'): b'\\u003C', 
   ord(b'&'): b'\\u0026', 
   ord(b'='): b'\\u003D', 
   ord(b'-'): b'\\u002D', 
   ord(b';'): b'\\u003B', 
   ord(b'`'): b'\\u0060', 
   ord(b'\u2028'): b'\\u2028', 
   ord(b'\u2029'): b'\\u2029'}
_js_escapes.update((ord(b'%c' % z), b'\\u%04X' % z) for z in range(32))

@keep_lazy(six.text_type, SafeText)
def escapejs(value):
    """Hex encodes characters for use in JavaScript strings."""
    return mark_safe(force_text(value).translate(_js_escapes))


def conditional_escape(text):
    """
    Similar to escape(), except that it doesn't operate on pre-escaped strings.

    This function relies on the __html__ convention used both by Django's
    SafeData class and by third-party libraries like markupsafe.
    """
    if hasattr(text, b'__html__'):
        return text.__html__()
    else:
        return escape(text)


def format_html(format_string, *args, **kwargs):
    """
    Similar to str.format, but passes all arguments through conditional_escape,
    and calls 'mark_safe' on the result. This function should be used instead
    of str.format or % interpolation to build up small HTML fragments.
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = {k:conditional_escape(v) for k, v in six.iteritems(kwargs)}
    return mark_safe(format_string.format(*args_safe, **kwargs_safe))


def format_html_join(sep, format_string, args_generator):
    """
    A wrapper of format_html, for the common case of a group of arguments that
    need to be formatted using the same format string, and then joined using
    'sep'. 'sep' is also passed through conditional_escape.

    'args_generator' should be an iterator that returns the sequence of 'args'
    that will be passed to format_html.

    Example:

      format_html_join('
', "<li>{} {}</li>", ((u.first_name, u.last_name)
                                                  for u in users))
    """
    return mark_safe(conditional_escape(sep).join(format_html(format_string, *tuple(args)) for args in args_generator))


@keep_lazy_text
def linebreaks(value, autoescape=False):
    """Converts newlines into <p> and <br />s."""
    value = normalize_newlines(force_text(value))
    paras = re.split(b'\n{2,}', value)
    if autoescape:
        paras = [ b'<p>%s</p>' % escape(p).replace(b'\n', b'<br />') for p in paras ]
    else:
        paras = [ b'<p>%s</p>' % p.replace(b'\n', b'<br />') for p in paras ]
    return (b'\n\n').join(paras)


class MLStripper(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def handle_entityref(self, name):
        self.fed.append(b'&%s;' % name)

    def handle_charref(self, name):
        self.fed.append(b'&#%s;' % name)

    def get_data(self):
        return (b'').join(self.fed)


def _strip_once(value):
    """
    Internal tag stripping utility used by strip_tags.
    """
    s = MLStripper()
    try:
        s.feed(value)
    except HTMLParseError:
        return value

    try:
        s.close()
    except HTMLParseError:
        return s.get_data() + s.rawdata

    return s.get_data()


@keep_lazy_text
def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    value = force_text(value)
    while b'<' in value and b'>' in value:
        new_value = _strip_once(value)
        if len(new_value) >= len(value):
            break
        value = new_value

    return value


@keep_lazy_text
def strip_spaces_between_tags(value):
    """Returns the given HTML with spaces between tags removed."""
    return re.sub(b'>\\s+<', b'><', force_text(value))


def smart_urlquote(url):
    """Quotes a URL if it isn't already quoted."""

    def unquote_quote(segment):
        segment = unquote(force_str(segment))
        segment = quote(segment, safe=RFC3986_SUBDELIMS + RFC3986_GENDELIMS + str(b'~'))
        return force_text(segment)

    try:
        scheme, netloc, path, query, fragment = urlsplit(url)
    except ValueError:
        return unquote_quote(url)

    try:
        netloc = netloc.encode(b'idna').decode(b'ascii')
    except UnicodeError:
        return unquote_quote(url)

    if query:
        query_parts = [ (unquote(force_str(q[0])), unquote(force_str(q[1]))) for q in parse_qsl(query, keep_blank_values=True)
                      ]
        query = urlencode(query_parts)
    path = unquote_quote(path)
    fragment = unquote_quote(fragment)
    return urlunsplit((scheme, netloc, path, query, fragment))


@keep_lazy_text
def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """
    Converts any URLs in text into clickable links.

    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.

    If trim_url_limit is not None, the URLs in the link text longer than this
    limit will be truncated to trim_url_limit-3 characters and appended with
    an ellipsis.

    If nofollow is True, the links will get a rel="nofollow" attribute.

    If autoescape is True, the link text and URLs will be autoescaped.
    """
    safe_input = isinstance(text, SafeData)

    def trim_url(x, limit=trim_url_limit):
        if limit is None or len(x) <= limit:
            return x
        return b'%s...' % x[:max(0, limit - 3)]

    def unescape(text, trail):
        """
        If input URL is HTML-escaped, unescape it so as we can safely feed it to
        smart_urlquote. For example:
        http://example.com?x=1&amp;y=&lt;2&gt; => http://example.com?x=1&y=<2>
        """
        unescaped = (text + trail).replace(b'&amp;', b'&').replace(b'&lt;', b'<').replace(b'&gt;', b'>').replace(b'&quot;', b'"').replace(b'&#39;', b"'")
        if trail and unescaped.endswith(trail):
            unescaped = unescaped[:-len(trail)]
        elif trail == b';':
            text += trail
            trail = b''
        return (
         text, unescaped, trail)

    def trim_punctuation(lead, middle, trail):
        """
        Trim trailing and wrapping punctuation from `middle`. Return the items
        of the new state.
        """
        trimmed_something = True
        while trimmed_something:
            trimmed_something = False
            stripped = middle.rstrip(TRAILING_PUNCTUATION_CHARS)
            if middle != stripped:
                trail = middle[len(stripped):] + trail
                middle = stripped
                trimmed_something = True
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead += opening
                    trimmed_something = True
                if middle.endswith(closing) and middle.count(closing) == middle.count(opening) + 1:
                    middle = middle[:-len(closing)]
                    trail = closing + trail
                    trimmed_something = True

        return (
         lead, middle, trail)

    def is_email_simple(value):
        """Return True if value looks like an email address."""
        if b'@' not in value or value.startswith(b'@') or value.endswith(b'@'):
            return False
        try:
            p1, p2 = value.split(b'@')
        except ValueError:
            return False

        if b'.' not in p2 or p2.startswith(b'.'):
            return False
        return True

    words = word_split_re.split(force_text(text))
    for i, word in enumerate(words):
        if b'.' in word or b'@' in word or b':' in word:
            lead, middle, trail = b'', word, b''
            lead, middle, trail = trim_punctuation(lead, middle, trail)
            url = None
            nofollow_attr = b' rel="nofollow"' if nofollow else b''
            if simple_url_re.match(middle):
                middle, middle_unescaped, trail = unescape(middle, trail)
                url = smart_urlquote(middle_unescaped)
            elif simple_url_2_re.match(middle):
                middle, middle_unescaped, trail = unescape(middle, trail)
                url = smart_urlquote(b'http://%s' % middle_unescaped)
            elif b':' not in middle and is_email_simple(middle):
                local, domain = middle.rsplit(b'@', 1)
                try:
                    domain = domain.encode(b'idna').decode(b'ascii')
                except UnicodeError:
                    continue

                url = b'mailto:%s@%s' % (local, domain)
                nofollow_attr = b''
            if url:
                trimmed = trim_url(middle)
                if autoescape and not safe_input:
                    lead, trail = escape(lead), escape(trail)
                    trimmed = escape(trimmed)
                middle = b'<a href="%s"%s>%s</a>' % (escape(url), nofollow_attr, trimmed)
                words[i] = mark_safe(b'%s%s%s' % (lead, middle, trail))
            elif safe_input:
                words[i] = mark_safe(word)
            elif autoescape:
                words[i] = escape(word)
        elif safe_input:
            words[i] = mark_safe(word)
        elif autoescape:
            words[i] = escape(word)

    return (b'').join(words)


def avoid_wrapping(value):
    """
    Avoid text wrapping in the middle of a phrase by adding non-breaking
    spaces where there previously were normal spaces.
    """
    return value.replace(b' ', b'\xa0')


def html_safe(klass):
    """
    A decorator that defines the __html__ method. This helps non-Django
    templates to detect classes whose __str__ methods return SafeText.
    """
    if b'__html__' in klass.__dict__:
        raise ValueError(b"can't apply @html_safe to %s because it defines __html__()." % klass.__name__)
    if six.PY2:
        if b'__unicode__' not in klass.__dict__:
            raise ValueError(b"can't apply @html_safe to %s because it doesn't define __unicode__()." % klass.__name__)
        klass_unicode = klass.__unicode__
        klass.__unicode__ = lambda self: mark_safe(klass_unicode(self))
        klass.__html__ = lambda self: unicode(self)
    else:
        if b'__str__' not in klass.__dict__:
            raise ValueError(b"can't apply @html_safe to %s because it doesn't define __str__()." % klass.__name__)
        klass_str = klass.__str__
        klass.__str__ = lambda self: mark_safe(klass_str(self))
        klass.__html__ = lambda self: str(self)
    return klass