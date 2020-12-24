# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/transitfeed/shapeloader.py
# Compiled at: 2018-01-24 00:52:58
from loader import Loader

class ShapeLoader(Loader):
    """A subclass of Loader that only loads the shapes from a GTFS file."""

    def __init__(self, *args, **kwargs):
        """Initialize a new ShapeLoader object.

    See Loader.__init__ for argument documentation.
    """
        Loader.__init__(self, *args, **kwargs)

    def Load(self):
        self._LoadShapes()
        return self._schedule