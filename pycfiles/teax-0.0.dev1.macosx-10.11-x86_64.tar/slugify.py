# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/teax/utils/slugify.py
# Compiled at: 2016-02-01 10:04:13
import re, unicodedata, types, sys
try:
    from htmlentitydefs import name2codepoint
    _unicode = unicode
    _unicode_type = types.UnicodeType
except ImportError:
    from html.entities import name2codepoint
    _unicode = str
    _unicode_type = str
    unichr = chr

import unidecode
__all__ = [
 'slugify']
CHAR_ENTITY_PATTERN = re.compile('&(%s);' % ('|').join(name2codepoint))
DECIMAL_PATTERN = re.compile('&#(\\d+);')
HEX_PATTERN = re.compile('&#x([\\da-fA-F]+);')
QUOTE_PATTERN = re.compile("[\\']+")
ALLOWED_CHARS_PATTERN = re.compile('[^-a-z0-9]+')
DUPLICATE_DASH_PATTERN = re.compile('-{2,}')
NUMBERS_PATTERN = re.compile('(?<=\\d),(?=\\d)')

def smart_truncate(string, max_length=0, word_boundaries=False, separator=' ', save_order=False):
    """
    Truncate a string.
    :param string (str): string for modification
    :param max_length (int): output string length
    :param word_boundaries (bool):
    :param save_order (bool): if True then word order of output string is like input string
    :param separator (str): separator between words
    :return:
    """
    string = string.strip(separator)
    if not max_length:
        return string
    if len(string) < max_length:
        return string
    if not word_boundaries:
        return string[:max_length].strip(separator)
    if separator not in string:
        return string[:max_length]
    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += ('{0}{1}').format(word, separator)
            elif next_len == max_length:
                truncated += ('{0}').format(word)
                break
            elif save_order:
                break

    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)


def slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False, separator='-', save_order=False, stopwords=()):
    """
    Make a slug from the given text.
    :param text (str): initial text
    :param entities (bool):
    :param decimal (bool):
    :param hexadecimal (bool):
    :param max_length (int): output string length
    :param word_boundary (bool):
    :param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
    :param separator (str): separator between words
    :param stopwords (iterable): words to discount
    :return (str):
    """
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')
    text = QUOTE_PATTERN.sub('-', text)
    text = unidecode.unidecode(text)
    if not isinstance(text, _unicode_type):
        text = _unicode(text, 'utf-8', 'ignore')
    if entities:
        text = CHAR_ENTITY_PATTERN.sub(lambda m: unichr(name2codepoint[m.group(1)]), text)
    if decimal:
        try:
            text = DECIMAL_PATTERN.sub(lambda m: unichr(int(m.group(1))), text)
        except:
            pass

    if hexadecimal:
        try:
            text = HEX_PATTERN.sub(lambda m: unichr(int(m.group(1), 16)), text)
        except:
            pass

    text = unicodedata.normalize('NFKD', text)
    if sys.version_info < (3, ):
        text = text.encode('ascii', 'ignore')
    text = text.lower()
    text = QUOTE_PATTERN.sub('', text)
    text = NUMBERS_PATTERN.sub('', text)
    text = ALLOWED_CHARS_PATTERN.sub('-', text)
    text = DUPLICATE_DASH_PATTERN.sub('-', text).strip('-')
    if stopwords:
        stopwords_lower = [ s.lower() for s in stopwords ]
        words = [ w for w in text.split('-') if w not in stopwords_lower ]
        text = ('-').join(words)
    if max_length > 0:
        text = smart_truncate(text, max_length, word_boundary, '-', save_order)
    if separator != '-':
        text = text.replace('-', separator)
    return text