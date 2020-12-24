# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/timer.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 464 bytes
import collections, time, torch

class PyTorchTimer:

    def __init__(self):
        self.ac = collections.defaultdict(int)
        self.t = None

    def tick(self, name):
        torch.cuda.synchronize()
        current_time = time.time()
        if name is not None:
            assert self.t is not None
            self.ac[name] += current_time - self.t
        self.t = current_time

    def __repr__(self):
        return self.ac.__repr__()