# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\fxs\simple.py
# Compiled at: 2012-02-06 09:19:16
"""Este efecto muestra lo mas simple, lo basico"""
from libs import common

class EfectoGenerico:

    def OnDialogue(self, diag):
        diag.Paint()

    def OnSyllable(self, diag):
        diag.actual.color1.CopyFrom(diag.actual.color2)
        diag.Paint()


class FxsGroup(common.FxsGroup):

    def __init__(self):
        self.in_ms = 150
        self.out_ms = 250
        self.syl_in_ms = 500
        self.syl_out_ms = 200
        self.fxs = (
         EfectoGenerico(), EfectoGenerico())