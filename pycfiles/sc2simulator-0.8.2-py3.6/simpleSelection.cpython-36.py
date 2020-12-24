# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\setup\simpleSelection.py
# Compiled at: 2018-10-04 22:34:16
# Size of source mod 2**32: 1301 bytes
import random
from sc2simulator.setup.simpleRaceMap import codeMap

def selectSimpleUnits(race, rules, mapData):

    def pick(choices, count=1):
        choices = list(choices)
        return [random.choice(choices) for i in range(count)]

    ret = []
    available = set()
    if rules.allowDefense:
        available |= codeMap[race]['defense']
    if rules.air:
        available |= codeMap[race]['air']
    if rules.ground:
        available |= codeMap[race]['ground']
    else:
        if not rules.air:
            available |= codeMap[race]['air']
            available |= codeMap[race]['ground']
    if not rules.detectors:
        available |= codeMap[race]['detection']
    if rules.defense:
        ret += pick(codeMap[race]['defense'], rules.addDefense)
    if rules.detectors:
        ret += pick(codeMap[race]['detection'], rules.detectors)
    ret += pick(available, count=(random.randint(rules.unitsMin, rules.unitsMax)))
    return ret