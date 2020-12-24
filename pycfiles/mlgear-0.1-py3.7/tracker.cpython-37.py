# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/mlgear/tracker.py
# Compiled at: 2019-12-27 10:22:07
# Size of source mod 2**32: 447 bytes
from datetime import datetime

class Tracker(object):

    def __init__(self):
        self.start = datetime.now()
        print('Tracker started at {}'.format(self.start))
        self.then = self.start
        self.now = self.start

    def tick(self, msg, end='\n', verbose=True):
        now = datetime.now()
        if verbose:
            print(('[{}] [{}] {}'.format(now - self.start, now - self.then, msg)), end=end)
        self.then = now