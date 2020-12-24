# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/exception.py
# Compiled at: 2017-12-28 04:09:42


class AssimuloException(Exception):
    pass


class Algebraic_Exception(AssimuloException):
    pass


class AssimuloRecoverableError(AssimuloException):
    pass


class TerminateSimulation(AssimuloException):
    pass


class TimeLimitExceeded(AssimuloException):
    pass


class DiscardValue(AssimuloException):
    pass


class Explicit_ODE_Exception(AssimuloException):
    pass


class ODE_Exception(AssimuloException):
    pass


class Implicit_ODE_Exception(AssimuloException):
    pass


class Rodas_Exception(AssimuloException):
    pass


class Dopri5_Exception(AssimuloException):
    pass


class GLIMDA_Exception(AssimuloException):
    pass


class ODEPACK_Exception(AssimuloException):
    pass


class DASP3_Exception(AssimuloException):
    pass


class RKStarter_Exception(AssimuloException):
    pass