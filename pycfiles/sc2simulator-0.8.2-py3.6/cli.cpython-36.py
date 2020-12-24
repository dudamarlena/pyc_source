# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2simulator\cli.py
# Compiled at: 2018-10-09 07:59:16
# Size of source mod 2**32: 13515 bytes
"""
PURPOSE: simulate a 1v1 scenario to test player actions.
"""
import argparse, os, re, shutil, subprocess, sys, time
from sc2ladderMgmt import getLadder
from sc2maptool import selectMap
from sc2maptool.mapRecord import MapRecord
from sc2maptool.cli import getSelectionParams
from sc2maptool.cli import optionsParser as addMapOptions
from sc2gameLobby import launcher
from sc2gameLobby.gameConfig import Config
from sc2gameLobby.setScenario import launchEditor
from sc2players import getPlayer, PlayerPreGame
from sc2simulator.__version__ import __version__
from sc2simulator import constants as c
from sc2simulator.setup import getSetup
from sc2simulator.setup.functions import getBankFilepath

def optionsParser(passedParser=None):
    if passedParser == None:
        parser = argparse.ArgumentParser(description=__doc__,
          epilog=('version: %s' % __version__))
    else:
        parser = passedParser
    mainOptions = parser.add_argument_group('Training Simulator Operations')
    mainOptions.add_argument('--editor', action='store_true', help='launch the scenario editor')
    mainOptions.add_argument('--regression', default='', help='run a predefined battery of test cases', metavar='NAMES')
    mainOptions.add_argument('--custom', action='store_true', help='play customized scenario(s) toward your own objectives using specified map')
    mainOptions.add_argument('--join', action='store_true', help="join another player's custom scenarior setup (your race is determined by the host)")
    simControlO = parser.add_argument_group('Gameplay control options')
    simControlO.add_argument('--repeat', default=1, type=int, help='the number of learning iterations performed per test.', metavar='INT')
    simControlO.add_argument('--duration', default=(c.DEF_DURATION), type=float, help=('how long this generated scenario should last (default: %d)' % c.DEF_DURATION), metavar='INT')
    simControlO.add_argument('--players', default='', help='the ladder player name(s) to control a player (comma separated).', metavar='NAMES')
    simControlO.add_argument('--replaydir', default=(c.PATH_NEW_MATCH_DATA), help='the path where generated replays will be stored.',
      metavar='PATH')
    addMapOptions(parser)
    predefOptns = parser.add_argument_group('Predefined Scenario options (from the editor)')
    predefOptns.add_argument('--cases', default='', help='the specific sc2 bank setup names (comma separated)', metavar='NAMES')
    predefOptns.add_argument('--cleandelay', default=10, type=int, help='number of seconds before temporary files are removed allowing the editor to launch successfully', metavar='INT')
    newGenOptns = parser.add_argument_group('Dynamically generated composition options')
    newGenOptns.add_argument('--race', default=(c.RANDOM), choices=(c.types.SelectRaces.ALLOWED_TYPES), help='the race this agent will play (default: random)')
    newGenOptns.add_argument('--enemyrace', default=(c.RANDOM), choices=(c.types.SelectRaces.ALLOWED_TYPES), help='the race your enemy will play (default: random)')
    newGenOptns.add_argument('--loc', default='', help="where this agent's army will be clustered", metavar='X,Y')
    newGenOptns.add_argument('--enemyloc', default='', help="where the enemy's army will be clustered", metavar='X,Y')
    newGenOptns.add_argument('--distance', default=(c.DEF_PLAYER_DIST), type=int, help=("the distance between each player's armies when either player's location isn't specified (default: %.1f)" % c.DEF_PLAYER_DIST), metavar='NUMBER')
    newGenOptns.add_argument('--unitsMin', default=(c.DEF_UNITS_MIN), type=int, help='the minimum number of units each player shall control', metavar='INT')
    newGenOptns.add_argument('--unitsMax', default=(c.DEF_UNITS_MAX), type=int, help='the maximum number of units each player shall control', metavar='INT')
    newGenOptns.add_argument('--allowDefense', action='store_true', help='defense structures can also be selected as part of the unit count')
    newGenOptns.add_argument('--air', action='store_true', help='all generated units must be air units')
    newGenOptns.add_argument('--ground', action='store_true', help='all generated units must be non-air units')
    newGenOptns.add_argument('--defense', default=0, type=int, help='include this many defensive structures for each player', metavar='INT')
    newGenOptns.add_argument('--detectors', default=0, type=int, help='include this many mobile detectors for each player', metavar='INT')
    sc2mapsOpts = parser.add_argument_group('Dynamic composition options WITHOUT sc2maps package')
    sc2mapsOpts.add_argument('--dimensions', default='150,150', help='provide actual map dimensions', metavar='X,Y')
    techTreeOpt = parser.add_argument_group('Dynamic composition options with sc2techTree package')
    techTreeOpt.add_argument('--mineral', default=99999, type=int, help='the target amount of mineral of each army composition', metavar='INT')
    techTreeOpt.add_argument('--vespene', default=99999, type=int, help='the target amount of vespene of each army composition', metavar='INT')
    techTreeOpt.add_argument('--supply', default=99999, type=int, help='the maximum supply each army composition will consume', metavar='INT')
    techTreeOpt.add_argument('--maxdps', default=99999, type=int, help='the target amount of total dps (damage per second) of each army composition', metavar='NUMBER')
    techTreeOpt.add_argument('--maxhp', default=99999, type=int, help='the target amount of total hp (hit points) of each army composition', metavar='NUMBER')
    techTreeOpt.add_argument('--energy', default=0, type=int, help='each caster will have this energy or their max, whichever is lower', metavar='NUMBER')
    techTreeOpt.add_argument('--energyMax', action='store_true', help='all casters have maximum energy')
    techTreeOpt.add_argument('--energyRand', action='store_true', help='all casters have a random amount of energy between 0 and their maximum')
    techTreeOpt.add_argument('--upgrades', default='', help='the names or IDs that your agent will start with', metavar='IDs')
    techTreeOpt.add_argument('--enemyUpgrades', default='', help='the names or IDs that your opponent will start with', metavar='IDs')
    return parser


