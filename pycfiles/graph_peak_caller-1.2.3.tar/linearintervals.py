# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivargry/dev/graph_peak_caller/graph_peak_caller/control/linearintervals.py
# Compiled at: 2018-08-24 06:06:37
import numpy as np

class LinearIntervalCollection(object):

    def __init__(self, starts, ends):
        self.starts = np.asanyarray(starts)
        self.ends = np.asanyarray(ends)
        self.n_intervals = self.starts.size

    def __eq__(self, other):
        if not np.allclose(self.starts, other.starts):
            return False
        print self.ends
        print other.ends
        return np.allclose(self.ends, other.ends)

    def __repr__(self):
        s = (' ').join(str(i) for i in self.starts)
        e = (' ').join(str(i) for i in self.ends)
        return '(%s:%s)' % (s, e)

    def extend_np(self, extension_size):
        return np.add.outer(np.array([-extension_size, extension_size]), self.starts)