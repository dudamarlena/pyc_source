# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/torreta.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import Actor
from pilasengine.actores.bala import Bala

class Torreta(Actor):
    """Representa una torreta que puede disparar y rota con el mouse."""

    def iniciar(self, municion_bala_simple=None, enemigos=[], cuando_elimina_enemigo=None, x=0, y=0, frecuencia_de_disparo=10):
        u"""Inicializa la Torreta.                                                
                                                                                 
        :param municion_bala_simple: Indica el tipo de munición que se utilizará.
        :param enemigos: Lista o grupo de enemigos que podría eliminar la torreta.
        :param x: Posición horizontal inicial.                                   
        :param y: Posición vertical inicial.                                     
        :param frecuencia_de_disparo: Frecuencia con la que se dispararán las municiones.
        """
        self.imagen = self.pilas.imagenes.cargar('torreta.png')
        self.radio_de_colision = 15
        if municion_bala_simple is None:
            municion_bala_simple = Bala
        self.aprender(self.pilas.habilidades.RotarConMouse, lado_seguimiento='arriba')
        self.aprender('DispararConClick', municion=municion_bala_simple, grupo_enemigos=enemigos, cuando_elimina_enemigo=cuando_elimina_enemigo, frecuencia_de_disparo=frecuencia_de_disparo, angulo_salida_disparo=90, distancia=27)
        return

    def get_municion(self):
        u"""Retorna la munción que está utilizando la torreta."""
        return self.habilidades.DispararConClick.municion

    def set_municion(self, municion):
        u"""Define la munición que utilizará la torreta."""
        self.habilidades.DispararConClick.municion = municion

    municion = property(get_municion, set_municion, doc='Define la munición de la torreta.')