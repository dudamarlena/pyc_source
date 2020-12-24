# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\connectToServer.py
# Compiled at: 2018-07-09 21:33:28
# Size of source mod 2**32: 2898 bytes
"""
PURPOSE: send request communications to a ladder server

    sendMatchResult()

    requestMatch()
        find matchup
        listen for matchup assignment
        launch client using assignment info
        issue commands as assigned
        play game
            if W, agent app result code  = 0
            else  agent app result code != 0
        reportResult() to ladder

    export / publish data
        standings by W/L
        standings by games played / sportsmanship rating
        hottest streak in standings w/ 5+ games
        service getPlayerData() request (provide info about a ladder's players)
"""
from six import iteritems
import json, requests
from sc2gameLobby import gameConstants as c
from sc2players import addPlayer, getPlayer

def cancelMatchRequest(cfg):
    """obtain information housed on the ladder about playerName"""
    payload = json.dumps([cfg.thePlayer])
    ladder = cfg.ladder
    return requests.post(url=(c.URL_BASE % (ladder.ipAddress, ladder.serverPort, 'cancelmatch')),
      data=payload)


def ladderPlayerInfo(cfg, playerName, getMatchHistory=False):
    """obtain information housed on the ladder about playerName"""
    payload = json.dumps([playerName, getMatchHistory])
    ladder = cfg.ladder
    return requests.post(url=(c.URL_BASE % (ladder.ipAddress, ladder.serverPort, 'playerstats')),
      data=payload)


def reportMatchCompletion(cfg, results, replayData):
    """send information back to the server about the match's winners/losers"""
    payload = json.dumps([cfg.flatten(), results, replayData])
    ladder = cfg.ladder
    return requests.post(url=(c.URL_BASE % (ladder.ipAddress, ladder.serverPort, 'matchfinished')),
      data=payload)


def sendMatchRequest(cfg):
    payload = cfg.toJson()
    ladder = cfg.ladder
    return requests.post(url=(c.URL_BASE % (ladder.ipAddress, ladder.serverPort, 'newmatch')),
      data=payload)