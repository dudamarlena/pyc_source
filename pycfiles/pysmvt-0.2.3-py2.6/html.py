# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/utils/html.py
# Compiled at: 2010-05-30 09:35:01
"""HTML utilities suitable for global use."""
import re, string
from pysmvt.utils.safestring import SafeData, mark_safe
from pysmvt.utils.encoding import force_unicode
from pysmvt.utils.functional import allow_lazy
from pysmvt.utils.http import urlquote
LEADING_PUNCTUATION = [
 '(', '<', '&lt;']
TRAILING_PUNCTUATION = ['.', ',', ')', '>', '\n', '&gt;']
DOTS = [
 '&middot;', '*', '•', '&#149;', '&bull;', '&#8226;']
unencoded_ampersands_re = re.compile('&(?!(\\w+|#\\d+);)')
word_split_re = re.compile('(\\s+)')
punctuation_re = re.compile('^(?P<lead>(?:%s)*)(?P<middle>.*?)(?P<trail>(?:%s)*)$' % (
 ('|').join([ re.escape(x) for x in LEADING_PUNCTUATION ]),
 ('|').join([ re.escape(x) for x in TRAILING_PUNCTUATION ])))
simple_email_re = re.compile('^\\S+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9._-]+$')
link_target_attribute_re = re.compile('(<a [^>]*?)target=[^\\s>]+')
html_gunk_re = re.compile('(?:<br clear="all">|<i><\\/i>|<b><\\/b>|<em><\\/em>|<strong><\\/strong>|<\\/?smallcaps>|<\\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile('((?:<p>(?:%s).*?[a-zA-Z].*?</p>\\s*)+)' % ('|').join([ re.escape(x) for x in DOTS ]), re.DOTALL)
trailing_empty_content_re = re.compile('(?:<p>(?:&nbsp;|\\s|<br \\/>)*?</p>\\s*)+\\Z')
del x

def escape(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return mark_safe(force_unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;'))


escape = allow_lazy(escape, unicode)

def conditional_escape(html):
    """
    Similar to escape(), except that it doesn't operate on pre-escaped strings.
    """
    if isinstance(html, SafeData):
        return html
    else:
        return escape(html)


def linebreaks(value, autoescape=False):
    """Converts newlines into <p> and <br />s."""
    value = re.sub('\\r\\n|\\r|\\n', '\n', force_unicode(value))
    paras = re.split('\n{2,}', value)
    if autoescape:
        paras = [ '<p>%s</p>' % escape(p.strip()).replace('\n', '<br />') for p in paras ]
    else:
        paras = [ '<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paras ]
    return ('\n\n').join(paras)


linebreaks = allow_lazy(linebreaks, unicode)

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub('<[^>]*?>', '', force_unicode(value))


strip_tags = allow_lazy(strip_tags)

def strip_spaces_between_tags(value):
    """Returns the given HTML with spaces between tags removed."""
    return re.sub('>\\s+<', '><', force_unicode(value))


strip_spaces_between_tags = allow_lazy(strip_spaces_between_tags, unicode)

def strip_entities(value):
    """Returns the given HTML with all entities (&something;) stripped."""
    return re.sub('&(?:\\w+|#\\d+);', '', force_unicode(value))


strip_entities = allow_lazy(strip_entities, unicode)

def fix_ampersands(value):
    """Returns the given HTML with all unencoded ampersands encoded correctly."""
    return unencoded_ampersands_re.sub('&amp;', force_unicode(value))


fix_ampersands = allow_lazy(fix_ampersands, unicode)

def urlize(text, trim_url_limit=None, nofollow=False, autoescape=False):
    """
    Converts any URLs in text into clickable links.

    Works on http://, https://, www. links and links ending in .org, .net or
    .com. Links can have trailing punctuation (periods, commas, close-parens)
    and leading punctuation (opening parens) and it'll still do the right
    thing.

    If trim_url_limit is not None, the URLs in link text longer than this limit
    will truncated to trim_url_limit-3 characters and appended with an elipsis.

    If nofollow is True, the URLs in link text will get a rel="nofollow"
    attribute.

    If autoescape is True, the link text and URLs will get autoescaped.
    """
    trim_url = lambda x, limit=trim_url_limit: limit is not None and len(x) > limit and '%s...' % x[:max(0, limit - 3)] or x
    safe_input = isinstance(text, SafeData)
    words = word_split_re.split(force_unicode(text))
    nofollow_attr = nofollow and ' rel="nofollow"' or ''
    for (i, word) in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word:
            match = punctuation_re.match(word)
        if match:
            (lead, middle, trail) = match.groups()
            url = None
            if middle.startswith('http://') or middle.startswith('https://'):
                url = urlquote(middle, safe='/&=:;#?+*')
            elif middle.startswith('www.') or '@' not in middle and middle and middle[0] in string.ascii_letters + string.digits and (middle.endswith('.org') or middle.endswith('.net') or middle.endswith('.com')):
                url = urlquote('http://%s' % middle, safe='/&=:;#?+*')
            elif '@' in middle and ':' not in middle and simple_email_re.match(middle):
                url = 'mailto:%s' % middle
                nofollow_attr = ''
            if url:
                trimmed = trim_url(middle)
                if autoescape and not safe_input:
                    lead, trail = escape(lead), escape(trail)
                    url, trimmed = escape(url), escape(trimmed)
                middle = '<a href="%s"%s>%s</a>' % (url, nofollow_attr, trimmed)
                words[i] = mark_safe('%s%s%s' % (lead, middle, trail))
            elif safe_input:
                words[i] = mark_safe(word)
            elif autoescape:
                words[i] = escape(word)
        elif safe_input:
            words[i] = mark_safe(word)
        elif autoescape:
            words[i] = escape(word)

    return ('').join(words)


urlize = allow_lazy(urlize, unicode)

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
    text = normalize_newlines(force_unicode(text))
    text = re.sub('<(/?)\\s*b\\s*>', '<\\1strong>', text)
    text = re.sub('<(/?)\\s*i\\s*>', '<\\1em>', text)
    text = fix_ampersands(text)
    text = link_target_attribute_re.sub('\\1', text)
    text = html_gunk_re.sub('', text)

    def replace_p_tags(match):
        s = match.group().replace('</p>', '</li>')
        for d in DOTS:
            s = s.replace('<p>%s' % d, '<li>')

        return '<ul>\n%s\n</ul>' % s

    text = hard_coded_bullets_re.sub(replace_p_tags, text)
    text = trailing_empty_content_re.sub('', text)
    return text


clean_html = allow_lazy(clean_html, unicode)