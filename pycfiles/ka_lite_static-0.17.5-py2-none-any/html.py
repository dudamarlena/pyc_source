# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/html.py
# Compiled at: 2018-07-11 18:15:30
"""HTML utilities suitable for global use."""
from __future__ import unicode_literals
import re, string
try:
    from urllib.parse import quote, unquote, urlsplit, urlunsplit
except ImportError:
    from urllib import quote, unquote
    from urlparse import urlsplit, urlunsplit

from django.utils.safestring import SafeData, mark_safe
from django.utils.encoding import force_text, force_str
from django.utils.functional import allow_lazy
from django.utils import six
from django.utils.text import normalize_newlines
TRAILING_PUNCTUATION = [
 b'.', b',', b':', b';', b'.)']
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('[', ']'), ('&lt;', '&gt;')]
DOTS = [
 b'&middot;', b'*', b'•', b'&#149;', b'&bull;', b'&#8226;']
unencoded_ampersands_re = re.compile(b'&(?!(\\w+|#\\d+);)')
word_split_re = re.compile(b'(\\s+)')
simple_url_re = re.compile(b'^https?://\\w', re.IGNORECASE)
simple_url_2_re = re.compile(b'^www\\.|^(?!http)\\w[^@]+\\.(com|edu|gov|int|mil|net|org)$', re.IGNORECASE)
simple_email_re = re.compile(b'^\\S+@\\S+\\.\\S+$')
link_target_attribute_re = re.compile(b'(<a [^>]*?)target=[^\\s>]+')
html_gunk_re = re.compile(b'(?:<br clear="all">|<i><\\/i>|<b><\\/b>|<em><\\/em>|<strong><\\/strong>|<\\/?smallcaps>|<\\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(b'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\\s*)+)' % (b'|').join([ re.escape(x) for x in DOTS ]), re.DOTALL)
trailing_empty_content_re = re.compile(b'(?:<p>(?:&nbsp;|\\s|<br \\/>)*?</p>\\s*)+\\Z')
strip_tags_re = re.compile(b'<[^>]*?>', re.IGNORECASE)

def escape(text):
    """
    Returns the given text with ampersands, quotes and angle brackets encoded for use in HTML.
    """
    return mark_safe(force_text(text).replace(b'&', b'&amp;').replace(b'<', b'&lt;').replace(b'>', b'&gt;').replace(b'"', b'&quot;').replace(b"'", b'&#39;'))


escape = allow_lazy(escape, six.text_type)
_js_escapes = {ord(b'\\'): b'\\u005C', 
   ord(b"'"): b'\\u0027', 
   ord(b'"'): b'\\u0022', 
   ord(b'>'): b'\\u003E', 
   ord(b'<'): b'\\u003C', 
   ord(b'&'): b'\\u0026', 
   ord(b'='): b'\\u003D', 
   ord(b'-'): b'\\u002D', 
   ord(b';'): b'\\u003B', 
   ord(b'\u2028'): b'\\u2028', 
   ord(b'\u2029'): b'\\u2029'}
_js_escapes.update((ord(b'%c' % z), b'\\u%04X' % z) for z in range(32))

def escapejs(value):
    """Hex encodes characters for use in JavaScript strings."""
    return mark_safe(force_text(value).translate(_js_escapes))


escapejs = allow_lazy(escapejs, six.text_type)

def conditional_escape(text):
    """
    Similar to escape(), except that it doesn't operate on pre-escaped strings.
    """
    if isinstance(text, SafeData):
        return text
    else:
        return escape(text)


