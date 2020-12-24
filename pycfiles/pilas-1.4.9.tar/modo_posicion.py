# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/depurador/modo_posicion.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.depurador.modo import ModoDepurador
from pilasengine.colores import blanco, negro

class ModoPosicion(ModoDepurador):

    def __init__(self, pilas, depurador):
        ModoDepurador.__init__(self, pilas, depurador)
        self.ejes = self.pilas.actores.Ejes()

    def cuando_dibuja_actor_sin_transformacion(self, actor, painter):
        self._definir_trazo_blanco(painter)
        x = ('{0:0.1f}').format(actor.x)
        y = ('{0:0.1f}').format(actor.y)
        texto = '(%s, %s)' % (x, y)
        self._texto(painter, texto, 21, 21, color=negro)
        self._texto(painter, texto, 20, 20, color=blanco)

    def sale_del_modo(self):
        self.ejes.eliminar()