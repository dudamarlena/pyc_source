# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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