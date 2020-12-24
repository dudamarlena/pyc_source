# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/lib/text.py
# Compiled at: 2016-04-19 10:47:47
import re

def truncate_html(text, truncate_len, truncate_text):
    """Truncates HTML to a certain number of words (not counting tags and
    comments). Closes opened tags if they were correctly closed in the given
    HTML. If text is truncated, truncate_text will be appended to the result.

    Newlines in the HTML are preserved.

    Modified from django.utils.text
    https://github.com/django/django/blob/master/django/utils/text.py

    :param str text: The text to truncate.
    :param str truncate_len: The number of words to shorten the HTML to
    :param int truncate_len: Text like '...' to append to the end of tuncated
        text.

    :returns: The truncated HTML
    :rtype: str
    """
    re_words = re.compile('<.*?>|((?:\\w[-\\w]*|&.*?;)+)', re.U | re.S)
    re_tag = re.compile('<(/)?([^ ]+?)(?:(\\s*/)| .*?)?>', re.S)
    length = truncate_len
    if length <= 0:
        return ''
    html4_singlets = ('br', 'col', 'link', 'base', 'img', 'param', 'area', 'hr', 'input')
    pos = 0
    end_text_pos = 0
    current_len = 0
    open_tags = []
    while current_len <= length:
        m = re_words.search(text, pos)
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
    if truncate_text:
        out += truncate_text
    for tag in open_tags:
        out += ('</{}>').format(tag)

    return out


def clean_markdown(markdown):
    """Formats markdown text for easier plaintext viewing.  Performs the
    following substitutions:

    - Removes bad or empty links
    - Removes images
    - Formats hyperlinks from ``[link](http://adicu.com)`` to
    ``link (http://adicu.com)``.

    :param str markdown: The markdown text to format.

    :returns: the formatted text:
    :rtype: str
    """
    substitutions = [
     ('\\s*\\!\\[[^\\]]*\\]\\([^\\)]*\\)', ''),
     ('\\s*\\[\\s*\\]\\([^\\)]*\\)', ''),
     ('\\[(?P<text>.*)\\]\\((?P<link>http[s]?://[^\\)]*)\\)', '\\1 (\\2)'),
     ('\\[(?P<text>.*)\\]\\((?P<link>[^\\)]*)\\)', '\\1'),
     ('\\*', '')]
    for pattern, repl in substitutions:
        markdown = re.sub(pattern, repl, markdown)

    return markdown