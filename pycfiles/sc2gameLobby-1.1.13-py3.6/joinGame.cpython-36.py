# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\joinGame.py
# Compiled at: 2018-09-28 23:46:20
# Size of source mod 2**32: 6454 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pysc2.lib import protocol
from pysc2.lib import remote_controller
from pysc2.lib.sc_process import FLAGS
import base64, os, subprocess, sys, time
from sc2gameLobby.clientManagement import ClientController
from sc2gameLobby import gameConfig
from sc2gameLobby import gameConstants as c
from sc2gameLobby import resultHandler as rh
now = time.time

def playerJoin(config, agentCallBack, lobbyTimeout=c.INITIAL_TIMEOUT, debug=True):
    """cause an agent to join an already hosted game"""
    FLAGS(sys.argv)
    log = protocol.logging.logging
    log.disable(log.CRITICAL)
    amHosting = not bool(config.host)
    thisPlayer = config.whoAmI()
    operPrefix = 'HOST' if amHosting else 'JOIN'
    operType = '%sGAME' % operPrefix
    createReq = config.requestCreateDetails() if amHosting else None
    joinReq = config.requestJoinDetails()
    selectedIP = config.clientInitHost()
    selectPort = config.clientInitPort()
    controller = None
    finalResult = rh.playerSurrendered(config)
    replayData = ''
    if debug:
        print('[%s] Starcraft2 game process is launching (fullscreen=%s).' % (operType, config.fullscreen))
    with config.launchApp(ip_address=selectedIP, port=selectPort, connect=False):
        try:
            try:
                controller = ClientController()
                controller.connect(url=selectedIP, port=selectPort, timeout=lobbyTimeout)
                if amHosting:
                    if debug:
                        print('[%s] Starcraft2 host application is live. (%s)' % (operType, controller.status))
                        print('[%s] Creating Starcraft Game at %s' % (operType, controller))
                    controller.create_game(createReq)
                    if debug:
                        print('[%s] Starcraft2 is waiting for %d player(s) to join. (%s)' % (operType, config.numAgents, controller.status))
                        print('[%s] sending request to join game. (%s)' % (operType, controller.status))
                else:
                    timeToWait = c.DEFAULT_HOST_DELAY
                    for i in range(timeToWait):
                        if debug:
                            print('[%s] waiting %d seconds for the host to finish its init sequence.' % (operType, timeToWait - i))
                        time.sleep(1)

                joinResp = controller.join_game(joinReq)
                print('[%s] connection to %s:%d was successful. Game is starting! (%s)' % (operType, selectedIP, selectPort, controller.status))
                thisPlayer.playerID = int(joinResp.player_id)
                if debug:
                    print('[%s] joined match as %s.' % (operType, thisPlayer))
                config.updateIDs((controller.game_info()), tag=operType, debug=debug)
                if debug:
                    print('[%s] all %d player(s) found; game has started! (%s)' % (operType, config.numGameClients, controller.status))
                config.save()
                try:
                    agentCallBack(config.name)
                except Exception as e:
                    print('ERROR: agent %s crashed during init: %s (%s)' % (thisPlayer.initCmd, e, type(e)))
                    return (rh.playerCrashed(config), '')

                getGameState = controller.observe
                startWaitTime = now()
                while 1:
                    obs = getGameState()
                    result = obs.player_result
                    if result:
                        finalResult = rh.idPlayerResults(config, result)
                        break
                    try:
                        agentCallBack(obs)
                    except Exception as e:
                        print('%s ERROR: agent callback %s of %s crashed during game: %s' % (type(e), agentCallBack, thisPlayer.initCmd, e))
                        finalResult = rh.playerCrashed(config)
                        break

                    newNow = now()
                    if newNow - startWaitTime > c.REPLAY_SAVE_FREQUENCY:
                        replayData = controller.save_replay()
                        startWaitTime = newNow

                replayData = controller.save_replay()
            except (protocol.ConnectionError, protocol.ProtocolError, remote_controller.RequestError) as e:
                if 'Status.in_game' in str(e):
                    finalResult = rh.playerSurrendered(config)
                else:
                    finalResult = rh.playerDisconnected(config)
                    print('%s Connection to game host has ended, even intentionally by agent. Message:%s%s' % (type(e), os.linesep, e))
            except KeyboardInterrupt:
                if debug:
                    print('caught command to forcibly shutdown Starcraft2 client.')
                finalResult = rh.playerSurrendered(config)

        finally:
            if replayData:
                replayData = base64.encodestring(replayData).decode()
            if controller:
                controller.quit()

    return (
     finalResult, replayData)