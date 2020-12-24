# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\Abelkm\testo.py
# Compiled at: 2012-02-06 09:19:18
"""
Hecho por Abelkm
http://my.opera.com/Abelkm/blog/
"""
from libs import common

class FX1(common.Fx):

    def EnDialogo(self, d):
        d.FullWiggle(4)
        d.Pintar()

    def EnSilaba(self, d):
        d.actual.color1.CopiarDe(d.actual.color2)
        d.Pintar()

    def EnSilabaMuerta(self, d):
        d.actual.color1.CopiarDe(d.actual.color3)
        d.Pintar()

    def EnDialogoSale(self, d):
        d.actual.color1.CopiarDe(d.actual.color4)
        d.Pintar()

    def EnDialogoEntra(self, d):
        d.actual.color1.CopiarDe(d.actual.color4)
        d.Pintar()


class FxsGroup(common.FxsGroup):

    def __init__(self):
        self.in_ms = 500
        self.out_ms = 500
        self.fxs = (FX1(), FX1())