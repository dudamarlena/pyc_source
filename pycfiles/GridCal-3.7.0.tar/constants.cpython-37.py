# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/santi/Documentos/GitHub/GridCal/src/GridCal/ThirdParty/pulp/constants.py
# Compiled at: 2019-07-13 06:16:34
# Size of source mod 2**32: 2584 bytes
"""
This file contains the constant definitions for PuLP
Note that hopefully these will be changed into something more pythonic
"""
VERSION = '1.6.11'
EPS = 1e-07
LpContinuous = 'Continuous'
LpInteger = 'Integer'
LpBinary = 'Binary'
LpCategories = {LpContinuous: 'Continuous', 
 LpInteger: 'Integer', 
 LpBinary: 'Binary'}
LpMinimize = 1
LpMaximize = -1
LpSenses = {LpMaximize: 'Maximize', 
 LpMinimize: 'Minimize'}
LpStatusNotSolved = 0
LpStatusOptimal = 1
LpStatusInfeasible = -1
LpStatusUnbounded = -2
LpStatusUndefined = -3
LpStatus = {LpStatusNotSolved: 'Not Solved', 
 LpStatusOptimal: 'Optimal', 
 LpStatusInfeasible: 'Infeasible', 
 LpStatusUnbounded: 'Unbounded', 
 LpStatusUndefined: 'Undefined'}
LpConstraintLE = -1
LpConstraintEQ = 0
LpConstraintGE = 1
LpConstraintSenses = {LpConstraintEQ: '=', 
 LpConstraintLE: '<=', 
 LpConstraintGE: '>='}
LpCplexLPLineSize = 78

def isiterable(obj):
    try:
        obj = iter(obj)
    except:
        return False
        return True


class PulpError(Exception):
    __doc__ = '\n    Pulp Exception Class\n    '