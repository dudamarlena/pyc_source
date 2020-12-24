# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/termprop/termprop/wcwidth.py
# Compiled at: 2014-04-25 02:25:25
import db.unicode6_2.normal, db.unicode6_2.cjk
_normal_pattern_fullwidth = db.unicode6_2.normal.pattern_fullwidth
_normal_pattern_combining = db.unicode6_2.normal.pattern_combining
_cjk_pattern_fullwidth = db.unicode6_2.cjk.pattern_fullwidth
_cjk_pattern_combining = db.unicode6_2.cjk.pattern_combining

def _generate_ucs4_codepoints(run):
    c1 = None
    for s in run:
        c = ord(s)
        if c < 55296:
            yield c
        elif c < 56320:
            c1 = c - 55296 << 10
        elif c < 57344 and c1:
            yield c1 | c - 56320
            c1 = None
        else:
            yield c

    return


def wcwidth(c):
    if c < 32:
        return -1
    elif c < 127:
        return 1
    elif c < 160:
        return -1
    elif c < 65536:
        s = unichr(c)
        if _normal_pattern_combining.match(s):
            return 0
        elif _normal_pattern_fullwidth.match(s):
            return 2
        return 1
    elif c < 127744:
        if c < 127488:
            return 1
        return 2
    elif c < 131072:
        return 1
    elif c < 917504:
        return 2
    return 1


def wcwidth_cjk(c):
    if c < 32:
        return -1
    elif c < 127:
        return 1
    elif c < 160:
        return -1
    elif c < 65536:
        s = unichr(c)
        if _cjk_pattern_combining.match(s):
            return 0
        elif _cjk_pattern_fullwidth.match(s):
            return 2
        return 1
    elif c < 127232:
        return 1
    elif c < 127392:
        if c == 127278:
            return 1
        elif c == 127338:
            return 1
        elif c == 127339:
            return 1
        return 2
    elif c < 127744:
        if c < 127488:
            return 1
        return 2
    elif c < 131072:
        return 1
    return 2


def wcswidth(run):
    n = 0
    for c in _generate_ucs4_codepoints(run):
        width = wcwidth(c)
        if width == -1:
            return -1
        n += width

    return n


def wcswidth_cjk(run):
    n = 0
    for c in _generate_ucs4_codepoints(run):
        width = wcwidth_cjk(c)
        if width == -1:
            return -1
        n += width

    return n