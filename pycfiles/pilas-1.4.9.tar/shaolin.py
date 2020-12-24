# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/shaolin.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor
from pilasengine.comportamientos.comportamiento import Comportamiento

class Shaolin(Actor):
    """Representa un luchador que se puede controlar con el teclado,
    puede saltar, golpear y recibir golpes."""

    def iniciar(self, x=0, y=0):
        self.x = x
        self.y = y
        self.hacer_inmediatamente(Parado)
        self.sombra = self.pilas.actores.Sombra()
        self.altura_del_salto = 0

    def actualizar(self):
        self.sombra.x = self.x
        self.sombra.z = self.z + 1
        self.sombra.rotacion = self.rotacion
        self.sombra.y = self.y + 10 - self.altura_del_salto
        self.sombra.escala = self.escala - self.altura_del_salto / 300.0


class Parado(Comportamiento):

    def iniciar(self, receptor):
        """Inicializa el comportamiento.

        :param receptor: La referencia al actor.
        """
        self.receptor = receptor
        self.control = receptor.pilas.control
        self.receptor.imagen = self.pilas.imagenes.cargar_grilla('shaolin/parado.png', 4, 1)
        self.receptor.centro = ('centro', 'abajo')

    def actualizar(self):
        self.receptor.imagen.avanzar(10)
        if self.control.derecha or self.control.izquierda:
            self.receptor.hacer_inmediatamente(Caminar)
        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltar)


class Caminar(Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.control = receptor.pilas.control
        self.receptor.imagen = self.pilas.imagenes.cargar_grilla('shaolin/camina.png', 4, 1)
        self.receptor.centro = ('centro', 'abajo')

    def actualizar(self):
        self.receptor.imagen.avanzar(10)
        if self.control.derecha:
            self.receptor.x += 5
            self.receptor.espejado = False
        elif self.control.izquierda:
            self.receptor.x -= 5
            self.receptor.espejado = True
        if self.control.arriba:
            self.receptor.hacer_inmediatamente(Saltar)
        if not self.control.derecha and not self.control.izquierda:
            self.receptor.hacer_inmediatamente(Parado)


class Saltar(Comportamiento):

    def iniciar(self, receptor):
        self.receptor = receptor
        self.control = receptor.pilas.control
        self.receptor.imagen = self.pilas.imagenes.cargar_grilla('shaolin/salta.png', 3, 1)
        self.receptor.centro = ('centro', 'abajo')
        self.y_inicial = self.receptor.y
        self.vy = 15

    def actualizar(self):
        self.receptor.y += self.vy
        self.vy -= 0.7
        distancia_al_suelo = self.receptor.y - self.y_inicial
        self.receptor.altura_del_salto = distancia_al_suelo
        if distancia_al_suelo < 0:
            self.receptor.y = self.y_inicial
            self.receptor.altura_del_salto = 0
            self.receptor.hacer_inmediatamente(Parado)
        if self.control.derecha:
            self.receptor.x += 5
            self.receptor.espejado = False
        elif self.control.izquierda:
            self.receptor.x -= 5
            self.receptor.espejado = True