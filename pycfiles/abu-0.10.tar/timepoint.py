# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bryanbriney/git/abtools/abtools/phylogeny/timepoint.py
# Compiled at: 2016-01-29 19:53:51


class Timepoint(object):
    """
    Stores and manipulates timepoint information.
    """

    def __init__(self, tp, order, color):
        super(Timepoint, self).__init__()
        self.name = tp
        self.order = int(order)
        self.raw_color = color
        self.color = self._get_color()

    def _get_color(self):
        if self._is_rbg():
            return self._convert_to_hex()
        return self.raw_color

    def _is_rbg(self):
        color = self.raw_color
        if type(color) == tuple:
            return True
        if len(self.raw_color.split(',')) == 3:
            self.raw_color = self._convert_to_tuple()
            return True
        return False

    def _convert_to_tuple(self):
        c = self.raw_color.split(',')
        r = float(c[0].replace('(', '').strip())
        g = float(c[1].strip())
        b = float(c[2].replace(')', '').strip())
        return (
         r, g, b)

    def _convert_to_hex(self):
        r = float(self.raw_color[0])
        g = float(self.raw_color[1])
        b = float(self.raw_color[2])
        if 0 < round(sum([r, b, g]), 2) <= 3:
            r, b, g = 255 * r, 255 * b, 255 * g
        return '#%02x%02x%02x' % (r, b, g)