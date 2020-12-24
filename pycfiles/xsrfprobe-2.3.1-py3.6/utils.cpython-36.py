# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/utils.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2086 bytes
from difflib import SequenceMatcher

def sameSequence(str1, str2):
    """
    This function is intended to find same sequence
                between str1 and str2.
    """
    seqMatch = SequenceMatcher(None, str1, str2)
    match = seqMatch.find_longest_match(0, len(str1), 0, len(str2))
    if match.size != 0:
        return str1[match.a:match.a + match.size]
    else:
        return ''


def replaceStrIndex(text, index=0, replacement=''):
    """
    This method returns a tampered string by
                    replacement
    """
    return '%s%s%s' % (text[:index], replacement, text[index + 1:])


def checkDuplicates(iterable):
    """
    This function works as a byte sequence checker for
            tuples passed onto this function.
    """
    seen = set()
    for x in iterable:
        if x in seen:
            return True
        seen.add(x)

    return False


def byteString(s, encoding='utf8'):
    """
    Return a byte-string version of 's',
            Encoded as utf-8.
    """
    try:
        s = s.encode(encoding)
    except (UnicodeEncodeError, UnicodeDecodeError):
        s = str(s)

    return s


def subSequence(str1, str2):
    """
    Returns whether 'str1' and 'str2' are subsequence
                    of one another.
    """
    j = 0
    i = 0
    m = len(str1)
    n = len(str2)
    while j < m and i < n:
        if str1[j] == str2[i]:
            j = j + 1
        i = i + 1

    return j == m