def defineLaunchOptions(scenario, replayOut):
    """create a configuration that is compatible with the game launcher"""

    class Dummy:
        pass

    ret = Dummy()
    ret.search = False
    ret.history = False
    ret.nogui = True
    ret.nofog = True
    ret.scenario = scenario
    ret.savereplay = replayOut
    return ret


def main(options=None):
    if options == None:
        parser = optionsParser()
        options = parser.parse_args()
        sys.argv = sys.argv[:1]
    else:
        try:
            specifiedMap = selectMap(
 options.mapname, excludeName=options.exclude, 
             closestMatch=True, **getSelectionParams(options))
        except Exception as e:
            print(e)
            return

        outTempName = specifiedMap.name + '_%d_%d.' + c.SC2_REPLAY_EXT
        outTemplate = os.path.join(options.replaydir, outTempName)
        if options.editor:
            bankFile = getBankFilepath(specifiedMap.name)
            if os.path.isfile(bankFile):
                bankName = re.sub('\\..*?$', '', os.path.basename(bankFile))
                bankDir = os.path.dirname(bankFile)
                dirTime = re.sub('\\.', '_', str(time.time()))
                tmpDir = os.path.join(bankDir, '%s_%s' % (bankName, dirTime))
                tmpXml = os.path.join(tmpDir, c.FILE_BANKLIST)
                tmpName = '%s.%s' % (bankName, c.SC2_MAP_EXT)
                tmpMapPath = os.path.join(tmpDir, tmpName)
                cfg = Config()
                dstMapDir = cfg.installedApp.mapsDir
                dstMapPath = os.path.join(dstMapDir, tmpName)
                if os.path.isdir(tmpDir):
                    shutil.rmtree(tmpDir)
                try:
                    os.makedirs(tmpDir)
                    shutil.copyfile(specifiedMap.path, tmpMapPath)
                    with open(tmpXml, 'w') as (f):
                        f.write(c.BANK_DATA % bankName)
                    if cfg.is64bit:
                        mpqApp = c.PATH_MPQ_EDITOR_64BIT
                    else:
                        mpqApp = c.PATH_MPQ_EDITOR_32BIT
                    cmd = c.MPQ_CMD % (mpqApp, tmpMapPath, tmpXml, c.FILE_BANKLIST)
                    x = subprocess.call(cmd)
                    print('Loaded previously defined %s scenarios.' % bankName)
                    if os.path.isfile(dstMapPath):
                        os.remove(dstMapPath)
                    shutil.copyfile(tmpMapPath, dstMapPath)
                    tmpRecord = MapRecord(specifiedMap.name, dstMapPath, {})
                    launchEditor(tmpRecord)
                finally:
                    time.sleep(options.cleandelay)
                    if os.path.isdir(tmpDir):
                        shutil.rmtree(tmpDir)
                    while 1:
                        try:
                            os.remove(dstMapPath)
                            break
                        except:
                            time.sleep(2)

            else:
                launchEditor(specifiedMap)
        else:
            if options.regression:
                batteries = options.test.split(',')
                raise NotImplementedError('TODO -- run each test battery')
            else:
                if options.custom:
                    playerNames = re.split('[,\\s]+', options.players)
                    if len(playerNames) != 2:
                        if not options.players:
                            playerNames = ''
                        raise ValueError("must specify two players, but given %d: '%s'" % (
                         len(playerNames), playerNames))
                    try:
                        thisPlayer = getPlayer(playerNames[0])
                    except Exception:
                        print("ERROR: player '%s' is not known" % playerNames[0])
                        return
                    else:
                        if options.race == c.RANDOM:
                            options.race = thisPlayer.raceDefault
                        cfg = Config(themap=specifiedMap, ladder=getLadder('versentiedge'), 
                         players=[
 PlayerPreGame(thisPlayer, selectedRace=(c.types.SelectRaces(options.race)))], 
                         mode=c.types.GameModes(c.MODE_1V1), 
                         opponents=playerNames[1:], 
                         whichPlayer=thisPlayer.name, 
                         fogDisabled=True, **thisPlayer.initOptions)
                        cfg.raw = True
                        scenarios = getSetup(specifiedMap, options, cfg)
                        for scenario in scenarios:
                            epoch = int(time.time())
                            failure = False
                            for curLoop in range(1, options.repeat + 1):
                                outFile = outTemplate % (epoch, curLoop)
                                launchOpts = defineLaunchOptions(scenario, outFile)
                                failure = launcher.run(launchOpts, cfg=cfg)
                                if failure:
                                    break

                            if failure:
                                break

                else:
                    if options.join:
                        raise NotImplementedError('TODO -- implement remote play')
                    else:
                        parser.print_help()
                        print('ERROR: must select a main option.')