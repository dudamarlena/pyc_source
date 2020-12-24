# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/strutil.py
# Compiled at: 2018-01-06 14:43:43


def commonprefix(l):
    cp = []
    for i in range(min(map(len, l))):
        c = l[0][i]
        for s in l[1:]:
            if s[i] != c:
                return ('').join(cp)

        cp.append(c)

    return ('').join(cp)


def commonsuffix(l):
    cp = []
    for i in range(min(map(len, l))):
        c = l[0][(-i - 1)]
        for s in l[1:]:
            if s[(-i - 1)] != c:
                cp.reverse()
                return ('').join(cp)

        cp.append(c)

    cp.reverse()
    return ('').join(cp)


def split_on_newlines(s):
    """
    Splits s on all of the three newline sequences: "
", "
", or "
".
    """
    res = []
    for x in s.split('\r\n'):
        for y in x.split('\r'):
            res.extend(y.split('\n'))

    return res


def pop_trailing_newlines(s):
    """
    @return a copy of s minus any trailing "
"'s or "
"'s
    """
    i = len(s) - 1
    if i < 0:
        return ''
    while s[i] in ('\n', '\r'):
        i = i - 1
        if i < 0:
            return ''

    return s[:i + 1]