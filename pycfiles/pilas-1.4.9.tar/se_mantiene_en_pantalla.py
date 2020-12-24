# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/se_mantiene_en_pantalla.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class SeMantieneEnPantalla(habilidades.Habilidad):
    """Se asegura de que el actor regrese a la pantalla si sale o que no
    salga en nigún momento de la pantalla.

    Si el actor sale por la derecha de la pantalla, entonces regresa
    por la izquiera. Si sale por arriba regresa por abajo y asi...

    """

    def iniciar(self, receptor, permitir_salida=True):
        u"""
        :param receptor: El actor que aprenderá la habilidad.
        :param permitir_salida: Valor booleano que establece si el actor
                                puede salir por los lados de la ventana y
                                regresar por el lado opuesto. Si se establece a
                                False, el actor no puede salir de la ventana en
                                ningún momento.
        """
        super(SeMantieneEnPantalla, self).iniciar(receptor)
        self.ancho, self.alto = self.pilas.obtener_area()
        self.permitir_salida = permitir_salida

    def actualizar(self):
        if self.permitir_salida:
            if self.receptor.derecha < -(self.ancho / 2):
                self.receptor.izquierda = self.ancho / 2
            elif self.receptor.izquierda > self.ancho / 2:
                self.receptor.derecha = -(self.ancho / 2)
            if self.receptor.abajo > self.alto / 2:
                self.receptor.arriba = -(self.alto / 2)
            elif self.receptor.arriba < -(self.alto / 2):
                self.receptor.abajo = self.alto / 2
        else:
            if self.receptor.izquierda <= -(self.ancho / 2):
                self.receptor.izquierda = -(self.ancho / 2)
            elif self.receptor.derecha >= self.ancho / 2:
                self.receptor.derecha = self.ancho / 2
            if self.receptor.arriba > self.alto / 2:
                self.receptor.arriba = self.alto / 2
            elif self.receptor.abajo < -(self.alto / 2):
                self.receptor.abajo = -(self.alto / 2)