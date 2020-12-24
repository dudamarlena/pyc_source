# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\not_so_simple.py
# Compiled at: 2012-03-08 22:12:10
from libs import common
from math import pi, sin

class FX1(common.Fx):

    def OnDialogueIn(self, s):
        s.Fade(0, 1)
        s.Paint()

    def OnSyllableSleep(self, s):
        s.Paint()

    def OnSyllable(self, s):
        s.actual.scale_x = s.actual.scale_y = 0.5 * sin(pi * s.progress) + 1
        s.actual.color1.CopyFrom(s.original.color2)
        s.Paint()

    def OnSyllableDead(self, s):
        s.actual.color1.CopyFrom(s.original.color2)
        s.Paint()

    def OnDialogueOut(self, s):
        s.Fade(1, 0)
        s.Paint()


class FxsGroup(common.FxsGroup):

    def __init__(self):
        self.in_ms = 150
        self.out_ms = 250
        self.syl_in_ms = 150
        self.syl_out_ms = 250
        self.fxs = (
         FX1(), FX1())