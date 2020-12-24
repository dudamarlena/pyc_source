# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/exceptions.py
# Compiled at: 2016-03-06 13:24:18
# Size of source mod 2**32: 808 bytes
"""This module contains exception classes from Pyramid Web Framework."""

class ConfigurationError(Exception):
    __doc__ = ' Raised when inappropriate input values are supplied to an API\n    method of a :term:`Configurator`'


class CyclicDependencyError(Exception):
    __doc__ = ' This class is a copy of ``pyramid.exceptions.CyclicDependencyError``.\n\n    The exception raised when the Pyramid topological sorter detects a\n    cyclic dependency.'

    def __init__(self, cycles):
        self.cycles = cycles

    def __str__(self):
        L = []
        cycles = self.cycles
        for cycle in cycles:
            dependent = cycle
            dependees = cycles[cycle]
            L.append('%r sorts before %r' % (dependent, dependees))

        msg = 'Implicit ordering cycle:' + '; '.join(L)
        return msg