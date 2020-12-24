# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/arrastrable.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class Arrastrable(habilidades.Habilidad):

    def iniciar(self, receptor):
        super(Arrastrable, self).iniciar(receptor)

    def intentar_arrastrar(self):
        self.pilas.eventos.termina_click.conectar(self.termina_de_arrastrar, id='termina_de_arrastrar')
        self.pilas.eventos.mueve_mouse.conectar(self.arrastrando, id='arrastrando')
        self.intentar_capturar_figura()

    def intentar_capturar_figura(self):
        if self._el_receptor_tiene_fisica():
            self.pilas.fisica.capturar_figura_con_el_mouse(self.receptor.figura)

    def arrastrando(self, evento):
        if self._el_receptor_tiene_fisica():
            self.pilas.fisica.cuando_mueve_el_mouse(evento.x, evento.y)
        else:
            self.receptor.x = evento.x
            self.receptor.y = evento.y

    def termina_de_arrastrar(self, evento):
        self.pilas.eventos.mueve_mouse.desconectar_por_id('arrastrando')
        self.pilas.eventos.termina_click.desconectar_por_id('termina_de_arrastrar')
        self.pilas.fisica.cuando_suelta_el_mouse()

    def _el_receptor_tiene_fisica(self):
        return hasattr(self.receptor, 'figura') and self.receptor.figura