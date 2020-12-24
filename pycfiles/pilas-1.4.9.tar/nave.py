# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/nave.py
# Compiled at: 2016-08-25 20:52:02
import pilasengine
from pilasengine.actores.animacion import Animacion

class Nave(Animacion):
    """Representa una nave que puede disparar.

    .. image:: ../../pilas/data/manual/imagenes/actores/nave.png

    """

    def __init__(self, pilas, x=0, y=0, velocidad=2):
        u"""
        Constructor de la Nave.

        :param x: posicion horizontal de la nave.
        :type x: int
        :param y: posicion vertical de la nave.
        :type y: int
        :param velocidad: Velocidad que llevará la nave.
        :type velocidad: int
        """
        self.velocidad = velocidad
        grilla = pilas.imagenes.cargar_grilla('nave.png', 2)
        Animacion.__init__(self, pilas, grilla, ciclica=True, x=x, y=y)
        self.radio_de_colision = 20
        self.aprender(pilas.habilidades.PuedeExplotar)
        self.municion = pilasengine.actores.Misil
        self.aprender(self.pilas.habilidades.Disparar, municion=self.municion, angulo_salida_disparo=90, frecuencia_de_disparo=6, distancia=4, escala=1)
        self.aprender(pilas.habilidades.MoverseConElTeclado, velocidad_maxima=self.velocidad, aceleracion=1, deceleracion=0.04, con_rotacion=True, velocidad_rotacion=1, marcha_atras=False)
        self.z = -1

    def actualizar(self):
        Animacion.actualizar(self)

    def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
        u"""Hace que una nave tenga como enemigos a todos los actores del grupo.

        :param grupo: El grupo de actores que serán sus enemigos.
        :type grupo: array
        :param cuando_elimina_enemigo: Funcion que se ejecutará cuando se
                                       elimine un enemigo.

        """
        self.cuando_elimina_enemigo = cuando_elimina_enemigo
        self.habilidades.Disparar.definir_colision(grupo, self.hacer_explotar_al_enemigo)

    def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
        u"""Es el método que se invoca cuando se produce una colisión 'tiro <-> enemigo'

        :param mi_disparo: El disparo de la nave.
        :param el_enemigo: El enemigo que se eliminará.
        """
        mi_disparo.eliminar()
        el_enemigo.eliminar()
        if self.cuando_elimina_enemigo:
            self.cuando_elimina_enemigo()