# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\resultHandler.py
# Compiled at: 2018-07-09 21:33:29
# Size of source mod 2**32: 2887 bytes
from sc2gameLobby import gameConstants as c

def tieDetermined(cfg):
    """all players tied their results"""
    return assignValue(cfg, c.RESULT_TIE, c.RESULT_TIE)


def launchFailure(cfg):
    """report that the match failed to start as anticipated"""
    return assignValue(cfg, c.RESULT_UNDECIDED, c.RESULT_UNDECIDED)


def playerSurrendered(cfg):
    """the player has forceibly left the game"""
    if cfg.numAgents + cfg.numBots == 2:
        otherResult = c.RESULT_VICTORY
    else:
        otherResult = c.RESULT_UNDECIDED
    return assignValue(cfg, c.RESULT_DEFEAT, otherResult)


def playerCrashed(cfg):
    """occurs when a player's understood state hasn't changed for too long"""
    return assignValue(cfg, c.RESULT_CRASH, c.RESULT_UNDECIDED)


def playerDisconnected(cfg):
    """occurs when a game client loses its connection from the host"""
    return assignValue(cfg, c.RESULT_DISCONNECT, c.RESULT_UNDECIDED)


def assignValue(cfg, playerValue, otherValue):
    """artificially determine match results given match circumstances.
    WARNING: cheating will be detected and your player will be banned from server"""
    player = cfg.whoAmI()
    result = {}
    for p in cfg.players:
        if p.name == player.name:
            val = playerValue
        else:
            val = otherValue
        result[p.name] = val

    return result


def idPlayerResults(cfg, rawResult):
    """interpret standard rawResult for all players with known IDs"""
    result = {}
    knownPlayers = []
    dictResult = {plyrRes.player_id:plyrRes.result for plyrRes in rawResult}
    for p in cfg.players:
        if p.playerID and p.playerID in dictResult:
            knownPlayers.append(p)
            result[p.name] = dictResult[p.playerID]

    return result