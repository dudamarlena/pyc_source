# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/target_details_impl.py
# Compiled at: 2013-04-04 15:36:37
"""Implementation of ITargetDetails for terminal implementation and
extension."""
from muntjac.event.dd.target_details import ITargetDetails

class TargetDetailsImpl(ITargetDetails):
    """A HashMap backed implementation of L{ITargetDetails} for terminal
    implementation and for extension.
    """

    def __init__(self, rawDropData, dropTarget=None):
        self._data = dict()
        self._data.update(rawDropData)
        self._dropTarget = dropTarget

    def getData(self, key):
        return self._data.get(key)

    def setData(self, key, value):
        if key in self._data:
            return self._data[key]
        else:
            self._data[key] = value
            return
            return

    def getTarget(self):
        return self._dropTarget