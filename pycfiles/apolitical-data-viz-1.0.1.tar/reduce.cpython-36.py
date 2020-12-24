# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/reduce.py
# Compiled at: 2019-06-15 16:42:10
# Size of source mod 2**32: 591 bytes
import numpy as np, apogee as ap

def factor_reduce(factor, evidence, val=0.0):
    if np.any(np.isin(factor.scope, evidence[0])):
        assignments = factor.assignments
        parameters = np.ones(len(assignments)) * val
        factor_map = ap.index_map_1d(factor.scope, [evidence[0]])
        for i, assignment in enumerate(assignments):
            if assignment[factor_map] == int(evidence[1]):
                parameters[i] = factor.parameters[i]

        return (factor.scope, factor.cards, parameters)
    else:
        return (
         factor.scope, factor.cards, factor.parameters)