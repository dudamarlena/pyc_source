# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/envelope/segments.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1135 bytes
import statistics

class Segments(list):
    __doc__ = '\n    A list of [level, time] pairs.\n    '

    def __init__(self, segments=(), length=None):
        super().__init__()
        self.base_value = 0
        for segment in segments:
            try:
                level, time = segment
            except TypeError:
                level, time = segment, None

            self.append([level, time])

        times = [t for s, t in self if t is not None]
        if times:
            mean = sum(times) / len(times)
        else:
            mean = (length or 1) / max(1, len(self))
        for segment in self:
            if segment[1] is None:
                segment[1] = mean

        self.total_time = sum(t for l, t in self)

    def __call__(self, time, base_value=0):
        elapsed_time = 0
        level = base_value
        for l, t in self:
            segment_end_time = elapsed_time + t
            if time < segment_end_time:
                delta_t = time - elapsed_time
                return level + (l - level) * delta_t / t
            elapsed_time = segment_end_time
            level = l

        return level