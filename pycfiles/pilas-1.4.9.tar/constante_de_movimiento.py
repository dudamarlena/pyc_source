# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/fisica/constantes/constante_de_movimiento.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import utils

class ConstanteDeMovimiento:
    """Representa una constante de movimiento para el mouse."""

    def __init__(self, pilas, figura):
        """Inicializa la constante.

        :param pilas: instancia de pilas
        :param figura: Figura a controlar desde el mouse.
        """
        self.pilas = pilas
        mundo = pilas.escena_actual().fisica.mundo
        punto_captura = (utils.convertir_a_metros(figura.x), utils.convertir_a_metros(figura.y))
        self.cuerpo_enlazado = mundo.CreateBody()
        self.constante = mundo.CreateMouseJoint(bodyA=self.cuerpo_enlazado, bodyB=figura._cuerpo, target=punto_captura, maxForce=1000.0 * figura._cuerpo.mass)
        figura._cuerpo.awake = True

    def mover(self, x, y):
        u"""Realiza un movimiento de la figura.

        :param x: Posición horizontal.
        :param y: Posición vertical.
        """
        self.constante.target = (
         utils.convertir_a_metros(x), utils.convertir_a_metros(y))

    def eliminar(self):
        self.pilas.escena_actual().fisica.mundo.DestroyBody(self.cuerpo_enlazado)