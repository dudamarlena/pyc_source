# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\setScenario.py
# Compiled at: 2018-10-07 22:28:04
# Size of source mod 2**32: 12918 bytes
"""PURPOSE: launch the mini-editor to create custom p setups"""
import glob, os, re, stat, subprocess, time
from s2clientprotocol.sc2api_pb2 import Action, RequestAction
from sc2gameLobby import debugCmds
from sc2gameLobby import gameConstants as c
from sc2gameLobby.gameConfig import Config

def launchEditor(mapObj):
    """
    PURPOSE: launch the editor using a specific map object
    INPUT:   mapObj (sc2maptool.mapRecord.MapRecord)
    """
    cfg = Config()
    if cfg.is64bit:
        selectedArchitecture = c.SUPPORT_64_BIT_TERMS
    else:
        selectedArchitecture = c.SUPPORT_32_BIT_TERMS
    editorCmd = '%s -run %s -testMod %s -displayMode 1'
    fullAppPath = os.path.join(cfg.installedApp.data_dir, c.FOLDER_APP_SUPPORT % selectedArchitecture[0])
    appCmd = c.FILE_EDITOR_APP % selectedArchitecture[1]
    fullAppFile = os.path.join(fullAppPath, appCmd)
    baseVersion = cfg.version.baseVersion
    availableVers = [int(re.sub('^.*?Base', '', os.path.basename(path))) for path in glob.glob(os.path.join(c.FOLDER_MODS, 'Base*'))]
    selV = max([v for v in availableVers if v <= baseVersion])
    modFilepath = os.path.join(c.FOLDER_MODS, 'Base%s' % selV, c.FILE_EDITOR_MOD)
    os.chmod(fullAppFile, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR | stat.S_IWGRP | stat.S_IXGRP)
    finalCmd = editorCmd % (appCmd, mapObj.path, modFilepath)
    cwd = os.getcwd()
    os.chdir(fullAppPath)
    os.system(finalCmd)
    os.chdir(cwd)


