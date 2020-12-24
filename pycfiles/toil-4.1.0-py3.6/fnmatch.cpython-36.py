# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/fnmatch.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 4644 bytes
from __future__ import absolute_import
import re
__all__ = [
 'filter', 'fnmatch', 'fnmatchcase', 'translate']
_cache = {}
_MAXCACHE = 100

def _purge():
    """Clear the pattern cache"""
    _cache.clear()


def fnmatch(name, pat):
    """Test whether FILENAME matches PATTERN.

    Patterns are Unix shell style:

    *       matches everything
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq

    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).

    >>> fnmatch('bar', '*' )
    True
    >>> fnmatch('foo/bar', '*' )
    False
    >>> fnmatch('foo/bar', '**' )
    True
    >>> fnmatch('foo/bar', '*/*' )
    True
    >>> fnmatch('foo/bar', '**/*' )
    True
    >>> fnmatch('/bar', '**/*' )
    True
    >>> fnmatch('/', '**' )
    True
    >>> fnmatch('/', '*' )
    False
    """
    import os
    name = os.path.normcase(name)
    pat = os.path.normcase(pat)
    return fnmatchcase(name, pat)


def filter(names, pat):
    """Return the subset of the list NAMES that match PAT"""
    import os, posixpath
    result = []
    pat = os.path.normcase(pat)
    if pat not in _cache:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _cache.clear()
        _cache[pat] = re.compile(res)
    else:
        match = _cache[pat].match
        if os.path is posixpath:
            for name in names:
                if match(name):
                    result.append(name)

        else:
            for name in names:
                if match(os.path.normcase(name)):
                    result.append(name)

    return result


def fnmatchcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """
    if pat not in _cache:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _cache.clear()
        _cache[pat] = re.compile(res)
    return _cache[pat].match(name) is not None


def translate(pat):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """
    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i += 1
        if c == '*':
            if i < len(pat):
                if pat[i] == '*':
                    i += 1
                    res += '.*'
            else:
                res += '[^/]*'
        else:
            if c == '?':
                res += '.'
            else:
                if c == '[':
                    j = i
                    if j < n:
                        if pat[j] == '!':
                            j += 1
                    if j < n:
                        if pat[j] == ']':
                            j += 1
                    while j < n and pat[j] != ']':
                        j += 1

                    if j >= n:
                        res += '\\['
                    else:
                        stuff = pat[i:j].replace('\\', '\\\\')
                    i = j + 1
                    if stuff[0] == '!':
                        stuff = '^' + stuff[1:]
                    else:
                        if stuff[0] == '^':
                            stuff = '\\' + stuff
                        res = '%s[%s]' % (res, stuff)
                else:
                    res = res + re.escape(c)

    return res + '\\Z(?ms)'