# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yeison/Development/gcpds/gym-bci/gym_bci/envs/pacman/ghostAgents.py
# Compiled at: 2019-11-13 21:55:24
# Size of source mod 2**32: 3248 bytes
from .game import Agent, Actions, Directions
from .util import manhattanDistance, raiseNotDefined, chooseFromDistribution, Counter

class GhostAgent(Agent):

    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        return chooseFromDistribution(dist)

    def getDistribution(self, state):
        """Returns a Counter encoding a distribution over actions from the provided state."""
        raiseNotDefined()


class RandomGhost(GhostAgent):
    __doc__ = 'A ghost that chooses a legal action uniformly at random.'

    def getDistribution(self, state):
        dist = Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        else:
            dist.normalize()
            return dist


class DirectionalGhost(GhostAgent):
    __doc__ = 'A ghost that prefers to rush Pacman, or flee when scared.'

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        if len(legalActions) == 0:
            return {}
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0
        speed = 1
        if isScared:
            speed = 0.5
        else:
            actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
            newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
            pacmanPosition = state.getPacmanPosition()
            distancesToPacman = [manhattanDistance(pos, pacmanPosition) for pos in newPositions]
            if len(distancesToPacman) == 0:
                import pdb
                pdb.set_trace()
            if isScared:
                bestScore = max(distancesToPacman)
                bestProb = self.prob_scaredFlee
            else:
                bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if distance == bestScore]
        dist = Counter()
        for a in bestActions:
            dist[a] = bestProb / len(bestActions)
        else:
            for a in legalActions:
                dist[a] += (1 - bestProb) / len(legalActions)
            else:
                dist.normalize()
                return dist