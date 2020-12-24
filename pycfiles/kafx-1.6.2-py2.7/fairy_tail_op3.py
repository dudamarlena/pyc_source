# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\Abelkm\fairy_tail_op3.py
# Compiled at: 2012-02-06 09:19:16
"""
Hecho por Abelkm
http://my.opera.com/Abelkm/blog/
"""
from libs import common
from libs.draw import advanced
from math import pi, sin, cos

class FX1(common.Fx):

    def EnSilaba(self, d):
        d.LoadTexture('textures/fire2.png', parte=d.PART_RELLENO)
        d.MoveTexture(60 * d.progreso, 60 * d.progreso, parte=d.PART_RELLENO)
        advanced.StartGroup()
        d.Pintar()
        advanced.fGlow(2, 0 + cos(pi * d.progreso) / 4)
        advanced.EndGroup()

    def EnSilabaMuerta(self, d):
        d.LoadTexture('textures/fire2.png', parte=d.PART_RELLENO)
        d.MoveTexture(-50 * d.progreso, -50 * d.progreso, parte=d.PART_RELLENO)
        d.Pintar()

    def EnDialogoSale(self, d):
        d.LoadTexture('textures/fire2.png', parte=d.PART_RELLENO)
        d.MoveTexture(70 * d.progreso, 70 * d.progreso, parte=d.PART_RELLENO)
        d.Fade(1, 0)
        d.actual.scale_y = 1 + d.progreso / 4.0
        advanced.StartGroup()
        d.Pintar()
        advanced.fBiDirBlur(pi / 2.0, 7)
        advanced.EndGroup()

    def EnDialogoEntra(self, d):
        d.LoadTexture('textures/stone2.png', parte=d.PART_RELLENO)
        d.Fade(0, 1)
        advanced.StartGroup()
        d.actual.scale_y = 1 + sin(pi * d.progreso)
        d.Pintar()
        advanced.fBiDirBlur(pi / 2.0, 7)
        advanced.EndGroup()

    def EnSilabaDorm(self, d):
        d.LoadTexture('textures/stone2.png', parte=d.PART_RELLENO)
        d.Pintar()


class FxsGroup(common.FxsGroup):

    def __init__(self):
        self.in_ms = 170
        self.out_ms = 100
        self.fxs = (FX1(), FX1())