# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyF3D/pipeline.py
# Compiled at: 2017-02-28 14:15:32
import pyopencl as cl, filters.MedianFilter as mf, warnings

class Pipeline:
    filter_types = {'MedianFilter': mf}

    def __init__(self):
        self.pipeline = []

    def add(self, filter):
        if filter.__class__ in self.filter_types.values():
            self.pipeline.append(filter)
        else:
            warnings.warn('Can only add filters of approved type (make this more informative)', Warning)