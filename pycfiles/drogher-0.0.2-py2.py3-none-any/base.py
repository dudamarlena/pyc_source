# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jbittel/code/drogher/build/lib/drogher/package/base.py
# Compiled at: 2016-04-13 10:51:42
import re

class Package(object):
    barcode = ''
    barcode_pattern = ''
    shipper = ''

    def __init__(self, barcode):
        self.barcode = barcode.replace(' ', '')

    def __repr__(self):
        return "%s('%s')" % ('package.' + self.__class__.__name__, self.barcode)

    @property
    def is_valid(self):
        if self.matches_barcode and self.valid_checksum:
            return True
        return False

    @property
    def matches_barcode(self):
        if self.barcode_pattern and self.barcode:
            return bool(re.match(self.barcode_pattern, self.barcode))
        return False

    @property
    def tracking_number(self):
        return self.barcode

    @property
    def valid_checksum(self):
        return False


class Unknown(Package):
    shipper = None