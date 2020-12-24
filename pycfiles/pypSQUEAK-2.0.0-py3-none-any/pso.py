# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dswistowski/pso/pypso/src/pypso/pso.py
# Compiled at: 2007-07-01 05:48:09
__doc__ = 'Główny moduł systemu. Zawiera klasy implementujące algorytm pso. Nie zawiera on ani strategii poruszania się cząsteczek, ani sposobu obliczania wartości pozycji, lecz pobiera te wszystkie dane z biblioteki strategii oraz biblioteki funkcji'
from math import sqrt
from pypso.functions import Boundary, Function, ELengthMismatch, Vector
from pypso.strategies import randomStrategy
from pypso.parameters import Parameters
from pypso import library
from pypso.particle import BIG_FLOAT

class Pso(Parameters):
    u"""
        Klasa reprezentująca całe stado.
        """
    __parameters__ = {'maxiter': (1000, 1, 200000, 0, 'Maksymalna liczba iteracji')}

    def __init__(self):
        self.function_library = library.function_library
        self.strategy_library = library.strategy_library
        super(Pso, self).__init__()
        self._gbest = BIG_FLOAT
        self._function = self.function_library.get('F1')[0]
        self._strategy = self.strategy_library.get('simple_PSO')[0]
        self.restart()

    def set_function(self, function):
        self._function = function

    def set_strategy(self, strategy):
        self._strategy = strategy

    def get_function(self):
        return self._function

    def get_strategy(self):
        return self._strategy

    def get_gbest(self):
        return self._gbest

    def get_gbestpos(self):
        return self._gbestpos

    def __str__(self):
        s = ''
        i = 1
        for agent in self._agents:
            s += 'Agent: #%i\n%s\n' % (i, str(agent))
            i = i + 1

        return s

    def parameter_set(self, name, value):
        if name == 'm':
            self.resize(value)

    def resize(self, size):
        u"""Zmiana wielkości stada"""
        old_size = len(self._agents)
        if old_size > size:
            self._agents = self._agents[:size]
            return
        if old_size < size:
            for i in range(size - old_size):
                self._agents.append(Particle(self))

        return

    def step(self):
        """Wykonanie iteracji algorytmu"""
        for agent in self._agents:
            if agent.fitness < self._gbest:
                self._gbest = agent.get_fitness()
                self._gbestpos = agent._p[:]

        if self._strategy != None:
            self._strategy(self)
            try:
                for agent in self._agents:
                    agent.step()

            except ELengthMismatch:
                self.restart()
            except ValueError:
                self.restart()
            else:
                self._stepno = self._stepno + 1
        return self._stepno

    def restart(self):
        u"""Uruchomienie algorytnu od początku"""
        self._agents = []
        self._stepno = 0
        if self._strategy != None:
            self._strategy.restart(self)
        return


if __name__ == '__main__':
    pso = Pso()
    print pso