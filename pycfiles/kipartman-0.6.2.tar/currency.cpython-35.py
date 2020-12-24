# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/currency/currency.py
# Compiled at: 2017-12-13 06:03:25
# Size of source mod 2**32: 940 bytes
import json, urllib
from multiprocessing import Pool

class Currency(object):

    def __init__(self, base):
        self.base = base
        self.load()
        pool = Pool(processes=1)

    def load(self):
        data = urllib.urlopen('http://api.fixer.io/latest?base=' + self.base).read()
        self.currencies = json.loads(data)
        print('Currencies: ', self.currencies)

    def convert(self, value, source, target):
        rates = self.currencies['rates']
        if source == self.base:
            rate_source_base = 1
        else:
            rate_source_base = rates[source]
        if target == self.base:
            rate_source_target = 1
        else:
            rate_source_target = rates[target]
        res = 0
        res = value / rate_source_base
        res = res * rate_source_target
        return res