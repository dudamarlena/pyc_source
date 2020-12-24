# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tuitwi/widechartools.py
# Compiled at: 2010-06-30 10:58:42
import sys, unicodedata
WIDE_CHARS = [
 'WF']

def get_wide_chars():
    return WIDE_CHARS[0]


def set_wide_chars(val):
    WIDE_CHARS[0] = val


def adjust_n_width(s, width=0, fill=' ', translate=True):
    u"""
    背景色設定用(bkgdで指定するとズレる)
    幅をnになるよう調整する
    長ければ切り詰め、短ければfillで詰める
    """
    if not isinstance(s, unicode):
        s = unicode(s)
    if width <= 0:
        return s.encode(sys.stdout.encoding)
    (u, i, diff) = ('', 0, 0)
    for c in s:
        diff = 1 if WIDE_CHARS[0].find(unicodedata.east_asian_width(c)) < 0 else 2
        if i + diff > width:
            break
        u += c
        i += diff

    u += fill * (width - i)
    if translate:
        u = u.encode(sys.stdout.encoding)
    return u


def split_from_width(s, max_width, translate=True):
    u"""
    表示幅に従ってmax_width以内ずつにsをsplitする.
    """
    if not isinstance(s, unicode):
        s = unicode(s)
    ret = []
    (length, diff) = (0, 0)
    tmp = ''
    for c in s:
        diff = 1 if WIDE_CHARS[0].find(unicodedata.east_asian_width(c)) < 0 else 2
        if length + diff > max_width:
            ret.append(tmp)
            length = diff
            tmp = c
        else:
            tmp += c
            length += diff

    if tmp:
        ret.append(tmp)
    if translate:
        ret = map(lambda s: s.encode(sys.stdout.encoding), ret)
    return ret