# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/contamination/instrument.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 1630 bytes
from numpy import ndarray
from .filter import Filter, ClearFilter

class Instrument:

    def __init__(self, name, filters, qes=None):
        self.name = name
        if not all([isinstance(f, Filter) for f in filters]):
            raise AssertionError('All filters must be Filter instances.')
        else:
            self.filters = filters
            self.pb_n = npb = len(filters)
            self.pb_names = [f.name for f in self.filters]
            if qes is not None:
                if isinstance(qes, (tuple, list, ndarray)):
                    assert len(filters) == len(qes), 'Number of QE profiles differs from the number of passbands.'
                    assert all([isinstance(qe, Filter) for qe in qes]), 'All QE profiles must be Filter instances.'
                    self.qes = qes
                elif isinstance(qes, Filter):
                    self.qes = npb * [qes]
            else:
                self.qes = npb * [ClearFilter('QE')]