def format_html(format_string, *args, **kwargs):
    """
    Similar to str.format, but passes all arguments through conditional_escape,
    and calls 'mark_safe' on the result. This function should be used instead
    of str.format or % interpolation to build up small HTML fragments.
    """
    args_safe = map(conditional_escape, args)
    kwargs_safe = dict([ (k, conditional_escape(v)) for k, v in six.iteritems(kwargs)
                       ])
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
', "<li>{0} {1}</li>", ((u.first_name, u.last_name)
                                                  for u in users))

    """
    return mark_safe(conditional_escape(sep).join(format_html(format_string, *tuple(args)) for args in args_generator))


def linebreaks(value, autoescape=False):
    """Converts newlines into <p> and <br />s."""
    value = normalize_newlines(value)
    paras = re.split(b'\n{2,}', value)
    if autoescape:
        paras = [ b'<p>%s</p>' % escape(p).replace(b'\n', b'<br />') for p in paras ]
    else:
        paras = [ b'<p>%s</p>' % p.replace(b'\n', b'<br />') for p in paras ]
    return (b'\n\n').join(paras)


linebreaks = allow_lazy(linebreaks, six.text_type)

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return strip_tags_re.sub(b'', force_text(value))


strip_tags = allow_lazy(strip_tags)

def remove_tags(html, tags):
    """Returns the given HTML with given tags removed."""
    tags = [ re.escape(tag) for tag in tags.split() ]
    tags_re = b'(%s)' % (b'|').join(tags)
    starttag_re = re.compile(b'<%s(/?>|(\\s+[^>]*>))' % tags_re, re.U)
    endtag_re = re.compile(b'</%s>' % tags_re)
    html = starttag_re.sub(b'', html)
    html = endtag_re.sub(b'', html)
    return html


remove_tags = allow_lazy(remove_tags, six.text_type)

def strip_spaces_between_tags(value):
    """Returns the given HTML with spaces between tags removed."""
    return re.sub(b'>\\s+<', b'><', force_text(value))


strip_spaces_between_tags = allow_lazy(strip_spaces_between_tags, six.text_type)

def strip_entities(value):
    """Returns the given HTML with all entities (&something;) stripped."""
    return re.sub(b'&(?:\\w+|#\\d+);', b'', force_text(value))


strip_entities = allow_lazy(strip_entities, six.text_type)

def fix_ampersands(value):
    """Returns the given HTML with all unencoded ampersands encoded correctly."""
    return unencoded_ampersands_re.sub(b'&amp;', force_text(value))


fix_ampersands = allow_lazy(fix_ampersands, six.text_type)

def smart_urlquote(url):
    """Quotes a URL if it isn't already quoted."""
    scheme, netloc, path, query, fragment = urlsplit(url)
    try:
        netloc = netloc.encode(b'idna').decode(b'ascii')
    except UnicodeError:
        pass
    else:
        url = urlunsplit((scheme, netloc, path, query, fragment))

    url = unquote(force_str(url))
    url = quote(url, safe=b"!*'();:@&=+$,/?#[]~")
    return force_text(url)


def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """
    Converts any URLs in text into clickable links.

    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.

    If trim_url_limit is not None, the URLs in link text longer than this limit
    will truncated to trim_url_limit-3 characters and appended with an elipsis.

    If nofollow is True, the URLs in link text will get a rel="nofollow"
    attribute.

    If autoescape is True, the link text and URLs will get autoescaped.
    """
    trim_url = lambda x, limit=trim_url_limit: limit is not None and len(x) > limit and b'%s...' % x[:max(0, limit - 3)] or x
    safe_input = isinstance(text, SafeData)
    words = word_split_re.split(force_text(text))
    for i, word in enumerate(words):
        match = None
        if b'.' in word or b'@' in word or b':' in word:
            lead, middle, trail = b'', word, b''
            for punctuation in TRAILING_PUNCTUATION:
                if middle.endswith(punctuation):
                    middle = middle[:-len(punctuation)]
                    trail = punctuation + trail

            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead = lead + opening
                if middle.endswith(closing) and middle.count(closing) == middle.count(opening) + 1:
                    middle = middle[:-len(closing)]
                    trail = closing + trail

            url = None
            nofollow_attr = b' rel="nofollow"' if nofollow else b''
            if simple_url_re.match(middle):
                url = smart_urlquote(middle)
            elif simple_url_2_re.match(middle):
                url = smart_urlquote(b'http://%s' % middle)
            elif b':' not in middle and simple_email_re.match(middle):
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
                    url, trimmed = escape(url), escape(trimmed)
                middle = b'<a href="%s"%s>%s</a>' % (url, nofollow_attr, trimmed)
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


urlize = allow_lazy(urlize, six.text_type)

def clean_html(text):
    """
    Clean the given HTML.  Specifically, do the following:
        * Convert <b> and <i> to <strong> and <em>.
        * Encode all ampersands correctly.
        * Remove all "target" attributes from <a> tags.
        * Remove extraneous HTML, such as presentational tags that open and
          immediately close and <br clear="all">.
        * Convert hard-coded bullets into HTML unordered lists.
        * Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the
          bottom of the text.
    """
    from django.utils.text import normalize_newlines
    text = normalize_newlines(force_text(text))
    text = re.sub(b'<(/?)\\s*b\\s*>', b'<\\1strong>', text)
    text = re.sub(b'<(/?)\\s*i\\s*>', b'<\\1em>', text)
    text = fix_ampersands(text)
    text = link_target_attribute_re.sub(b'\\1', text)
    text = html_gunk_re.sub(b'', text)

    def replace_p_tags(match):
        s = match.group().replace(b'</p>', b'</li>')
        for d in DOTS:
            s = s.replace(b'<p>%s' % d, b'<li>')

        return b'<ul>\n%s\n</ul>' % s

    text = hard_coded_bullets_re.sub(replace_p_tags, text)
    text = trailing_empty_content_re.sub(b'', text)
    return text


clean_html = allow_lazy(clean_html, six.text_type)