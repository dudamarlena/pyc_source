# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/clitellum_evs/rejection/engines.py
# Compiled at: 2018-01-22 09:50:01
__doc__ = '\nMotores de rechazo\n'

class RejectionEventException(Exception):
    u"""
    Excepcion que se lanza cuando un evento ha sido rechazado en alguna transición
    """

    def __init__(self, root, event):
        msg = 'Error al procesar el evento %s, en la entidad %s' % (event.get_name(), str(root.get_id()))
        Exception.__init__(self, msg)


class RejectionEngine(object):
    """
    Clase base de los motores de rechazo
    """

    def __init__(self):
        self._rejected_events = []

    def get_rejected_events(self):
        """
        Devuelve la lista de los eventos rechazados
        """
        return self._rejected_events

    def reject(self, root, event):
        """
        Rechazo del evento
        """
        raise NotImplementedError()

    def execute(self):
        """
        Ejecuta la logica final del motor de rechazo
        """
        raise NotImplementedError()


class IgnoreRejectionEngine(RejectionEngine):
    """
    Define el motor de rechazo que no realiza ninguna accion cuando se rechaza un evento.
    """

    def __init__(self):
        RejectionEngine.__init__(self)

    def reject(self, root, event):
        self._rejected_events.append(event)

    def execute(self):
        pass


class StopOnErrorRejectionEngine(RejectionEngine):
    u"""
    Define el motor de rechazo de paro, cuando llega alguna transición que se ha podido aplicar
    no se siguen aplicando mas eventos.
    """

    def __init__(self):
        RejectionEngine.__init__(self)

    def reject(self, root, event):
        self._rejected_events.append(event)
        raise RejectionEventException(root, event)

    def execute(self):
        pass