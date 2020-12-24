# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/medusa/util.py
# Compiled at: 2019-09-16 13:23:31
# Size of source mod 2**32: 1354 bytes
from supervisor.compat import escape

def html_repr(object):
    so = escape(repr(object))
    if hasattr(object, 'hyper_respond'):
        return '<a href="/status/object/%d/">%s</a>' % (id(object), so)
    return so


def progressive_divide(n, parts):
    result = []
    for part in parts:
        n, rem = divmod(n, part)
        result.append(rem)
    else:
        result.append(n)
        return result


def split_by_units(n, units, dividers, format_string):
    divs = progressive_divide(n, dividers)
    result = []
    for i in range(len(units)):
        if divs[i]:
            result.append(format_string % (divs[i], units[i]))
        result.reverse()
        if not result:
            return [
             format_string % (0, units[0])]
        return result


def english_bytes(n):
    return split_by_units(n, ('', 'K', 'M', 'G', 'T'), (1024, 1024, 1024, 1024, 1024), '%d %sB')


def english_time(n):
    return split_by_units(n, ('secs', 'mins', 'hours', 'days', 'weeks', 'years'), (60,
                                                                                   60,
                                                                                   24,
                                                                                   7,
                                                                                   52), '%d %s')