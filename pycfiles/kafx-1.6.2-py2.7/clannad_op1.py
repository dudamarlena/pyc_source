# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\Abelkm\clannad_op1.py
# Compiled at: 2012-02-06 09:19:16
"""
Hecho por Abelkm
http://my.opera.com/Abelkm/blog/
reemplazar las imágenes por otras para probarlo, no las voy a subir al svn
"""
from libs import common
from libs.draw import advanced
from math import pi, sin, cos

class FX1(common.Fx):

    def EnSilaba(self, d):
        d.LoadTexture('E:/Documents and Settings/Administrador/Escritorio/Nueva carpeta/textures/glass3.png', parte=d.PART_RELLENO)
        d.MoveTexture(60 * d.progreso, 60 * d.progreso, parte=d.PART_RELLENO)
        d.actual.color1.a = 0.6
        advanced.StartGroup()
        d.Pintar()
        advanced.fGlow(2, sin(pi * d.progreso) / 6.0)
        advanced.EndGroup()

    def EnSilabaMuerta(self, d):
        d.LoadTexture('E:/Documents and Settings/Administrador/Escritorio/Nueva carpeta/textures/glass3.png', parte=d.PART_RELLENO)
        d.actual.color1.a = 0.6
        advanced.StartGroup()
        d.Pintar()
        advanced.ModoPintado('add')
        advanced.EndGroup()

    def EnDialogoSale(self, d):
        d.LoadTexture('E:/Documents and Settings/Administrador/Escritorio/Nueva carpeta/textures/glass3.png', parte=d.PART_RELLENO)
        d.actual.color1.a = common.Interpolar(d.progreso, 0.6, 0)
        d.actual.color3.a = common.Interpolar(d.progreso, 1, 0)
        d.actual.borde = common.Interpolar(d.progreso, 1, 0)
        advanced.StartGroup()
        d.Pintar()
        advanced.fBiDirBlur(pi, sin(pi * d.progreso) * 5.0)
        advanced.ModoPintado('add')
        advanced.EndGroup()

    def EnDialogoEntra(self, d):
        d.LoadTexture('E:/Documents and Settings/Administrador/Escritorio/Nueva carpeta/textures/glass1.png', parte=d.PART_RELLENO)
        d.actual.color1.a = common.Interpolar(d.progreso, 0, 0.6)
        d.actual.color3.a = common.Interpolar(d.progreso, 0, 1)
        d.actual.borde = common.Interpolar(d.progreso, 0, 1)
        advanced.StartGroup()
        d.Pintar()
        advanced.fBiDirBlur(pi, sin(pi * d.progreso) * 5.0)
        advanced.ModoPintado('add')
        advanced.EndGroup()

    def EnSilabaDorm(self, d):
        d.LoadTexture('E:/Documents and Settings/Administrador/Escritorio/Nueva carpeta/textures/glass1.png', parte=d.PART_RELLENO)
        d.actual.color1.a = 0.6
        advanced.StartGroup()
        d.Pintar()
        advanced.ModoPintado('add')
        advanced.EndGroup()


class FxsGroup(common.FxsGroup):

    def __init__(self):
        self.in_ms = 240
        self.out_ms = 300
        self.fxs = (FX1(), FX1())