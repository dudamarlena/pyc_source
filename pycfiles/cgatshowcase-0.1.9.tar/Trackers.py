# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ifs/devel/andreas/CGATReport/CGATReport/templates/Trackers.py
# Compiled at: 2014-09-18 10:37:00
from CGATReport.Tracker import Tracker
from collections import OrderedDict as odict

class SimpleExampleData(Tracker):
    """Simple Example Data.
    """
    tracks = [
     'bicycle', 'car']

    def __call__(self, track):
        if track == 'car':
            return odict((('wheels', 4), ('max passengers', 5)))
        if track == 'bicycle':
            return odict((('wheels', 2), ('max passengers', 1)))