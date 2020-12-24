# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/clitellum_evs/fsm.py
# Compiled at: 2017-11-27 04:55:45
__doc__ = '\nMaquina de estados del event sourcing\n'

class EventSourcingMachine(object):
    """
    Clase que define la maquina de estados
    """

    def __init__(self):
        self._states = []
        self._transitions = {}
        self._initial_state = None
        self._current_state = None
        return

    def add_state(self, name, initial_state=False):
        """
        Anade estado a los estados validos de la maquina.
        :param name: nombre del estado
        """
        if name in self._states:
            return
        self._states.append(name)
        if initial_state:
            self._initial_state = name
            self._current_state = name

    def add_transition(self, name, from_state, to_state):
        """
        Anade transicion a partir de un nombre y dos estados.
        :param name: nombre de la transicion
        :param from_state: estado
        :param to_state: estado
        """
        if from_state not in self._states or to_state not in self._states:
            return
        if name in self._transitions:
            self._transitions[name][from_state] = to_state
        else:
            self._transitions[name] = {from_state: to_state}

    def set_state(self, state):
        """
        Setea el estado pasado por parametro como estado actual.
        :param state: estado
        """
        self._current_state = state

    def get_initial_state(self):
        """
        Devuelve el estado inicial de la maquina de estados
        """
        return self._initial_state

    def get_state(self):
        """
        Devuelve el estado actual.
        :return: Estado
        """
        return self._current_state

    def transite(self, name):
        """
        Transiciona una transicion si esta definida.
        :param name: nombre de la transicion
        :return: boolean si ha podido ejecutar la transicion.
        """
        if name in self._transitions:
            if self._current_state in self._transitions[name]:
                self._current_state = self._transitions[name][self._current_state]
                return True
        return False