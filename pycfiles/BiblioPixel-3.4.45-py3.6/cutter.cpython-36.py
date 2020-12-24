# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/cutter.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1992 bytes
"""
Cut matrices by row or column and apply operations to them.
"""

class Cutter:
    __doc__ = '\n    Base class that pre-calculates cuts and can use them to\n    apply a function to the layout.\n\n    Each "cut" is a row or column, depending on the value of by_row.\n\n    The entries are iterated forward or backwards, depending on the\n    value of forward.\n    '

    def __init__(self, layout, by_row=True):
        self.layout = layout
        cuts = layout.height if by_row else layout.width
        cutter = self.cut_row if by_row else self.cut_column
        self.cuts = [cutter(i) for i in range(cuts)]

    def apply(self, function):
        """
        For each row or column in cuts, read a list of its colors,
        apply the function to that list of colors, then write it back
        to the layout.
        """
        for cut in self.cuts:
            value = self.read(cut)
            function(value)
            self.write(cut, value)


class Slicer(Cutter):
    __doc__ = '\n    Implementation of Cutter that uses slices of the underlying colorlist.\n    Does not work if the Matrix layout is serpentine or has any reflections\n    or rotations.\n    '

    def cut_row(self, i):
        return slice(self.layout.width * i, self.layout.width * (i + 1))

    def cut_column(self, i):
        return slice(i, None, self.layout.width)

    def read(self, cut):
        return self.layout.color_list[cut]

    def write(self, cut, value):
        self.layout.color_list[cut] = value


class Indexer(Cutter):
    __doc__ = '\n    Slower implementation of Cutter that uses lists of indices and the\n    Matrix interface.\n    '

    def cut_row(self, i):
        return [(column, i) for column in range(self.layout.width)]

    def cut_column(self, i):
        return [(i, row) for row in range(self.layout.height)]

    def read(self, cut):
        return [(self.layout.get)(*i) for i in cut]

    def write(self, cut, value):
        for i, v in zip(cut, value):
            (self.layout.set)(*i, **{'color': v})