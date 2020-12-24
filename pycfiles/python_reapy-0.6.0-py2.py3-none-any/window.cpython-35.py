# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/window/window.py
# Compiled at: 2019-03-01 15:21:16
# Size of source mod 2**32: 236 bytes
import reapy
from reapy.core import ReapyObject
import reapy.reascript_api as RPR

class Window(ReapyObject):

    def __init__(self, id):
        self.id = id

    @property
    def _args(self):
        return (self.id,)