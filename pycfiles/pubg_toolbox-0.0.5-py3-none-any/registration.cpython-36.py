# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/suliman/Documents/Projects/pipTests/PUBGbot/pubgReports/registration.py
# Compiled at: 2019-10-15 00:50:49
# Size of source mod 2**32: 3407 bytes
import csv
try:
    from . import PUBGstats
except:
    import PUBGstats

import os
PLAYERSFILE = 'PLAYERS.csv'
directory = os.path.dirname(__file__)
filepath = os.path.join(directory, PLAYERSFILE)

def checkRegistration(discordName, PUBGName):
    global filepath
    with open(filepath, 'r') as (fil):
        r = csv.reader(fil)
        next(r)
        lineNum = 1
        for line in r:
            if line[0] == discordName:
                if line[1] == PUBGName:
                    return True
                else:
                    return lineNum
            lineNum += 1

        return False


def registerPlayer(discordName, PUBGName):
    result = checkRegistration(discordName, PUBGName)
    isPUBGPlayer = PUBGstats.getPlayerInfo(PUBGName)
    if isPUBGPlayer == False:
        result = -1
    if result == True:
        if isinstance(result, bool) == True:
            return 'User ({}) is already registered with the PUBG name ({})'.format(discordName, PUBGName)
    if result == False:
        with open(filepath, 'a') as (fil):
            toAdd = [
             discordName, PUBGName]
            w = csv.writer(fil)
            w.writerows([toAdd])
            return 'User ({}) is now registered with the PUBG name ({})'.format(discordName, PUBGName)
    if isinstance(result, int) == True and result > 0:
        with open(filepath, 'r') as (fil):
            r = csv.reader(fil)
            lists = list(r)
            oldPUBGName = lists[result][1]
            lists[result][1] = PUBGName
            with open(filepath, 'w') as (wfil):
                w = csv.writer(wfil)
                w.writerows(lists)
        return 'User ({}) PUBG name has been updated from ({}) to ({})'.format(discordName, oldPUBGName, PUBGName)
    else:
        if result == -1:
            return "({}) is not a valid PUBG name (the player's profile has not been found on the PUBG servers)".format(PUBGName)
        return False


def getRegisteredPlayers():
    with open(filepath, 'r') as (fil):
        r = csv.reader(fil)
        next(r)
        players = list(r)
    return players


def getSpecificPlayer(discordName):
    with open(filepath, 'r') as (fil):
        r = csv.reader(fil)
        next(r)
        for player in r:
            if player[0] == discordName:
                return player[1]


def main():
    """
    result = checkRegistration('suli', 'stx0')
    print('case suli, stx0, result: {}'.format(result))
    result = checkRegistration('suli', 'none')
    print('case suli, none, result: {}'.format(result))
    result = checkRegistration('su', 'none')
    print('case su, none, result: {}'.format(result))
    """
    print(getSpecificPlayer('suli'))


if __name__ == '__main__':
    main()
# global PLAYERSFILE ## Warning: Unused global