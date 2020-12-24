# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/utils.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 718 bytes


def strformat(strings_at, length):
    """
    Returns a string of given length, composed by strings at specified
    positions, as specified by strings_at. The rest is filled with spaces.
    strings_at is a list of tuples of two elements, the first a number,
    the second a string.
    """
    res = ''
    for pos, string in sorted(strings_at, key=lambda x: x[0]):
        res = res[:pos]
        res += ' ' * (pos - len(res))
        res += string

    res = res[:length]
    res += ' ' * (length - len(res))
    return res


def clamp(value, minvalue, maxvalue):
    """
    Returns the value, clamped between min and max value
    if outside that range
    """
    return sorted([minvalue, value, maxvalue])[1]