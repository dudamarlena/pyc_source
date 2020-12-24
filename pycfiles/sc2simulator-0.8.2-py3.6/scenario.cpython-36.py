# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\scenarioMgr\scenario.py
# Compiled at: 2018-10-07 19:34:25
# Size of source mod 2**32: 7347 bytes
import random
try:
    import sc2techTree
    techtree = sc2techTree.getLastTree()
except Exception as e:
    techtree = None

from sc2simulator import constants as c
from sc2simulator.scenarioMgr.scenarioPlayer import ScenarioPlayer
from sc2simulator.scenarioMgr.scenarioUnit import ScenarioUnit, convertTechUnit
from sc2simulator.setup.mapLocations import pickCloserLoc, pickFurtherLoc

class Scenario(object):
    __doc__ = 'contains all information required to set up a scenario'

    def __init__(self, name):
        self.name = name
        self.players = {}
        self.units = {}
        self.upgrades = {}
        self.startloop = 1
        self.duration = c.DEF_DURATION

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<%s '%s' players:%s>" % (self.__class__.__name__,
         self.name, sorted(list(self.players.keys())))

    def addPlayer(self, idx, loc=None, race=None):
        """add a definition for a player within a Scenario"""
        idx = int(idx)
        if idx in self.players:
            print('WARNING: attempted to add already existing player %d: %s' % (
             idx, self.players[idx]))
            return self.players[idx]
        upgradeList = []
        self.upgrades[idx] = upgradeList
        p = ScenarioPlayer(idx, (self.units), upgradeList, pos=loc, race=race)
        self.players[idx] = p

    def addUnit(self, tag=0, newUnit=None, allowDuplicate=False, **attrs):
        """define a unit within a Scenario"""

        def genTag(minVal=150):
            usedUnits = self.units
            newTag = random.randint(minVal, c.MAX_TAG)
            while newTag in usedUnits:
                newTag = random.randint(minVal, c.MAX_TAG)

            return newTag

        if tag:
            tag = int(tag)
        else:
            tag = genTag()
        if tag in self.units:
            if not allowDuplicate:
                print('WARNING: unit tag %d already exists in %s as %s' % (
                 tag, self, self.units[tag]))
            return
        else:
            if newUnit:
                if not isinstance(newUnit, ScenarioUnit):
                    newUnit = convertTechUnit(newUnit, tag=tag, **attrs)
            else:
                newUnit = ScenarioUnit(tag)
                (newUnit.update)(**attrs)
            self.units[tag] = newUnit
            return newUnit

    def addUpgrade(self, player, upgrade):
        """define an upgrade within a Scenario"""
        if player not in self.players:
            self.addPlayer(player)
        if isinstance(upgrade, str):
            if not techtree:
                raise NotImplementedError("upgrade '%s' cannot be defined unless the sc2techTree package is available" % upgrade)
            upgrade = sc2techTree.getUpgrade(upgrade)
        self.upgrades[player].append(upgrade)

    def newBaseUnits(self, playerID):
        """define a set of new 'base' units for the specified player"""
        player = self.players[playerID]
        if player.baseUnits:
            return player.baseUnits
        else:
            location = player.position
            x0, y0 = location[:2]
            if player.race == c.ZERG:
                off = 2
                for i in range(0, 2):
                    newUnit = self.updateUnit(tag=0, base=True, nametype='NydusNetwork',
                      code=95,
                      owner=playerID,
                      position=(pickCloserLoc(location, 5 * i)),
                      energy=0,
                      life=850,
                      shields=0)

                for x, y in [(0, -off), (-off, 0), (off, 0), (0, off)]:
                    targetX, targetY = location[:2]
                    unitLoc = (targetX + x, targetY + y)
                    newUnit = self.updateUnit(tag=0, base=True, nametype='CreepTumorBurrowed',
                      code=137,
                      owner=playerID,
                      position=unitLoc,
                      energy=0,
                      life=50,
                      shields=0)

            else:
                if player.race == c.PROTOSS:
                    for i in range(0, 4):
                        newUnit = self.updateUnit(tag=0, base=True, nametype='Pylon',
                          code=60,
                          owner=playerID,
                          position=(pickCloserLoc(location, 4 * i)),
                          energy=0,
                          life=200,
                          shields=200)

                else:
                    if player.race == c.TERRAN:
                        for i in range(0, 4):
                            newUnit = self.updateUnit(tag=0, base=True, nametype='SupplyDepot',
                              code=19,
                              owner=playerID,
                              position=(pickCloserLoc(location, 4 * i)),
                              energy=0,
                              life=400,
                              shields=0)

                    else:
                        raise ValueError('bad race value: %s' % player.race)
            return player.baseUnits

    def updateUnit(self, tag=0, techUnit=None, **attrs):
        """include more information to better represent the specified unit"""
        try:
            u = self.units[tag]
            (u.update)(**attrs)
        except KeyError:
            u = (self.addUnit)(tag, newUnit=techUnit, **attrs)
            if u.owner:
                if u.owner not in self.players:
                    self.addPlayer(u.owner)

        return u