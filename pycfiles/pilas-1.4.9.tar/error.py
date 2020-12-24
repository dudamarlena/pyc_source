# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/escenas/error.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.escenas.escena import Escena

class Error(Escena):
    """Representa la escena de errores de pilas.

    Esta escena muestra el tipo de error en la pantalla,
    junto con una descripción y el archivo que ocasionó
    el error.
    """

    def iniciar(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fondo = self.pilas.fondos.Plano()
        self.actor_error = self.pilas.actores.MensajeError(self.titulo, self.descripcion)

    def actualizar(self):
        pass

    def terminar(self):
        pass