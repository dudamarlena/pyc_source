# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marstr/.local/share/virtualenvs/py-envelopes-g9vmKF97/lib/python3.7/site-packages/envelopes/balance.py
# Compiled at: 2019-06-23 18:58:48
# Size of source mod 2**32: 2162 bytes
import re, decimal
TERM_PATTERN = re.compile('^\\s*(?P<id>[^\\s\\-\\d]+?)??\\s*(?P<magnitude>-?(?:[\\d]*|(?:\\d{1,3}(?:,\\d{3})+))(?:\\.\\d+)?)$')

class Balance(dict):
    __doc__ = ' Holds a collection of assets, and the corresponding magnitudes present.\n    '

    def __init__(self, value='0'):
        chunks = value.split(';')
        for chunk in chunks:
            parsed = TERM_PATTERN.match(chunk)
            if parsed:
                self[parsed.group('id')] = decimal.Decimal(parsed.group('magnitude').replace(',', ''))
            else:
                raise RuntimeError('"{}" is not a valid balance'.format(value))

    def __add__(self, other):
        retval = Balance()
        unseen = set(other.keys())
        for k, v in self.items():
            retval[k] = v + other.get(k, decimal.Decimal('0'))
            unseen.discard(k)

        for k in unseen:
            retval[k] = other[k]

        return retval

    def __sub__(self, other):
        retval = Balance()
        unseen = set(other.keys())
        for k, v in self.items():
            retval[k] = v - other.get(k, decimal.Decimal('0'))
            unseen.discard(k)

        for k in unseen:
            retval[k] = -other[k]

        return retval

    def __eq__(self, other):
        unseen = set(other.keys())
        for k, v in self.items():
            unseen.discard(k)
            if v != other.get(k, decimal.Decimal('0')):
                return False

        for entry in unseen:
            if other[entry] != decimal.Decimal('0'):
                return False

        return True