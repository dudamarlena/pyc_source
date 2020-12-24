# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gruffy/bar_conversion.py
# Compiled at: 2010-10-04 14:52:46


class BarConversion(object):
    mode = None
    zero = None
    graph_top = None
    graph_height = None
    minimum_value = None
    spread = None

    def getLeftYRightYscaled(self, data_point):
        result = [
         None, None]
        if self.mode == 1:
            result[0] = self.graph_top + self.graph_height * (1 - data_point) + 1
            result[1] = self.graph_top + self.graph_height - 1
        elif self.mode == 2:
            result[0] = self.graph_top + 1
            result[1] = self.graph_top + self.graph_height * (1 - data_point) - 1
        elif self.mode == 3:
            val = data_point - self.minimum_value / self.spread
            if data_point >= self.zero:
                result[0] = self.graph_top + self.graph_height * (1 - (val - self.zero)) + 1
                result[1] = self.graph_top + self.graph_height * (1 - self.zero) - 1
            else:
                result[0] = self.graph_top + self.graph_height * (1 - (val - self.zero)) + 1
                result[1] = self.graph_top + self.graph_height * (1 - self.zero) - 1
        else:
            result[0] = 0.0
            result[1] = 0.0
        return result