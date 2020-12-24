# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/tareas/tarea_condicional.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.tareas.tarea import Tarea

class TareaCondicional(Tarea):
    """Representa una tarea similar a Tarea, pero que solo se ejecuta si El
    retorno de la función a ejecutar devuelve True.
    """

    def ejecutar(self):
        """Ejecuta la tarea, y se detiene si no revuelve True."""
        retorno = Tarea.ejecutar(self)
        if not retorno:
            self.una_vez = True