# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/utils/roman.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 2687 bytes
"""Convert to and from Roman numerals"""
__author__ = 'Mark Pilgrim (f8dy@diveintopython.org)'
__version__ = '1.4'
__date__ = '8 August 2001'
__copyright__ = 'Copyright (c) 2001 Mark Pilgrim\n\nThis program is part of "Dive Into Python", a free Python tutorial for\nexperienced programmers.  Visit http://diveintopython.org/ for the\nlatest version.\n\nThis program is free software; you can redistribute it and/or modify\nit under the terms of the Python 2.1.1 license, available at\nhttp://www.python.org/2.1.1/license.html\n'
import re

class RomanError(Exception):
    pass


class OutOfRangeError(RomanError):
    pass


class NotIntegerError(RomanError):
    pass


class InvalidRomanNumeralError(RomanError):
    pass


romanNumeralMap = (('M', 1000), ('CM', 900), ('D', 500), ('CD', 400), ('C', 100), ('XC', 90),
                   ('L', 50), ('XL', 40), ('X', 10), ('IX', 9), ('V', 5), ('IV', 4),
                   ('I', 1))

def toRoman(n):
    """convert integer to Roman numeral"""
    if not 0 < n < 5000:
        raise OutOfRangeError('number out of range (must be 1..4999)')
    if int(n) != n:
        raise NotIntegerError('decimals can not be converted')
    result = ''
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer

    return result


romanNumeralPattern = re.compile("\n    ^                   # beginning of string\n    M{0,4}              # thousands - 0 to 4 M's\n    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),\n                        #            or 500-800 (D, followed by 0 to 3 C's)\n    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),\n                        #        or 50-80 (L, followed by 0 to 3 X's)\n    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),\n                        #        or 5-8 (V, followed by 0 to 3 I's)\n    $                   # end of string\n    ", re.VERBOSE)

def fromRoman(s):
    """convert Roman numeral to integer"""
    if not s:
        raise InvalidRomanNumeralError('Input can not be blank')
    if not romanNumeralPattern.search(s):
        raise InvalidRomanNumeralError('Invalid Roman numeral: %s' % s)
    result = 0
    index = 0
    for numeral, integer in romanNumeralMap:
        while s[index:index + len(numeral)] == numeral:
            result += integer
            index += len(numeral)

    return result