# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/limit.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1334 bytes


class Limit:

    def __init__(self, ratio=1, knee=0, gain=1, enable=True):
        """
        :param float ratio: the compression ratio (1 means no compression).
            ratio should usually between 0 and 1.

        :param float knee: the ratio where the compression starts to kick in.
            knee should usually be 0 <= knee <= ratio

        :param float gain: post limiter output gain. gain should usually be >= 0
        """
        self.ratio = ratio
        self.knee = knee
        self.gain = gain
        self.enable = enable

    def __bool__(self):
        return self.enable and (self.gain != 1 or self.ratio < 1)

    def limit(self, value):
        if not (self.enable or self):
            return value
        else:
            overshoot = value - self.knee
            if overshoot >= 0:
                scale = (self.ratio - self.knee) / (1 - self.knee or 1)
                value = self.knee + overshoot * scale
            value = min(value, self.ratio)
            return value * self.gain

    def limit_colors(self, colors, math):
        if self:
            total = math.sum(colors)
            max_total = 765 * len(colors)
            average = total / max_total
            limit = self.limit(average) / average
            math.scale(colors, limit)