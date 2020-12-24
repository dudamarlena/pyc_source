# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\setup\unitSelection.py
# Compiled at: 2018-10-04 22:53:49
# Size of source mod 2**32: 3022 bytes
"""
Automatically generate a 'random' unit composition setup for two players using
an approximately equivalent resource values for each player.  The races of each
player are random unless specifically declared.
"""
import random, re
try:
    import sc2techTree
    techtree = sc2techTree.getLastTree()
except Exception:
    techtree = None

from sc2simulator.setup.simpleSelection import selectSimpleUnits
from sc2simulator.setup.treeSelection import selectUnitList

def generatePlayerUnits(scenario, playerID, race, rules, location, mapData):
    if techtree:
        playerUnits = selectUnitList(sc2techTree, race, rules, mapData)
        for techUnit in playerUnits:
            allUnits = scenario.units.values()
            if techUnit.energyStart:
                energyMax = techUnit.energyMax
                if rules.energy:
                    energyVal = min(rules.energy, energyMax)
                else:
                    if rules.energyMax:
                        energyVal = energyMax
                    else:
                        if rules.energyRand:
                            energyVal = random.randint(0, energyMax)
                        else:
                            energyVal = techUnit.energyStart
            else:
                energyVal = 0
            newUnit = scenario.updateUnit(techUnit=techUnit, owner=playerID, position=location,
              energy=energyVal)

    else:
        for unitCode in selectSimpleUnits(race, rules, mapData):
            newUnit = scenario.updateUnit(position=location, owner=playerID, code=unitCode)


def generateUpgrades(scenario, playerID, options):
    """identify the upgrades corresponding to the specified options"""
    if playerID == 1:
        upgradeStr = options.upgrades
    else:
        upgradeStr = options.enemyUpgrades
    if not upgradeStr:
        return
    if not techtree:
        raise ValueError('cannot determine upgrades without the sc2techTree  (given: %s)' % upgradeStr)
    for techPart in re.split('[,:;]+', upgradeStr):
        try:
            techKey = int(techPart)
            tech = sc2techTree.getUpgradeByID(techKey)[0]
        except ValueError:
            techKey = techPart
            try:
                tech = sc2techTree.getUpgrade(techKey)
            except KeyError:
                raise KeyError("could not identify upgrade: '%s'" % techKey)

        except IndexError:
            raise IndexError("could not identify upgrade ID: '%s'" % techKey)

        scenario.addUpgrade(playerID, tech)