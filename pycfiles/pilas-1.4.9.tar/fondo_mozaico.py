# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fondos/fondo_mozaico.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.fondos.fondo import Fondo

class FondoMozaico(Fondo):

    def __init__(self, pilas=None, imagen=None):
        super(FondoMozaico, self).__init__(pilas, imagen)

    def dibujar(self, painter):
        painter.save()
        x = self.pilas.obtener_escena_actual().camara.x
        y = -self.pilas.obtener_escena_actual().camara.y
        ancho, alto = self.pilas.obtener_area()
        painter.drawTiledPixmap(-ancho / 2, -alto / 2, ancho, alto, self.imagen._imagen, x % self.imagen.ancho(), y % self.imagen.alto())
        painter.restore()