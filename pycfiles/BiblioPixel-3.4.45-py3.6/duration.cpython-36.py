# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/duration.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2628 bytes
"""
Convert a string duration to a number of seconds.
"""
import re
SI_PREFIXES = ((1000000000000000000000000, 'yotta', 'Y'), (1000000000000000000000, 'zetta', 'Z'),
               (1000000000000000000, 'exa', 'E'), (1000000000000000, 'peta', 'P'),
               (1000000000000, 'tera', 'T'), (1000000000, 'giga', 'G'), (1000000, 'mega', 'M'),
               (1000, 'kilo', 'k'), (100, 'hecto', 'h'), (10, 'deka', 'da'), (0.1, 'deci', 'd'),
               (0.01, 'centi', 'c'), (0.001, 'milli', 'm'), (1e-06, 'micro', 'µ'),
               (1e-09, 'nano', 'n'), (1e-12, 'pico', 'p'), (1e-15, 'femto', 'f'),
               (1e-18, 'atto', 'a'), (1e-21, 'zepto', 'z'), (1e-24, 'yocto', 'y'))
SI_SCALES = dict([(p[1], p[0]) for p in SI_PREFIXES] + [(p[2], p[0]) for p in SI_PREFIXES] + [
 [
  'u', 1e-09]])
UNITS = {'week':604800, 
 'day':86400, 
 'hour':3600, 
 'hr':3600, 
 'minute':60, 
 'min':60, 
 'second':1, 
 'sec':1, 
 's':1}
PART_MATCH = re.compile('([0-9.]+)([a-zA-Z]+)').fullmatch

def _get_units(s):
    if s.endswith('ss'):
        raise ValueError('Unknown unit')

    def split_unit(s):
        for u in UNITS:
            if s.endswith(u):
                return (
                 s[:-len(u)], u)

    prefix, unit = s.endswith('s') and split_unit(s[:-1]) or split_unit(s) or (
     s, '')
    if not unit:
        raise ValueError('Unknown unit ' + s)
    scale = UNITS[unit]
    if not prefix:
        return scale
    else:
        if prefix not in SI_SCALES:
            raise ValueError('Unknown metric prefix ' + prefix)
        return SI_SCALES[prefix] * scale


def parse(s):
    """
    Parse a string representing a time interval or duration into seconds,
    or raise an exception

    :param str s: a string representation of a time interval
    :raises ValueError: if ``s`` can't be interpreted as a duration

    """
    parts = s.replace(',', ' ').split()
    if not parts:
        raise ValueError('Cannot parse empty string')
    pieces = []
    for part in parts:
        m = PART_MATCH(part)
        pieces.extend(m.groups() if m else [part])

    if len(pieces) == 1:
        pieces.append('s')
    if len(pieces) % 2:
        raise ValueError('Malformed duration %s: %s: %s' % (s, parts, pieces))
    result = 0
    for number, units in zip(*[iter(pieces)] * 2):
        number = float(number)
        if number < 0:
            raise ValueError('Durations cannot have negative components')
        result += number * _get_units(units)

    return result