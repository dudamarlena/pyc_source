# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/utils/bounds.py
# Compiled at: 2016-12-02 14:15:22
import numpy as np

class bounds(object):

    def __init__(self, min, max):
        self.min = np.array(min)
        self.max = np.array(max)

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_both(self):
        return np.vstack([self.get_min(), self.get_max()])

    def get_list(self):
        return [
         self.get_min(), self.get_max()]