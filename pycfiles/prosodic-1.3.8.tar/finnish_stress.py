# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/Dropbox/LITLAB/CODE/prosodic/dicts/fi/syllabifier/finnish_stress.py
# Compiled at: 2012-12-06 15:11:04
from finnish_functions import *
from copy import deepcopy
stress_dict = {}

def make_stresses(weights):
    stresses = []
    if len(weights) == 1 and not is_heavy(weights[0]):
        return [
         [
          Stress.none]]
    if len(weights) > 0:
        stresses += [Stress.primary]
    for i in range(1, len(weights)):
        stresses += [Stress.none]

    stress_parity = 0
    i = 2
    while i < len(weights) - 1:
        if i % 2 == stress_parity:
            if stresses[(i + 1)] != Stress.none or is_heavier(weights[(i + 1)], weights[i]) and i + 1 < len(weights) - 1:
                stresses[i + 1] = Stress.secondary
                i += 1
                stress_parity = (stress_parity + 1) % 2
            else:
                stresses[i] = Stress.secondary
        i += 2

    stresses = [stresses]
    if len(weights) > 1 and is_heavy(weights[(-1)]):
        if stresses[0][(-2)] == Stress.none:
            stresses += deepcopy(stresses)
            stresses[1][-1] = Stress.secondary
        elif stresses[0][(-2)] == Stress.secondary and not is_heavy(weights[(-2)]):
            stresses += deepcopy(stresses)
            stresses[1][-1] = Stress.secondary
            stresses[1][-2] = Stress.none
    return stresses