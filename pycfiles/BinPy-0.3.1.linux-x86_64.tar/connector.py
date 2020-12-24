# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/Gates/connector.py
# Compiled at: 2014-04-21 09:30:38
from __future__ import division

class Connector:
    """
    This class is the primary medium for data transfer. Objects of this
    class can be connected to any digital object.

    Example
    =======

    >>> from BinPy import *
    >>> conn = Connector(1)  #Initializing connector with initial state = 1
    >>> conn.state
    1
    >>> gate = OR(0, 1)
    >>> conn.tap(gate, 'output')  #Tapping the connector

    Methods
    =======

    * tap
    * untap
    * isInputof
    * isOutputof
    * trigger
    """

    def __init__(self, state=None):
        self.connections = {'output': [], 'input': []}
        self.state = state
        self.oldstate = None
        return

    def tap(self, element, mode):
        if mode == 'output':
            self.connections['output'] = []
        if element not in self.connections[mode]:
            self.connections[mode].append(element)

    def untap(self, element, mode):
        if element in self.connections[mode]:
            self.connections[mode].remove(element)
        else:
            raise Exception('ERROR:Connector is not the %s of the passed element' % mode)

    def isInputof(self, element):
        return element in self.connections['input']

    def isOutputof(self, element):
        return element in self.connections['output']

    def trigger(self):
        for i in self.connections['input']:
            i.trigger()

    def __call__(self):
        return self.state

    def __bool__(self):
        if self.state == 1:
            return True
        return False

    __nonzero__ = __bool__

    def __int__(self):
        if self.state == 1:
            return 1
        return 0

    def __float__(self):
        return float(self.state)

    def __repr__(self):
        return str(self.state)

    def __str__(self):
        return 'Connector; State: ' + str(self.state)

    def __add__(self, other):
        return self.state + other.state

    def __sub__(self, other):
        return self.state - other.state

    def __mul__(self, other):
        return self.state * other.state

    def __truediv__(self, other):
        return self.state / other.state