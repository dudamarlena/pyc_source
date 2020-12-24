# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/glob.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import re
from functools32 import lru_cache

@lru_cache(maxsize=500)
def _translate(pat, doublestar=False):
    i, n = 0, len(pat)
    res = []
    while i < n:
        c = pat[i]
        i = i + 1
        if c == '*':
            if doublestar:
                if pat[i:i + 1] == '*':
                    res.append('.*')
                    i += 1
                else:
                    res.append('[^/]*')
            else:
                res.append('.*')
        elif c == '?':
            res.append('.')
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j + 1
            if j < n and pat[j] == ']':
                j = j + 1
            while j < n and pat[j] != ']':
                j = j + 1

            if j >= n:
                res.append('\\[')
            else:
                stuff = pat[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res.append('[%s]' % stuff)
        else:
            res.append(re.escape(c))

    res.append('\\Z(?ms)')
    return re.compile(('').join(res))


def glob_match(value, pat, doublestar=False, ignorecase=False, path_normalize=False):
    """A beefed up version of fnmatch.fnmatch"""
    if ignorecase:
        value = value.lower()
        pat = pat.lower()
    if path_normalize:
        value = value.replace('\\', '/')
        pat = pat.replace('\\', '/')
    return _translate(pat, doublestar=doublestar).match(value) is not None