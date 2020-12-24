# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bullseye/replay_capture.py
# Compiled at: 2012-03-03 17:24:45
from traits.api import Str
import numpy as np, glob, itertools
from .capture import BaseCapture

class ReplayCapture(BaseCapture):
    replay_glob = Str

    def __init__(self, replay_glob, **k):
        self.replay_glob = replay_glob
        super(ReplayCapture, self).__init__(**k)

    def setup(self):
        names = glob.glob(self.replay_glob)
        names.sort()
        self.names = itertools.cycle(names)
        self.height, self.width = self.dequeue().shape

    def dequeue(self):
        return np.load(self.names.next())['arr_0']