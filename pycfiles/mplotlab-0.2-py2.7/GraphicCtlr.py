# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\graphics\GraphicCtlr.py
# Compiled at: 2016-02-07 09:44:32
from Navigation import Navigation

class GraphicCtlr(object):

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__navigation = Navigation(self.__canvas)

    def control(self, zoom=True, pan=False):
        nav = self.__navigation
        if pan == (nav._active != 'PAN'):
            nav.pan()
        if zoom == (nav._active != 'ZOOM'):
            nav.zoom()