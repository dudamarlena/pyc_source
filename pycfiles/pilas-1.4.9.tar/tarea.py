# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pilasengine/tareas/tarea.py
# Compiled at: 2016-08-25 20:52:02
from pilasengine.actores.actor import ActorEliminadoException

class Tarea(object):

    def __init__(self, planificador, pilas, una_vez, time_out, dt, funcion, *args, **kwargs):
        u"""Representa una tarea que se puede ejecutar dentro del planificador.

        :param time_out: El tiempo absoluto para ejecutar la tarea.
        :param dt: La frecuencia de ejecución.
        :param funcion: La funcion a invocar.
        :param parametros: Una lista de argumentos para la funcion anterior.
        :param una_vez: Indica si la funcion se tiene que ejecutar una sola vez.
        """
        self.planificador = planificador
        self.una_vez = una_vez
        self.time_out = time_out
        self.dt = dt
        self.funcion = funcion
        self.args, self.kwargs = args, kwargs
        self.pilas = pilas

    def ejecutar(self):
        """Ejecuta la tarea."""
        try:
            return self.funcion(*self.args, **self.kwargs)
        except ActorEliminadoException:
            self.pilas.log('Se evitó ejecutar la tarea sobre un actor eliminado...')

    def eliminar(self):
        """Quita la tarea del planificador para que no se vuelva a ejecutar."""
        self.planificador.eliminar_tarea(self)

    def terminar(self):
        """Termina la tarea (alias de eliminar)."""
        self.eliminar()