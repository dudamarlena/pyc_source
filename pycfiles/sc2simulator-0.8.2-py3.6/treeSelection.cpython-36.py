# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\setup\treeSelection.py
# Compiled at: 2018-10-04 23:26:47
# Size of source mod 2**32: 5438 bytes
"""
unit selection that requires the sc2techTree package
"""
import random
from sc2simulator import constants as c
from sc2simulator.setup.simpleRaceMap import codeMap

def selectUnitList(treeMod, race, rules, mapData, numFails=0):
    """pick units that meet all criteria"""
    units = []
    newRules = copyRules(rules)
    motherShipPicked = False
    available = set()
    tree = treeMod.getLastTree()
    ignoredTypes = {12, 31, 58, 85, 113, 128, 151, 501, 687, 892}
    for u in tree._leaves[race].values():
        for p in u.produces:
            if any([ignoreType == p.mType for ignoreType in ignoredTypes]):
                pass
            else:
                available.add(p)

    while len(units) < rules.unitsMax:
        u = pickRandomUnit(available, newRules, motherShipPicked)
        if u == None:
            if rules.unitsMin < len(units):
                break
            else:
                if numFails < c.MAX_UNIT_GRP_TRIES:
                    print('Criteria failed %d times; unit selection has restarted' % (numFails + 1))
                    return selectUnitList(available, rules, mapData, numFails + 1)
                else:
                    print('FAILED to select units after %d attempts.' % numFails)
                    return []
        else:
            if u.name == 'Mothership':
                motherShipPicked = True
            units.append(u)

    if rules.defense:
        remaining = int(rules.defense)
        available = [treeMod.getUnitByID(code)[0] for code in codeMap[race]['defense']]
        while remaining > 0:
            newU = random.choice(available)
            units.append(newU)
            remaining -= 1

    if rules.detectors:
        remaining = int(rules.detectors)
        available = [treeMod.getUnitByID(code)[0] for code in codeMap[race]['detection']]
        while remaining > 0:
            newU = random.choice(available)
            units.append(newU)
            remaining -= 1

    return units


def pickRandomUnit(choices, rules, ms=False):

    def isValidSelection(unit):
        if not unit.isUnit:
            return False
        else:
            if unit.isStructure:
                if not unit.weapons:
                    return False
                else:
                    if not rules.allowDefense:
                        return False
                    else:
                        if rules.air:
                            if not unit.isAir:
                                return False
                            if rules.ground:
                                if unit.isAir:
                                    return False
                        else:
                            if unit.dps > rules.maxdps:
                                return False
                            if unit.hits > rules.maxhp:
                                return False
                        cost = unit.cost
                        if cost.mineral > rules.mineral:
                            return False
                    if cost.vespene > rules.vespene:
                        return False
                if -cost.supply > rules.supply:
                    return False
            else:
                if ms:
                    if unit.name == 'Mothership':
                        return False
            return True

    def confirmSelection(unit):
        rules.mineral -= unit.cost.mineral
        rules.vespene -= unit.cost.vespene
        rules.supply += unit.cost.supply
        rules.maxdps -= unit.dps
        rules.maxhp -= unit.healthMax
        return unit

    choices = list(choices)
    while True:
        try:
            selection = random.choice(choices)
        except:
            return
        else:
            if isValidSelection(selection):
                break
            choices.remove(selection)

    return confirmSelection(selection)


def copyRules(originals):
    """create a similarly structured object as the provided options, but one which can be safely modified"""

    class Dummy:
        pass

    ret = Dummy()
    ret.mineral = originals.mineral
    ret.vespene = originals.vespene
    ret.supply = originals.supply
    ret.maxdps = originals.maxdps
    ret.maxhp = originals.maxhp
    ret.allowDefense = originals.allowDefense
    ret.air = originals.air
    ret.ground = originals.ground
    ret.unitsMin = originals.unitsMin
    ret.unitsMax = originals.unitsMax
    return ret