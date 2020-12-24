# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fondos/plano.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.fondos.fondo import Fondo
from pilasengine.fondos.fondo_mozaico import FondoMozaico

class Plano(FondoMozaico):

    def iniciar(self):
        self.imagen = 'fondos/plano.png'