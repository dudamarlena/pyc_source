# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/calvo.py
# Compiled at: 2016-08-25 20:52:02
import pilasengine
from pilasengine.actores.maton import Maton
from pilasengine.comportamientos.comportamiento import Comportamiento

class Calvo(Maton):
    """Representa un personaje de juego tipo RPG."""

    def iniciar(self, x=0, y=0):
        self.imagen = self.pilas.imagenes.cargar_grilla('rpg/calvo.png', 3, 4)