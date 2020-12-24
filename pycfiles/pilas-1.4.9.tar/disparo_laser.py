# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/disparo_laser.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor
import math

class DisparoLaser(Actor):
    """Muestra un disparo que avanza por la pantalla.

    .. image:: ../../pilas/data/manual/imagenes/actores/disparo_laser.png

    Este actor se podría usar como arma para juegos de naves
    generalmente. Por ejemplo, el actor NaveRoja dispara usando
    este actor como munición.

    """

    def pre_iniciar(self, x=0, y=0, rotacion=0, velocidad=10, imagen='sin_imagen.png'):
        self.x = x
        self.y = y
        self.rotacion = rotacion
        self.velocidad = velocidad
        self.imagen = imagen
        self._calcular_movimiento_desde_rotacion(velocidad)
        self.aprender(self.pilas.habilidades.EliminarseSiSaleDePantalla)
        self.cuando_se_elimina = None
        return

    def actualizar(self):
        self.x += self.dx
        self.y += self.dy

    def _calcular_movimiento_desde_rotacion(self, velocidad):
        rotacion_en_radianes = math.radians(self.rotacion)
        self.dx = math.cos(rotacion_en_radianes) * velocidad
        self.dy = math.sin(rotacion_en_radianes) * velocidad

    def eliminar(self):
        if self.cuando_se_elimina:
            self.cuando_se_elimina(self)
        Actor.eliminar(self)