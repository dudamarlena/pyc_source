# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\launcher.py
# Compiled at: 2018-10-26 00:07:51
# Size of source mod 2**32: 12709 bytes
"""
Copyright 2018 Versentiedge LLC All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import base64, importlib, json, os, re, requests, subprocess, sys, time
from sc2players import addPlayer, getPlayer, PlayerPreGame, PlayerRecord
from sc2ladderMgmt import getLadder
from sc2gameLobby.gameConfig import Config
from sc2gameLobby import connectToServer
from sc2gameLobby import gameConstants as c
from sc2gameLobby import genericObservation as go
from sc2gameLobby import host, join
from sc2gameLobby import resultHandler as rh
from sc2gameLobby import versions

def exitStatement(msg, code=1):
    printMsg = msg
    if code:
        printMsg = 'ERROR: %s' % msg
    print('%s%s' % (os.linesep, printMsg))
    return code


def badConnect(ladder, code=2):
    return exitStatement(('A connection could not be made. %s may not be available or you may not be connected to the internet.' % ladder),
      code=code)


def getLaunchConfig(options):
    player = PlayerPreGame((getPlayer(options.player)), selectedRace=(options.race), observe=(options.observe))
    ret = Config(expo=(c.EXPO_SELECT[options.exp]),
      version=(options.version),
      ladder=(getLadder(options.ladder)),
      players=[
     player],
      whichPlayer=(player.name),
      mode=(c.types.GameModes(options.mode)),
      themap=(options.map),
      numObservers=(options.obs),
      trust=True,
      fogDisabled=(options.nofog),
      stepSize=(options.step),
      opponents=(options.opponents.split(',') if options.opponents else []),
      fullscreen=(not options.windowed),
      raw=(options.raw),
      score=(options.score),
      feature=(options.feature),
      render=(options.rendered))
    ret.connection
    return ret


def run(options, cfg=None):
    if options.search or options.history:
        if not options.player:
            options.player = options.search
        if cfg == None:
            cfg = getLaunchConfig(options)
        try:
            httpResp = connectToServer.ladderPlayerInfo(cfg, (options.search), getMatchHistory=(options.history))
        except requests.exceptions.ConnectionError:
            return badConnect(cfg.ladder)
        else:
            if not httpResp.ok:
                return exitStatement(httpResp.text)
            printStr = '%15s : %s'
            for playerAttrs, playerHistory in httpResp.json():
                player = PlayerRecord(source=playerAttrs)
                print(player)
                for k in ('type', 'difficulty', 'initCmd', 'rating'):
                    print(printStr % (k, getattr(player, k)))

                if 'created' in playerAttrs:
                    print(printStr % ('created', time.strftime('%Y-%m-%d', time.localtime(player.created))))
                if playerHistory:
                    for h in playerH:
                        print(printStr % ('history', h))

                print()

    else:
        if options.nogui:
            if cfg == None:
                cfg = getLaunchConfig(options)
            try:
                httpResp = connectToServer.sendMatchRequest(cfg)
            except requests.exceptions.ConnectionError:
                return badConnect(cfg.ladder)
            else:
                if not httpResp.ok:
                    return exitStatement(httpResp.text)
                else:
                    data = httpResp.json()
                    for pData in data['players']:
                        pName = pData[0]
                        try:
                            getPlayer(pName)
                        except ValueError:
                            try:
                                y = connectToServer.ladderPlayerInfo(cfg, pName)
                            except requests.exceptions.ConnectionError:
                                return badConnect(cfg.ladder)
                            else:
                                settings = y[0][0]
                                del settings['created']
                                addPlayer(settings)

                    matchCfg = Config()
                    matchCfg.loadJson(data)
                    print('SERVER-ASSIGNED CONFIGURATION')
                    matchCfg.display()
                    print()
                    thisPlayer = matchCfg.whoAmI()
                    result = None
                    replayData = ''
                    callback = go.doNothing
                    if thisPlayer.initCmd:
                        if re.search('^\\w+\\.[\\w\\.]+$', thisPlayer.initCmd):
                            parts = thisPlayer.initCmd.split('.')
                            moduleName = parts[0]
                            try:
                                thing = importlib.import_module(moduleName)
                                for part in parts[1:]:
                                    thing = getattr(thing, part)

                                callback = thing()
                            except ModuleNotFoundError as e:
                                return exitStatement('agent %s initialization command (%s) did not begin with a module (expected: %s). Given: %s' % (thisPlayer.name, thisPlayer.initCmd, moduleName, e))
                            except AttributeError as e:
                                return exitStatement('invalid %s init command format (%s): %s' % (thisPlayer, thisPlayer.initCmd, e))
                            except Exception as e:
                                return exitStatement('general failure to initialize agent %s: %s %s' % (thisPlayer.name, type(e), e))

                        else:
                            p = subprocess.Popen(thisPlayer.initCmd.split())
                            p.communicate()
                            msg = 'Command-line bot %s finished normally.' % thisPlayer
                            if p.returncode:
                                msg = 'Command-line bot %s crashed (%d).' % (
                                 thisPlayer, p.returncode)
                                try:
                                    httpResp = connectToServer.reportMatchCompletion(matchCfg, result, replayData)
                                    if not httpResp.ok:
                                        msg += ' %s!' % httpResp.text
                                except requests.exceptions.ConnectionError:
                                    msg += ' lost prior connection to %s!' % cfg.ladder

                            return exitStatement(msg, code=(p.returncode))
                    try:
                        try:
                            if matchCfg.host:
                                func = join
                            else:
                                func = host
                            result, replayData = func(matchCfg, agentCallBack=callback, scenario=(options.scenario))
                        except c.TimeoutExceeded as e:
                            print(e)
                            result = rh.launchFailure(matchCfg)

                    finally:
                        if hasattr(callback, 'shutdown'):
                            callback.shutdown()
                        callback = None

                    replaySize = len(replayData) if replayData else 0
                    if replaySize:
                        if not options.scenario:
                            print('FINAL RESULT: (%d)' % replaySize)
                            print(json.dumps(result, indent=4))
                            if options.savereplay:
                                dirName = os.path.dirname(options.savereplay)
                                if dirName:
                                    if not os.path.isdir(dirName):
                                        os.makedirs(dirName)
                                with open(options.savereplay, 'wb') as (f):
                                    f.write(replayData)
                if result != None:
                    try:
                        replayData = base64.encodestring(replayData).decode()
                        httpResp = connectToServer.reportMatchCompletion(matchCfg, result, replayData)
                        if not httpResp.ok:
                            return exitStatement(httpResp.text)
                        if httpResp.text:
                            if 'invalid' in httpResp.text:
                                return ValueError
                    except requests.exceptions.ConnectionError:
                        return badConnect(cfg.ladder)
                    except Exception as e:
                        return exitStatement('%s: %s' % (type(e), e))

                    if replaySize:
                        print(httpResp.json())
        else:
            if options.add:
                (versions.addNew)(*options.add.split(','))
            else:
                if options.update:
                    keys = ['label',
                     'version',
                     'base-version',
                     'data-hash',
                     'fixed-hash',
                     'replay-hash']
                    data = {}
                    for k, v in zip(keys, options.update.split(',')):
                        data[k] = v

                    versions.handle.update(data)
                    versions.handle.save()
                else:
                    if options.versions:
                        for v, record in sorted(versions.handle.ALL_VERS_DATA.items()):
                            print(v)
                            for k, v in sorted(record.items()):
                                print('%15s: %s' % (k, v))

                            print()

                    else:
                        if cfg == None:
                            cfg = getLaunchConfig(options)
                        cfg.display()
                        print('ERROR: GUI mode is not yet implemented.')