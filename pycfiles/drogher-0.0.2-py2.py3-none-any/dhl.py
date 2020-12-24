# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jbittel/code/drogher/build/lib/drogher/package/dhl.py
# Compiled at: 2016-04-08 19:30:31
from .base import Package

class DHL(Package):
    barcode_pattern = '^\\d{10}$'
    shipper = 'DHL'

    @property
    def valid_checksum(self):
        chars, check_digit = self.tracking_number[:-1], self.tracking_number[(-1)]
        return int(chars) % 7 == int(check_digit)