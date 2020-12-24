# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\scenarioMgr\scenarioPlayer.py
# Compiled at: 2018-10-04 21:40:53
# Size of source mod 2**32: 6221 bytes
import os, re
try:
    import sc2techTree
except:
    sc2techTree = None

from sc2simulator import constants as c
from sc2simulator.scenarioMgr.scenarioUnit import convertTechUnit
from sc2simulator.setup.mapLocations import pickValidMapLoc

class ScenarioPlayer(object):
    __doc__ = 'sufficient info to fully represent a player within a scenario'

    def __init__(self, number, units, upgrades, pos=None, race=c.RANDOM):
        self._baseUnits = []
        self.number = number
        self._units = units
        self.upgrades = upgrades
        self.position = pos
        self.race = race

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<%s #%d %s units:%d upgrades:%d @ %s>' % (self.__class__.__name__,
         self.number, self.race, self.numUnits, self.numUpgrades,
         self.position)

    @property
    def baseUnits(self):
        if self._baseUnits:
            return self._baseUnits
        else:
            for u in self._units.values():
                if u.owner != self.number:
                    pass
                else:
                    if not u.base:
                        pass
                    else:
                        self._baseUnits.append(u)

            return self._baseUnits

    @property
    def loc(self):
        if self.position:
            return (c.cu.MapPoint)(*self.position)
        else:
            return c.cu.MapPoint(0.0, 0.0)

    @property
    def numUnits(self):
        return len(self.units)

    @property
    def numUpgrades(self):
        return len(self.upgrades)

    @property
    def units(self):
        return [u for u in self._units.values() if u.owner == self.number if not u.base]

    @property
    def upgradeReqs(self):
        """identify the producers and producing ability by extracting info from tech tree objects"""

        def exists(code, unitList):
            """identify the unit in unitList that matches code, else None"""
            for existingUnit in unitList:
                if existingUnit.code == code:
                    return existingUnit

        def getTechAbilities(tech, done, unitAbils, u=None):
            if tech in done:
                return unitAbils
            else:
                done.add(tech)
                cost, techUnit = max([(tu.cost.mineral, tu) for tu in tech.producingAbility.producers])
                if not u:
                    u = convertTechUnit(techUnit,
                      owner=(self.number), position=(pickValidMapLoc()))
                    unitAbils[u] = []
                    supplyUnit = techUnit.matchingSupplyDef
                    if supplyUnit.name == 'Pylon':
                        unitAbils[convertTechUnit(supplyUnit, owner=(self.number), position=(u.position))] = []
                producerTechUnit = sc2techTree.getUnit(u.nametype)
                if producerTechUnit.isAddon:
                    for name in re.findall('^([A-Z][a-z]+)', producerTechUnit.name):
                        parent = sc2techTree.getUnit(name)
                        uX, uY, uZ = u.position
                        parentPos = (uX - 2.5, uY + 0.5, uZ)
                        parentU = convertTechUnit(parent, owner=(self.number), position=parentPos)
                        unitAbils[parentU] = []

            for r in tech.requires:
                if r.isUnit:
                    if not exists(r.mType.code, unitAbils):
                        reqUnit = convertTechUnit(r,
                          owner=(self.number), position=(pickValidMapLoc()))
                        unitAbils[reqUnit] = []
                else:
                    if r.isUpgrade:
                        getTechAbilities(r, done, unitAbils, u=u)
                    else:
                        raise NotImplementedError('unclear what to do with the requirement type %s' % r)

            unitAbils[u].append(tech.producingAbility)

        ret = {}
        processedUpgrades = set()
        for tech in self.upgrades:
            getTechAbilities(tech, processedUpgrades, ret)

        return ret

    def display(self, indent=0, display=True):
        """pretty print ALL information about this player"""
        idt = ' ' * indent
        msg = []
        msg.append('%s%s' % (idt, self))
        msg.append('%s    %d unit(s):' % (idt, self.numUnits))
        for u in self.units:
            msg.append('%s        %s' % (idt, u))

        msg.append('%s    %d upgrade(s):' % (idt, self.numUpgrades))
        for u in self.upgrades:
            msg.append('%s        %s' % (idt, u))

        if display:
            for m in msg:
                print(m)

        else:
            return os.linesep.join(msg)