# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jbittel/code/drogher/build/lib/drogher/package/fedex.py
# Compiled at: 2016-04-21 16:57:10
import itertools
from .base import Package

class FedEx(Package):
    shipper = 'FedEx'


class FedExExpress(FedEx):
    barcode_pattern = '^\\d{34}$'

    @property
    def tracking_number(self):
        return self.barcode[20:22].lstrip('0') + self.barcode[22:]

    @property
    def valid_checksum(self):
        chars, check_digit = self.tracking_number[:-1], self.tracking_number[(-1)]
        total = 0
        for digit, char in zip(itertools.cycle([1, 3, 7]), reversed(chars)):
            total += int(char) * digit

        return total % 11 % 10 == int(check_digit)


class FedExGround96(FedEx):
    barcode_pattern = '^96\\d{20}$'

    @property
    def tracking_number(self):
        return self.barcode[7:]

    @property
    def valid_checksum(self):
        chars, check_digit = self.tracking_number[:-1], self.tracking_number[(-1)]
        odd = even = 0
        for i, char in enumerate(reversed(chars)):
            if i & 1:
                odd += int(char)
            else:
                even += int(char)

        check = (even * 3 + odd) % 10
        if check != 0:
            check = 10 - check
        return check == int(check_digit)