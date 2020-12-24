# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\simulation\commons.py
# Compiled at: 2016-04-20 14:58:08
# Size of source mod 2**32: 1639 bytes
from mad.evaluation import Symbols

class SimulatedEntity:
    __doc__ = '\n    Factor out commonalities between all simulated entities\n    '

    def __init__(self, name, environment):
        self.environment = environment
        self.name = name
        self.simulation = self.environment.look_up(Symbols.SIMULATION)

    @property
    def schedule(self):
        return self.simulation.schedule

    @property
    def listener(self):
        listener = self.environment.look_up(Symbols.LISTENER)
        assert listener is not None, "Error: Simulated entity '{0}' has no listener".format(self.name)
        return listener

    def look_up(self, symbol):
        return self.environment.look_up(symbol)

    @property
    def factory(self):
        return self.simulation.factory

    def next_request_id(self):
        return self.simulation.next_request_id()