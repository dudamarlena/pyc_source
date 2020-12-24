# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\setup\functions.py
# Compiled at: 2018-10-08 10:40:33
# Size of source mod 2**32: 4178 bytes
"""
Fully define a 'random' generated setup for the players per specified conditions
"""
import random, re
from sc2simulator import constants as c
from sc2simulator.scenarioMgr import Scenario, parseBankXml, getBankFilepath
from sc2simulator.setup import mapLocations
from sc2simulator.setup.mapLocations import convertStrToPoint, defineLocs
from sc2simulator.setup.unitSelection import generateUpgrades
from sc2simulator.setup.unitSelection import generatePlayerUnits

def getSetup(mapObj, options, cfg):
    """get the appropriate scenarios, whether predefined or custom generated"""
    mdata = None
    try:
        import sc2maps
        mData = sc2maps.MapData(mapName=(mapObj.name))
        mapLocations.mapDimensions = mData.dimensions.toCoords()
        mdata = mData.placement.halfGrid
    except Exception:
        try:
            if not options.dimensions:
                raise ValueError('must provide dims')
            mapLocations.mapDimensions = convertStrToPoint(options.dimensions)
            if len(mapLocations.mapDimensions) < 2:
                raise ValueError('must provide valid dimensions (given: %s)' % mapLocations.mapDimensions)
        except ValueError:
            print('ERROR: must provide valid map dimensions (given: %s' % options.dimensions)
            return []
        else:
            mdata = mapLocations.mapDimensions

    scenarios = []
    if options.cases:
        try:
            bankName = getBankFilepath(mapObj.name)
            bank = parseBankXml(bankName)
        except:
            print("ERROR: failed to load specified bank '%s'" % mapObj.name)
            return scenarios
        else:
            for scenarioName in re.split('[,;:]+', options.cases):
                try:
                    scenarios.append(bank.scenarios[scenarioName])
                except:
                    print("WARNING: scenario '%s' was not found in bank %s" % (
                     scenarioName, bankName))

    else:
        scenarios += generateScenario(mapObj, options, cfg, mdata)
    return scenarios


def generateScenario(mapObj, options, cfg, mdata):
    """override this function is different generation methods are desired"""
    scenario = Scenario('custom%s' % mapObj.name)
    scenario.duration = options.duration
    d = options.distance
    mapLocs = defineLocs(options.loc, options.enemyloc, d)
    givenRaces = [options.race, options.enemyrace]
    for i, (pLoc, r) in enumerate(zip(mapLocs, givenRaces)):
        race = pickRace(r)
        pIdx = i + 1
        scenario.addPlayer(pIdx, loc=pLoc, race=race)
        generatePlayerUnits(scenario, pIdx, race, options, pLoc, mapData=mdata)
        try:
            generateUpgrades(scenario, pIdx, options)
        except Exception as e:
            print('ERROR: %s' % e)
            return []

    return [
     scenario]


def pickRace(specifiedRace):
    """ensure the selected race for scenario generation is a race, not random"""
    if specifiedRace == c.RANDOM:
        choices = list(c.types.SelectRaces.ALLOWED_TYPES.keys())
        choices.remove(c.RANDOM)
        newRace = random.choice(choices)
        return newRace
    else:
        return specifiedRace