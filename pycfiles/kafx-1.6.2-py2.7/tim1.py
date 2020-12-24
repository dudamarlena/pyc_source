# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\timh\tim1.py
# Compiled at: 2012-02-06 09:19:16
from libs import common
from libs.draw import advanced
from math import sin, pi
import random

class fx1(common.Fx):

    def EnDialogo(self, d):
        d.LoadTexture('textures/fuego/f0000.png', 1)
        d.Pintar()

    def EnSilaba(self, s):
        advanced.StartGroup()
        s.Pintar()
        advanced.fGlow(1, 0.1 + sin(pi * s.progreso) / 6.0)
        advanced.EndGroup()


class FxsGroup(common.FxsGroup):
    fxs = [
     fx1()]