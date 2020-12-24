# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/benchmarks/naive.py
# Compiled at: 2018-04-27 11:38:22
# Size of source mod 2**32: 437 bytes
from pyFTS.common import fts

class Naive(fts.FTS):
    """Naive"""

    def __init__(self, **kwargs):
        (super(Naive, self).__init__)(order=1, name='Naive', **kwargs)
        self.name = 'Naïve Model'
        self.detail = 'Naïve Model'
        self.benchmark_only = True
        self.is_high_order = False

    def forecast(self, data, **kwargs):
        return data