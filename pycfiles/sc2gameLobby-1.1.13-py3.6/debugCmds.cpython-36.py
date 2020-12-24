# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\debugCmds.py
# Compiled at: 2018-10-07 21:13:03
# Size of source mod 2**32: 3478 bytes
from s2clientprotocol.common_pb2 import Point2D
from s2clientprotocol.debug_pb2 import DebugCommand
from s2clientprotocol.debug_pb2 import DebugCreateUnit
from s2clientprotocol.debug_pb2 import DebugKillUnit
from s2clientprotocol.debug_pb2 import DebugSetUnitValue

def create(*units):
    """create this unit within the game as specified"""
    ret = []
    for unit in units:
        x, y = unit.position[:2]
        pt = Point2D(x=x, y=y)
        unit.tag = 0
        new = DebugCommand(create_unit=DebugCreateUnit(unit_type=(unit.code),
          owner=(unit.owner),
          pos=pt,
          quantity=1))
        ret.append(new)

    return ret


def modify(*units):
    """set the unit defined by in-game tag with desired properties
    NOTE: all units must be owned by the same player or the command fails."""
    ret = []
    for unit in units:
        for attr, idx in (('energy', 1), ('life', 2), ('shields', 3)):
            newValue = getattr(unit, attr)
            if not newValue:
                pass
            else:
                new = DebugCommand(unit_value=DebugSetUnitValue(value=newValue,
                  unit_value=idx,
                  unit_tag=(unit.tag)))
                ret.append(new)

    return ret


def remove(*tags):
    """remove the in-game units specified by tags from the game"""
    return DebugCommand(kill_unit=DebugKillUnit(tag=tags))


def revealMap():
    return setGameState(1)


def allowEnemyControl():
    return setGameState(2)


def disableFoodSupply():
    return setGameState(3)


def disableAllCosts():
    return setGameState(4)


def giveAllResources():
    return setGameState(5)


def enableGodMode():
    return setGameState(6)


def giveMineral():
    return setGameState(7)


def giveVespene():
    return setGameState(8)


def disableCooldown():
    return setGameState(9)


def disableTechReqs():
    return setGameState(10)


def advAllTechOneLevel():
    return setGameState(11)


def fastProduction():
    return setGameState(12)


def setGameState(enumVal):
    """reference lines 69-82 of this file:
    https://github.com/Blizzard/s2client-proto/blob/master/s2clientprotocol/debug.proto
    """
    return DebugCommand(game_state=(int(enumVal)))