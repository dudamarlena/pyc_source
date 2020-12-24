# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\hint.py
# Compiled at: 2018-06-07 14:38:12
# Size of source mod 2**32: 474 bytes
from .ProcessingPlugin import Output

class Hint(object):

    def __init__(self, **kwargs):
        self.parent = None
        self.checked = False

    @property
    def name(self):
        raise NotImplementedError


class PlotHint(Hint):

    def __init__(self, x, y):
        super(PlotHint, self).__init__()
        self.x = x
        self.y = y

    @property
    def name(self):
        return f"{self.y.name} vs. {self.x.name}"