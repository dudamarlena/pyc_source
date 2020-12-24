# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/control/control.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 1313 bytes
import json, logging, os, time
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ..core import Evented

class Control(Evented):
    controlId = 0
    addedToMap = pyqtSignal()
    removedFromMap = pyqtSignal()

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map_):
        self._map = map_
        if map_ is None:
            self.removedFromMap.emit()
        else:
            self.addedToMap.emit()

    @property
    def jsName(self):
        return self._controlName

    @property
    def controlName(self):
        return self._controlName

    @controlName.setter
    def controlName(self, name):
        self._controlName = name

    def __init__(self):
        super().__init__()
        self._controlName = self._getNewControlName()

    def addTo(self, map_):
        map_.addControl(self)

    def removeFrom(self, map_):
        map_.removeControl(self)

    def _getNewControlName(self):
        controlName = 'c{}'.format(self.controlId)
        Control.controlId += 1
        return controlName