def initScenario(controller, scenario, thisPlayerID, debug=False):
    """once in the in_game state, use the controller to set up the scenario"""

    def createUnitsWithTags(unitList, existingUnits={}, maxTries=25):
        """create each unit of unitList in game, identified by their tag"""
        createCmds = (debugCmds.create)(*unitList)
        (controller.debug)(*createCmds)
        triesRemaining = maxTries
        getGameState = controller.observe
        numNeededNewUnits = len(unitList)
        newUnits = {}
        while len(newUnits) < numNeededNewUnits and triesRemaining > 0:
            units = getGameState().observation.raw_data.units
            for i, unit in enumerate(unitList):
                if unit.tag:
                    pass
                else:
                    for liveUnit in units:
                        if liveUnit.unit_type != unit.code:
                            pass
                        else:
                            if liveUnit.owner != unit.owner:
                                pass
                            else:
                                if liveUnit.tag in existingUnits:
                                    pass
                                else:
                                    unit.tag = liveUnit.tag
                                    existingUnits[unit.tag] = liveUnit
                                    newUnits[unit.tag] = unit
                                    break

            triesRemaining -= 1

        return newUnits

    def detectCurrentUnits(**filters):
        detectedUnits = {}
        getGameState = controller.observe
        while 1:
            obs = getGameState()
            if obs.observation.game_loop <= 1:
                pass
            else:
                foundNewUnit = False
                for u in obs.observation.raw_data.units:
                    if u.tag in detectedUnits:
                        pass
                    else:
                        foundNewUnit = True
                        detectedUnits[u.tag] = u

                if foundNewUnit:
                    continue
            if detectedUnits:
                break

        if filters:
            return filterUnits(detectedUnits, **filters)
        else:
            return detectedUnits

    def filterUnits(unitDict, noNeutral=False, ownedOnly=False):
        """select the desired types of units from unitDict"""

        def allow(unit):
            if noNeutral:
                if unit.alliance == c.NEUTRAL:
                    return False
                else:
                    if unit.mineral_contents:
                        return False
                    if unit.vespene_contents:
                        return False
            if ownedOnly:
                if unit.owner != thisPlayerID:
                    return False
            return True

        if not (noNeutral or ownedOnly):
            return unitDict
        else:
            return {unit.tag:unit for unit in unitDict.values() if allow(unit)}

    def removeUnitsByKey(originalUnits=None, keepTags=[], **filters):
        """remove all detected units"""
        if originalUnits:
            units = filterUnits(originalUnits, **filters)
        else:
            originalUnits = detectCurrentUnits(**filters)
            units = originalUnits
        rmTags = list(units.keys())
        for keeper in keepTags:
            try:
                rmTags.remove(keeper)
            except:
                pass

        return removeUnitsByTag(*rmTags, **{'knownUnits': originalUnits})

    def removeUnitsByTag(*rmUnitTags, knownUnits={}):
        """remove specific units"""
        for rmTag in rmUnitTags:
            try:
                del knownUnits[rmTag]
            except:
                if not knownUnits:
                    break

        if rmUnitTags:
            rmCmd = (debugCmds.remove)(*rmUnitTags)
            controller.debug(rmCmd)
        return knownUnits

    def wait(delay, msg):
        if debug:
            print(msg)
        while 1:
            time.sleep(1)
            delay -= 1
            if delay > 0:
                if debug:
                    print('%d...' % delay)
                    continue
                    break

    knownUnits = detectCurrentUnits(noNeutral=True)
    for pIdx, p in scenario.players.items():
        baseUnits = scenario.newBaseUnits(pIdx)
        newUs = createUnitsWithTags((p.baseUnits), existingUnits=knownUnits)

    wait(2, 'delay before default unit deletion; %d remain' % len(newUs))
    if scenario.units:
        rmTags = []
        keepUnits = {
         19, 60, 95, 137}
        for unit in knownUnits.values():
            if unit.unit_type in keepUnits:
                pass
            else:
                rmTags.append(unit.tag)

        removeUnitsByTag(*rmTags, **{'knownUnits': knownUnits})
        wait(1, 'idle for unit kills (keep %d)' % len(knownUnits))
        removeUnitsByKey(keepTags=(knownUnits.keys()), noNeutral=True)
    if debug:
        print('%d remaining initial, known units' % len(knownUnits))
    initialUnits = dict(knownUnits)
    if thisPlayerID == 1:
        controller.debug(debugCmds.disableAllCosts(), debugCmds.allowEnemyControl(), debugCmds.fastProduction())
    wait(0.5, 'delay before creation')
    actionLists = []
    nonActionLists = []
    newU = {}
    for playerID, upgrades in scenario.upgrades.items():
        if not upgrades:
            continue
        reqs = scenario.players[playerID].upgradeReqs
        producingUnits = reqs.keys()
        if playerID == thisPlayerID:
            if debug:
                print('preparing %d upgrades for player #%d' % (len(upgrades), playerID))
            newU = createUnitsWithTags(producingUnits, existingUnits=knownUnits)
        for unit, toDoActions in reqs.items():
            for i, ability in enumerate(toDoActions):
                while len(actionLists) <= i:
                    actionLists.append([])
                    nonActionLists.append([])

                action = Action()
                uCmd = action.action_raw.unit_command
                uCmd.unit_tags.append(unit.tag)
                uCmd.queue_command = True
                uCmd.ability_id, ignoreTargetType = ability.getGameCmd()
                if playerID == thisPlayerID:
                    actionLists[i].append(action)
                else:
                    nonActionLists[i].append(action)

    for i, (al, nal) in enumerate(zip(actionLists, nonActionLists)):
        if debug:
            print('upgrade action list #%d commands: %d' % (i + 1, len(al)))
        if al:
            controller.actions(RequestAction(actions=al))
        else:
            if not nal:
                continue
            if i == 0:
                wait(6, "wait for all player's level 1 upgrades")
            else:
                if i == 1:
                    wait(7, "wait for all player's level 2 upgrades")
                elif i == 2:
                    wait(8, "wait for all player's level 3 upgrades")

    if thisPlayerID == 1:
        controller.debug(debugCmds.disableAllCosts(), debugCmds.allowEnemyControl(), debugCmds.fastProduction())
    wait(0.5, 'wait to disable cheats before proceeding')
    if thisPlayerID == 1:
        removeUnitsByKey(keepTags=initialUnits, noNeutral=True)
        wait(1.0, 'idle for unit kills')
        knownUnits = removeUnitsByKey(keepTags=initialUnits, noNeutral=True)
    cameraMv = Action()
    playerLoc = scenario.players[thisPlayerID].loc
    playerLoc.assignIntoInt(cameraMv.action_raw.camera_move.center_world_space)
    controller.actions(RequestAction(actions=[cameraMv]))
    if debug:
        print('repositioned camera')
    scenarioUnits = {}
    for p in scenario.players.values():
        newUnits = createUnitsWithTags((p.units), existingUnits=knownUnits)
        scenarioUnits.update(newUnits)

    modifyCmds = (debugCmds.modify)(*scenarioUnits.values())
    (controller.debug)(*modifyCmds)
    wait(0.1, 'allow modifications to finish')
    controller.debug(debugCmds.revealMap())
    if debug:
        print('scenario setup is finished')