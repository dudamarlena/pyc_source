# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/errors.py
# Compiled at: 2018-06-14 23:17:51


class EvolutionException(Exception):
    """Base class for a Django Evolution exception."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class CannotSimulate(EvolutionException):
    """A mutation cannot be simulated."""
    pass


class SimulationFailure(EvolutionException):
    """A mutation simulation has failed."""
    pass


class EvolutionNotImplementedError(EvolutionException, NotImplementedError):
    """An operation is not supported by the mutation or database backend."""
    pass