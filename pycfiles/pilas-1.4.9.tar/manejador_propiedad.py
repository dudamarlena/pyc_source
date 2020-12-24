# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/actores/manejador_propiedad.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.deslizador_horizontal import DeslizadorHorizontal
from pilasengine import colores

class ManejadorPropiedad(DeslizadorHorizontal):

    def pre_iniciar(self, x=0, y=0, actor='actor', propiedad='x', _min=0, _max=100):
        pass

    def iniciar(self, x=0, y=0, actor='actor', propiedad='x', _min=0, _max=100):
        valor_inicial = getattr(actor, propiedad)
        DeslizadorHorizontal.iniciar(self, x, y, _min, _max, propiedad, valor_inicial=valor_inicial)
        self.actor = actor
        self.propiedad = propiedad
        self.conectar(self.cuando_cambia)

    def cuando_cambia(self, valor):
        setattr(self.actor, self.propiedad, valor)