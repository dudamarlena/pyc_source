# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/possibleStates.py
# Compiled at: 2014-08-29 00:09:34
import fsc
from copy import copy
from pdb import set_trace
from pprint import pprint

def determineRelevantSubwordLenghts(n, state):
    """
This function register states to their possible relevant subword
lenghts. 

(See Definition 4.0.22 for "relevant subword")
    """
    minProfilLen = 0
    if len(state) > 0:
        rightMostPosition = max(state, key=lambda s: s.i)
        minProfilLen = rightMostPosition.i
    return (minProfilLen, 2 * n + 1)


def transition(n, profil, pos, withTransitions):
    i = pos.i
    e = pos.e
    w = len(profil)
    positions = []
    if pos.isTransposition:
        if profil[i] == 1:
            return [fsc.StandardPosition(i + 2, e)]
        else:
            return positions

    if withTransitions and w - i >= 2 and profil[i:i + 2] == [0, 1]:
        positions += [fsc.TPosition(i, e + 1)]
    if i < w and profil[i] is 1:
        return [fsc.StandardPosition(i + 1, e)]
    else:
        positions += [fsc.StandardPosition(i, e + 1), fsc.StandardPosition(i + 1, e + 1)]
        if i < w:
            k = fsc.positiveK(profil[i:i + min(n - e + 1, len(profil) - i)])
            if k is not None:
                positions.append(fsc.StandardPosition(i + k, e + k - 1))
        positions = filter(lambda s: s.i <= w, positions)
        positions = filter(lambda s: s.e <= n, positions)
        return positions


def getNextState(n, profil, state, withTransitions):
    nextState = []
    for pos in state:
        nextState += transition(n, profil, pos, withTransitions)

    difference = 0
    if len(nextState) > 0:
        nextState = fsc.reduce(nextState, n)
        difference = nextState[0].i - state[0].i
        if difference > 0:
            for pos in nextState:
                pos.i = pos.i - difference

    return (
     nextState, difference)


def genAllProfilPowerSet(n):
    set = [ [] for i in range(2 * n + 2) ]
    set[0] = [[]]
    for i in range(1, 2 * n + 2):
        for j in [0, 1]:
            set[i] += map(lambda s: [j] + s, set[(i - 1)])

    return set


def genTransitions(n, withTransitions=True):
    allProfils = genAllProfilPowerSet(n)
    transitions = [ {} for i in range(2 * n + 2) ]
    processedStates = []
    unprocessedStates = [
     [
      fsc.StandardPosition(0, 0)]]
    while len(unprocessedStates) > 0:
        state = unprocessedStates.pop()
        processedStates.append(state)
        profilLenMin, profilLenMax = determineRelevantSubwordLenghts(n, state)
        for profilLen in range(profilLenMin, profilLenMax + 1):
            for profil in allProfils[profilLen]:
                nextState, difference = getNextState(n, profil, state, withTransitions)
                transitions[profilLen].setdefault(str(profil), {}).setdefault(str(state), (nextState, difference))
                if nextState != [] and nextState not in processedStates and nextState not in unprocessedStates:
                    unprocessedStates.append(nextState)

    return transitions


if __name__ == '__main__':
    pprint([genTransitions(2)])