# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/habilidades/imitar.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine import habilidades
from pilasengine import fisica

class Imitar(habilidades.Habilidad):
    """Logra que el actor imite las propiedades de otro."""

    def iniciar(self, receptor, objeto_a_imitar, con_escala=True, con_rotacion=True):
        u"""Inicializa la habilidad.

        :param receptor: Referencia al actor.
        :param objeto_a_imitar: Cualquier objeto con atributos rotacion,
                                x e y (por ejemplo otro actor).
        :param con_rotacion: Si debe imitar o no la rotación.
        """
        super(Imitar, self).iniciar(receptor)
        self.objeto_a_imitar = objeto_a_imitar
        receptor.id = objeto_a_imitar.id
        if hasattr(objeto_a_imitar, '_cuerpo'):
            receptor.figura = objeto_a_imitar
            receptor.figura_de_colision = objeto_a_imitar
        self.con_escala = con_escala
        self.con_rotacion = con_rotacion
        self.imitar()

    def actualizar(self):
        self.imitar()

    def imitar(self):
        self.receptor.x = self.objeto_a_imitar.x
        self.receptor.y = self.objeto_a_imitar.y
        if self.con_escala:
            self.objeto_a_imitar.escala = self.receptor.escala
        if self.con_rotacion:
            self.receptor.rotacion = self.objeto_a_imitar.rotacion

    def eliminar(self):
        super(Imitar, self).eliminar()
        if isinstance(self.objeto_a_imitar, fisica.figura.Figura):
            self.objeto_a_imitar.eliminar()
            self.receptor.figura = None
        return