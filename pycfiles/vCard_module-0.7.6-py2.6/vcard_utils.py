# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vcard/vcard_utils.py
# Compiled at: 2010-05-07 09:20:22
"""General purpose utility functions"""
import re

def find_unescaped(text, char, escape_char='\\'):
    r"""
    Find occurrence of an unescaped character.

    @param text: String
    @param char: Character to find
    @param escape_char: Escape character
    @return: Index of first match, None if no match
    
    Examples:
    >>> find_unescaped('BEGIN:VCARD', ':')
    5
    >>> find_unescaped('foo\\,bar,baz', ',')
    8
    >>> find_unescaped(r'foo\,bar,baz', ',')
    8
    >>> find_unescaped('foo\\\\,bar,baz', ',')
    5
    >>> find_unescaped('foo,bar,baz', ':')
    >>> find_unescaped('foo\\,bar\\,baz', ',')
    """
    unescaped_regex = '(?<!' + escape_char + escape_char + ')' + '(?:' + escape_char + escape_char + escape_char + escape_char + ')*' + '(' + char + ')'
    regex = re.compile(unescaped_regex)
    char_match = regex.search(text)
    if char_match is None:
        return
    else:
        return char_match.start(1)


def split_unescaped(text, separator, escape_char='\\\\'):
    """
    Find strings separated by an unescaped character.

    @param text: String
    @param separator: Separator
    @param escape_char: Escape character
    @return: List of strings between separators, excluding the separator
    """
    result = []
    while True:
        index = find_unescaped(text, separator, escape_char)
        if index is not None:
            result.append(text[:index])
            text = text[index + 1:]
        else:
            result.append(text)
            return result

    return