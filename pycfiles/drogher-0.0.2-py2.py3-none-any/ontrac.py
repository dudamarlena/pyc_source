# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jbittel/code/drogher/build/lib/drogher/package/ontrac.py
# Compiled at: 2016-05-26 16:22:48
from .base import Package

class OnTrac(Package):
    barcode_pattern = '^[A-Z][0-9]{14}$'
    shipper = 'OnTrac'

    @property
    def valid_checksum(self):
        chars, check_digit = self.tracking_number[:-1], self.tracking_number[(-1)]
        odd = even = 0
        for i, char in enumerate(chars):
            try:
                num = int(char)
            except ValueError:
                num = (ord(char) - 3) % 10

            if i & 1:
                odd += num
            else:
                even += num

        check = (odd * 2 + even) % 10
        if check != 0:
            check = 10 - check
        return check == int(check_digit)