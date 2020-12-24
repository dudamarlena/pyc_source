# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/aumentar_con_rueda.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades

class AumentarConRueda(habilidades.Habilidad):

    def iniciar(self, receptor):
        super(AumentarConRueda, self).iniciar(receptor)
        self.pilas.eventos.mueve_rueda.conectar(self.cambiar_de_escala)

    def cambiar_de_escala(self, evento):
        self.receptor.escala += evento.delta / 4.0