# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/benchmarks/naive.py
# Compiled at: 2018-04-27 11:38:22
# Size of source mod 2**32: 437 bytes
from pyFTS.common import fts

class Naive(fts.FTS):
    __doc__ = 'Naïve Forecasting method'

    def __init__(self, **kwargs):
        (super(Naive, self).__init__)(order=1, name='Naive', **kwargs)
        self.name = 'Naïve Model'
        self.detail = 'Naïve Model'
        self.benchmark_only = True
        self.is_high_order = False

    def forecast(self, data, **kwargs):
        return data