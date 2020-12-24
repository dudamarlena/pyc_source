# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/parser.py
# Compiled at: 2015-11-18 14:57:32
# Size of source mod 2**32: 1390 bytes
from __future__ import unicode_literals
import re
from .models import Emoji, JOINER_CHARS
from .utils import code_point_to_unicode
from .pattern import RE_PATTERN_TEMPLATE
PATTERN = re.compile(RE_PATTERN_TEMPLATE)

def replace(txt, callback):
    """
    Replace all unicode emojis in a given text

    :param str txt: Text source to be parsed
    :param callable callback: A callable that should accept    a instance of :py:class:`Emoji` and    return a str to replace the match
    :return: Parsed text with all the emojis    replaced by the callback result
    :rtype: str
    """

    def func(m):
        return callback(Emoji(unicode=(m.group('emoji'))))

    return re.sub(PATTERN, func, txt)


def normalize(code_points, separator='-'):
    """
    Normalize a code point removing joiner    characters such as emoji variations,    Zero Width Joiner and leading zeros

    :param str code_points: code points separated by an hyphen    or the separator param value
    :param str separator: The separator used to split the code points,    process them and merge them back
    :return: Code points with no joiner chars,    leading zeros, and lower cased.
    :rtype: str
    """
    return separator.join(c.lstrip('0').lower() for c in code_points.split(separator) if code_point_to_unicode(c) not in JOINER_CHARS)