# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/limitado_a_bordes_de_pantalla.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.habilidades import se_mantiene_en_pantalla

class LimitadoABordesDePantalla(se_mantiene_en_pantalla.SeMantieneEnPantalla):
    """Se asegura de que el actor no pueda salir por los bordes
    de la pantalla.
    """

    def iniciar(self, receptor):
        u"""
        :param receptor: El actor que aprenderá la habilidad.
        """
        super(LimitadoABordesDePantalla, self).iniciar(receptor, permitir_salida=False)