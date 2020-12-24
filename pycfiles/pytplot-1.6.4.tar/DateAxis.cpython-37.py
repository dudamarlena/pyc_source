# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomAxis/DateAxis.py
# Compiled at: 2020-04-30 01:29:24
# Size of source mod 2**32: 5767 bytes
import pyqtgraph as pg, time

class DateAxis(pg.AxisItem):
    __doc__ = '\n    This class takes in tplot time variables and creates ticks/tick labels\n    depending on the time length of the data.\n    '

    def tickStrings(self, values, scale, spacing):
        strns = []
        if not values:
            return strns
        for x in values:
            try:
                rng = max(values) - min(values)
                if rng < 300:
                    string = '%H:%M:%S'
                    label1 = '%b %d -'
                    label2 = ' %b %d, %Y'
                else:
                    if 300 <= rng < 345600:
                        if x % 86400 == 0:
                            string = '%Y-%m-%d'
                            label1 = '%b %d -'
                            label2 = ' %b %d, %Y'
                        else:
                            string = '%H:%M'
                            label1 = '%b %d -'
                            label2 = ' %b %d, %Y'
                    elif 345600 <= rng < 2592000:
                        string = '%m-%d'
                        label1 = '%b %d -'
                        label2 = ' %b %d, %Y'
                    else:
                        if 2592000 <= rng < 62208000:
                            string = '%b-%Y'
                            label1 = '%Y -'
                            label2 = ' %Y'
                        else:
                            if rng >= 62208000:
                                string = '%Y'
                                label1 = ''
                                label2 = ''
                strns.append(time.strftime(string, time.gmtime(x)))
            except ValueError:
                strns.append(' ')

        try:
            label = time.strftime(label1, time.gmtime(min(values))) + time.strftime(label2, time.gmtime(max(values)))
        except ValueError:
            label = ''

        return strns

    def tickSpacing(self, minVal, maxVal, size):
        rng = maxVal - minVal
        if rng < 4:
            levels = [(1, 0)]
            return levels
        if 4 <= rng < 15:
            levels = [(2, 0)]
            return levels
        if 15 <= rng < 60:
            levels = [(5, 0)]
            return levels
        if 60 <= rng < 300:
            levels = [(30, 0)]
            return levels
        if 300 <= rng < 600:
            levels = [(60, 0)]
            return levels
        if 600 <= rng < 1800:
            levels = [(300, 0)]
            return levels
        if 1800 <= rng < 3600:
            levels = [(900, 0)]
            return levels
        if 3600 <= rng < 7200:
            levels = [(1800, 0)]
            return levels
        if 7200 <= rng < 21600:
            levels = [(3600, 0)]
            return levels
        if 21600 <= rng < 43200:
            levels = [(7200, 0)]
            return levels
        if 43200 <= rng < 86400:
            levels = [(14400, 0)]
            return levels
        if 86400 <= rng < 172800:
            levels = [(21600, 0)]
            return levels
        if 172800 <= rng < 345600:
            levels = [(43200, 0)]
            return levels
        if 345600 <= rng < 2592000:
            levels = [(172800, 0)]
            return levels
        if 2592000 <= rng < 62208000:
            levels = [(2592000.0, 0)]
            return levels
        if rng >= 62208000:
            levels = [
             (31540000.0, 0)]
            return levels