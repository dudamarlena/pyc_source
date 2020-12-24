# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/colorpicker/color_change_event.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.component import Event

class ColorChangeEvent(Event):

    def __init__(self, source, color):
        Event.__init__(self, source)
        self._color = color

    def getColor(self):
        return self._color