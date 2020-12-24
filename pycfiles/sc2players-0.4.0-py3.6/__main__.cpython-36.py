# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2players\__main__.py
# Compiled at: 2018-09-29 00:49:25
# Size of source mod 2**32: 6325 bytes
"""
command-line interface to interact with the player repository
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six import itervalues
import argparse, sys, time
from sc2players import constants as c
from sc2players.__version__ import __version__
from sc2players.playerManagement import *
from sc2players.playerRecord import PlayerRecord
if __name__ == '__main__':
    usage_def = ''
    parser = argparse.ArgumentParser(description=__doc__,
      epilog=('version: %s' % __version__))
    actionOpts = parser.add_argument_group('player record action options (pick at most one)')
    actionOpts.add_argument('criteria', nargs='*', help=('define additional attributes as key=value pairs.  KEYS: %s' % ', '.join(PlayerRecord.AVAILABLE_KEYS)))
    actionOpts.add_argument('--add', action='store_true', help='Add settings as a new player definition. (Provide criteria)')
    actionOpts.add_argument('--update', type=str, help='update settings for selected record.')
    actionOpts.add_argument('--get', type=str, help='the specific player to highlight.')
    actionOpts.add_argument('--rm', type=str, help='the specific player to remove from the player database.')
    actionOpts.add_argument('--stale', type=float, help='select all stale player records (specify value in days)')
    actionOpts.add_argument('--rmstale', type=float, help='remove all stale player records (specify value in days)')
    filterOpts = parser.add_argument_group('player --get filter options')
    filterOpts.add_argument('--exclude', action='store_true', help='exclude players with names specified by --get.')
    filterOpts.add_argument('--best', action='store_true', help='match players that are closer with --get')
    displayOpts = parser.add_argument_group('display options')
    displayOpts.add_argument('--details', default=None, action='store_true', help='show details of each player identified.')
    displayOpts.add_argument('--summary', action='store_true', help='show an additional summary')
    displayOpts.add_argument('--matches', type=int, help='display the most recent X matches')
    displayOpts.add_argument('--apm', type=int, help='calculate the apm for the most recent X matches (0 = all matches)')
    options = parser.parse_args()
    criteria = {}
    terms = [a.split('=') for a in options.criteria]
    try:
        for i, (k, v) in enumerate(terms):
            criteria[k] = v

    except ValueError:
        print("ERROR: key '%s' must specify a value using '=' followed by a value (no whitespace)." % terms[i][0])
        sys.exit(1)

    action = True
    if options.stale:
        records = getStaleRecords(limit=(options.stale))
    else:
        if options.rmstale:
            records = removeStaleRecords(limit=(options.rmstale))
        else:
            if options.get:
                records = [
                 getPlayer(options.get)]
                options.summary = True
            else:
                if options.add:
                    records = [
                     addPlayer(criteria)]
                    options.details = True
                    options.summary = True
                else:
                    if options.update:
                        records = [
                         updatePlayer(options.update, criteria)]
                        options.details = True
                        options.summary = True
                    else:
                        if options.rm:
                            records = [
                             delPlayer(options.rm)]
                            options.details = True
                            options.summary = True
                        else:
                            records = list(itervalues(getKnownPlayers(reset=True)))
                            action = False
        for r in records:
            printStr = '%15s : %s'
            print(r)
            if options.details:
                attrs = [
                 (
                  'type', r.type)]
                if r.type in [c.BOT, c.AI]:
                    attrs.append(('init command', r.initCmd))
                attrs.append(('init options', r.initOptStr))
                attrs.append(('default race', r.raceDefault))
                attrs.append(('total matches', len(r.matches)))
                attrs.append(('rating', r.rating))
                attrs.append(('creation', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.created))))
                for k, v in attrs:
                    print(printStr % (k, v))

            if options.apm:
                if options.matches:
                    apm = (r.apmRecent)(maxMatches=options.matches, **criteria)
                else:
                    apm = (r.apmAggregate)(**criteria)
                print(printStr % ('apm', apm))
            if options.matches:
                newCriteria = dict(criteria)
                newCriteria['maxMatches'] = options.matches
                foundMatches = (r.recentMatches)(**newCriteria)
                print(printStr % ('recent matches', len(foundMatches)))
                for m in foundMatches:
                    print('            ', m)

        if options.summary:
            print('num players(s)%s: %d' % (' affected by action' if action else '', len(records)))