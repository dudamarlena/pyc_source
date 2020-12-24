# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/gym_bci/envs/pacman/pacmanAgents.py
# Compiled at: 2019-11-13 19:04:27
# Size of source mod 2**32: 2247 bytes
from .pacman import Directions
from .game import Agent
import random
from .game import Agent
from .util import lookup

class LeftTurnAgent(Agent):
    __doc__ = 'An agent that turns left at every opportunity'

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP:
            current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal:
            return left
        if current in legal:
            return current
        if Directions.RIGHT[current] in legal:
            return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal:
            return Directions.LEFT[left]
        return Directions.STOP


class GreedyAgent(Agent):

    def __init__(self, evalFn='scoreEvaluation'):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)


class OpenAIAgent(Agent):
    __doc__ = '\n        Just a placeholder.\n    '

    def __init__(self):
        pass


def scoreEvaluation(state):
    return state.getScore()