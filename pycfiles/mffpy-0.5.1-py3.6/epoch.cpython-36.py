# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/epoch.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 2151 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
from .dict2xml import TEXT

class Epoch:
    __doc__ = 'class describing a recording epoch\n\n    .mff files can be discontinuous.  Each part is described by one `Epoch`\n    instance with properties `Epoch.t0`, `Epoch.dt`, and for convenience\n    the end time `Epoch.t1` of the epoch.\n    '
    _s_per_us = 1e-06

    def __init__(self, beginTime, endTime, firstBlock, lastBlock):
        self.beginTime = beginTime
        self.endTime = endTime
        self.firstBlock = firstBlock
        self.lastBlock = lastBlock

    def add_block(self, duration):
        self.lastBlock += 1
        self.endTime += duration

    @property
    def t0(self):
        """return start time of the epoch in seconds"""
        return self.beginTime * self._s_per_us

    @property
    def t1(self):
        """return end time of the epoch in seconds"""
        return self.t0 + self.dt

    @property
    def dt(self):
        """return duration of the epoch in seconds"""
        return (self.endTime - self.beginTime) * self._s_per_us

    @property
    def block_slice(self):
        """return slice to access data blocks containing the epoch"""
        return slice(self.firstBlock - 1, self.lastBlock)

    def __str__(self):
        return f"Epoch:\n        t0 = {self.t0} sec.; dt = {self.dt} sec.\n        Data in blocks {self.block_slice}"

    @property
    def content(self):
        return {TEXT: {'beginTime':{TEXT: str(self.beginTime)}, 
                'endTime':{TEXT: str(self.endTime)}, 
                'firstBlock':{TEXT: str(self.firstBlock)}, 
                'lastBlock':{TEXT: str(self.lastBlock)}}}