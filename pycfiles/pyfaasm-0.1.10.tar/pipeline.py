# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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