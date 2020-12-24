# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/spyda/utils.py
# Compiled at: 2013-11-18 22:42:07
"""Utilities"""
import re, sys, htmlentitydefs
from heapq import nlargest
from traceback import format_exc
from difflib import SequenceMatcher
from restclient import GET
from nltk import clean_html as html_to_text
from lxml.html import tostring as doc_to_str
from lxml.html.soupparser import fromstring as html_to_doc
from . import __version__
HEADERS = {'User-Agent': ('{0} v{1}').format(__name__, __version__)}
UNICHAR_REPLACEMENTS = (
 ('\xa0', ' '),
 ('–', '-'),
 ('—', '-'),
 ('‘', '`'),
 ('’', "'"),
 ('…', '...'),
 ('“', '"'),
 ('”', '"'))

def is_url(s):
    return s.find('://') > 0


def dict_to_text(d):
    return ('\n').join(('{0:s}: {1:s}').format(k, v) for k, v in d.items())


def unescape(text):
    """Removes HTML or XML character references and entities from a text string.

    :param text: The HTML (or XML) source text.

    :returns:   The plain text, as a Unicode string, if necessary.
    """

    def fixup(m):
        text = m.group(0)
        if text[:2] == '&#':
            try:
                if text[:3] == '&#x':
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))

            except ValueError:
                pass

        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass

        return text

    return re.sub('&#?\\w+;', fixup, text)


def unichar_to_text(text):
    """Convert some common unicode characters to their plain text equivilent.

    This includes for example left and right double quotes, left and right single quotes, etc.
    """
    for replacement in UNICHAR_REPLACEMENTS:
        text = text.replace(*replacement)

    return text


def get_close_matches(word, possibilities, n=3, cutoff=0.6):
    """Use SequenceMatcher to return list of close matches.

    word is a sequence for which close matches are desired (typically a string).

    possibilities is a list of sequences against which to match word (typically a list of strings).

    Optional arg n (default 3) is the maximum number of close matches to return. n must be > 0.

    Optional arg cutoff (default 0.6) is a float in [0.0, 1.0].
    Possibilities that don't score at least that similar to word are ignored.

    The best (no more than n) matches among the possibilities are returned
    in a list, sorted by similarity score, most similar first.
    """
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff and s.ratio() >= cutoff:
            result.append((x, s.ratio()))

    return nlargest(n, result)


def fetch_url(url):
    response, content = GET(url, headers=HEADERS, resp=True)
    if 'content-type' in response and 'charset=' in response['content-type']:
        charset = response['content-type'].split('charset=')[1]
    else:
        charset = None
    return (response, content.decode(charset) if charset is not None else content)


def log(msg, *args, **kwargs):
    sys.stderr.write(('{0:s}{1:s}').format(msg.format(*args), kwargs.get('n', '\n')))
    sys.stderr.flush()


def error(e):
    log('ERROR: {0:s}', e)
    log(format_exc())


def status(msg, *args):
    log('\r\x1b[K{0:s}', msg.format(*args), n='')


def parse_html(html):
    return html_to_doc(html)


def doc_to_text(doc):
    return unichar_to_text(html_to_text(unescape(doc_to_str(doc))))


def get_links(html, badchars='"\' \x0b\x0c\t\n\r'):
    tags = parse_html(html).cssselect('a')
    hrefs = (tag.get('href') for tag in tags)
    return (href.strip(badchars) for href in hrefs if href is not None)