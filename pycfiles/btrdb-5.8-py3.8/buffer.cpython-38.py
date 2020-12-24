# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/utils/buffer.py
# Compiled at: 2019-03-06 16:01:18
# Size of source mod 2**32: 2010 bytes
"""
Module for buffering utilities
"""
from collections import defaultdict

class PointBuffer(defaultdict):

    def __init__(self, length, *args, **kwargs):
        (super().__init__)(lambda : [None] * length, *args, **kwargs)
        self.num_streams = length
        self.active = [True] * length
        self.last_known_time = [None] * length

    def add_point(self, stream_index, point):
        self.last_known_time[stream_index] = max(self.last_known_time[stream_index] or -1, point.time)
        self[point.time][stream_index] = point

    def earliest(self):
        if len(self.keys()) == 0:
            return
        return min(self.keys())

    def deactivate(self, stream_index):
        self.active[stream_index] = False

    def is_ready(self, key):
        """
        Returns bool indicating whether a given key has all points from active
        (at the time) streams.
        """
        for idx, latest_time in enumerate(self.last_known_time):
            if not self.active[idx] or latest_time is None or key > latest_time:
                return False
            return True

    def next_key_ready(self):
        """

        """
        keys = list(self.keys())
        keys.sort()
        for key in keys:
            if self.is_ready(key):
                return key