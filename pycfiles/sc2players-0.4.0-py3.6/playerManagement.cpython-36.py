# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2players\playerManagement.py
# Compiled at: 2018-09-29 00:00:12
# Size of source mod 2**32: 5888 bytes
"""
PURPOSE: manage records of all known players, both local and remote
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six import iteritems, itervalues
import glob, os, re, time
from sc2players import constants as c
from sc2players.playerRecord import PlayerRecord
from sc2players.playerPreGame import PlayerPreGame
playerCache = {}

def addPlayer(settings):
    """define a new PlayerRecord setting and save to disk file"""
    _validate(settings)
    player = PlayerRecord(settings)
    player.save()
    getKnownPlayers()[player.name] = player
    return player


def updatePlayer(name, settings):
    """update an existing PlayerRecord setting and save to disk file"""
    player = delPlayer(name)
    _validate(settings)
    player.update(settings)
    player.save()
    getKnownPlayers()[player.name] = player
    return player


def getPlayer(name):
    """obtain a specific PlayerRecord settings file"""
    if isinstance(name, PlayerRecord):
        return name
    try:
        return getKnownPlayers()[name.lower()]
    except KeyError:
        raise ValueError("given player name '%s' is not a known player definition" % name)


def delPlayer(name):
    """forget about a previously defined PlayerRecord setting by deleting its disk file"""
    player = getPlayer(name)
    try:
        os.remove(player.filename)
    except IOError:
        pass

    try:
        del getKnownPlayers()[player.name]
    except:
        pass

    return player


def buildPlayer(name, ptype, cmd='', options={}, difficulty=None, rating=None, race=None, obs=False, pid=0, raceDefault=c.RANDOM):
    newRating = rating or c.DEFAULT_RATING
    if not isinstance(difficulty, c.ComputerDifficulties):
        newDiff = c.ComputerDifficulties(difficulty)
    else:
        newDiff = difficulty
    ret = PlayerRecord(name=name, type=ptype, initCmd=cmd, initOptions=options, difficulty=newDiff,
      rating=newRating,
      raceDefault=raceDefault)
    if bool(race or obs or pid):
        return PlayerPreGame(ret, selectedRace=race, observe=obs, playerID=pid)
    else:
        return ret


def getKnownPlayers(reset=False):
    """identify all of the currently defined players"""
    global playerCache
    if not playerCache or reset:
        jsonFiles = os.path.join(c.PLAYERS_FOLDER, '*.json')
        for playerFilepath in glob.glob(jsonFiles):
            filename = os.path.basename(playerFilepath)
            name = re.sub('^player_', '', filename)
            name = re.sub('\\.json$', '', name)
            player = PlayerRecord(name)
            playerCache[player.name] = player

    return playerCache


def getBlizzBotPlayers():
    """identify all of Blizzard's built-in bots"""
    ret = {}
    for pName, p in iteritems(getKnownPlayers()):
        if p.isComputer:
            ret[pName] = p

    return ret


def getStaleRecords(limit=c.DEFAULT_TIME_LIMIT):
    ret = []
    now = time.time()
    seconds = float(limit) * 24 * 60 * 60
    maxNoAct = min(seconds, c.NO_ACTIVITY_LIMIT * 24 * 60 * 60)
    for player in itervalues(getKnownPlayers()):
        if player.matches:
            sinceLastMatch, match = sorted([(now - m.endTime, m) for m in player.matches])[0]
            if sinceLastMatch > seconds:
                ret.append(player)
            else:
                sinceCreation = now - player.created
                if sinceCreation > maxNoAct:
                    ret.append(player)

    return ret


def removeStaleRecords(**kwargs):
    """identify all currently stale records and remove them"""
    return [delPlayer(record) for record in getStaleRecords(**kwargs)]


def _validate(settings):
    if 'created' in settings:
        raise ValueError("parameter 'created' is expected to be automatmically generated.")
    if '_matches' in settings:
        raise ValueError('matches are declared after playing matches, not during init.')


__all__ = [
 'addPlayer', 'getPlayer', 'delPlayer', 'getKnownPlayers', 'getBlizzBotPlayers',
 'updatePlayer', 'getStaleRecords', 'removeStaleRecords']