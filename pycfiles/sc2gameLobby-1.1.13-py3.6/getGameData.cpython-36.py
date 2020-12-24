# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\getGameData.py
# Compiled at: 2018-12-08 10:24:34
# Size of source mod 2**32: 4781 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from s2clientprotocol import sc2api_pb2 as sc_pb
from pysc2.lib import protocol
from pysc2.lib import remote_controller
from pysc2.lib.sc_process import FLAGS
from sc2common import types as t
from sc2gameLobby import gameConfig
from sc2gameLobby import gameConstants as c
from sc2maptool import selectMap
from sc2players import PlayerPreGame
import os, sys, time
now = time.time

def run(debug=False):
    """PURPOSE: start a starcraft2 process using the defined the config parameters"""
    FLAGS(sys.argv)
    config = gameConfig.Config(version=None,
      themap=selectMap(ladder=True),
      players=[
     'defaulthuman', 'blizzbot2_easy'])
    createReq = sc_pb.RequestCreateGame(realtime=(config.realtime),
      disable_fog=(config.fogDisabled),
      random_seed=(int(now())),
      local_map=sc_pb.LocalMap(map_path=(config.mapLocalPath), map_data=(config.mapData)))
    joinRace = None
    for player in config.players:
        reqPlayer = createReq.player_setup.add()
        playerObj = PlayerPreGame(player)
        if playerObj.isComputer:
            reqPlayer.difficulty = playerObj.difficulty.gameValue()
            pType = playerObj.type.type
        else:
            pType = c.PARTICIPANT
        reqPlayer.type = t.PlayerControls(pType).gameValue()
        reqPlayer.race = playerObj.selectedRace.gameValue()
        if not playerObj.isComputer:
            joinRace = reqPlayer.race

    interface = sc_pb.InterfaceOptions()
    raw, score, feature, rendered = config.interfaces
    interface.raw = raw
    interface.score = score
    interface.feature_layer.width = 24
    joinReq = sc_pb.RequestJoinGame(options=interface)
    joinReq.race = joinRace
    if debug:
        print('Starcraft2 game process is launching.')
    controller = None
    with config.launchApp() as (controller):
        try:
            try:
                if debug:
                    print('Starcraft2 application is live. (%s)' % controller.status)
                controller.create_game(createReq)
                if debug:
                    print('Starcraft2 is waiting for %d player(s) to join. (%s)' % (config.numAgents, controller.status))
                playerID = controller.join_game(joinReq).player_id
                print('[GET IN-GAME DATA] player#%d %s' % (playerID, config))
                return (controller.ping(), controller.data())
            except (protocol.ConnectionError, protocol.ProtocolError, remote_controller.RequestError) as e:
                if debug:
                    print('%s Connection to game closed (NOT a bug)%s%s' % (type(e), os.linesep, e))
                else:
                    print('Connection to game closed.')
            except KeyboardInterrupt:
                print('caught command to forcibly shutdown Starcraft2 host server.')

        finally:
            config.disable()
            controller.quit()