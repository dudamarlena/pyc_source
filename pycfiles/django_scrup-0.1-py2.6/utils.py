# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/scrup/utils.py
# Compiled at: 2010-03-08 15:50:24


class BaseConverter(object):
    """
    Convert numbers from base 10 integers to base X strings and back again.
    The default converts to/from base62 strings.
    
    Based on http://www.djangosnippets.org/snippets/1431/
    """
    decimal_digits = '0123456789'
    base62_digits = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'

    def __init__(self, digits=base62_digits):
        self.digits = digits

    def from_decimal(self, i):
        return self.convert(i, self.decimal_digits, self.digits)

    def to_decimal(self, s):
        return int(self.convert(s, self.digits, self.decimal_digits))

    def convert(number, fromdigits, todigits):
        if str(number)[0] == '-':
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0
        x = 0
        for digit in str(number):
            x = x * len(fromdigits) + fromdigits.index(digit)

        if x == 0:
            res = todigits[0]
        else:
            res = ''
            while x > 0:
                digit = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))

            if neg:
                res = '-' + res
        return res

    convert = staticmethod(convert)