# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football/management/commands/football_live_scores.py
# Compiled at: 2012-11-15 06:10:12
import json, datetime
from django.core.cache import cache
from football365.management.commands.football365_fetch import Command as BaseCommand

class Command(BaseCommand):
    pipeline = {'live': ('live_raw', 'xml2dom', 'live_structure', 'live_commit')}

    def live_commit(self, call, data):
        """
        Produces something like this:
            [{"AWAYTEAMSCORE": 0, 
              "HOMETEAMSCORE": 0, 
              "HOMETEAMCODE": null, 
              "MATCHSTATUS": "22:00 CAT", 
              "AWAYTEAMCODE": null, 
              "AWAYTEAM": "Sunderland", 
              "LIVE": false, 
              "AWAYTEAMCARDS": [], 
              "HOMETEAMGOALS": [], 
              "DATE": "20/03/12 20:00", 
              "HOMETEAMCARDS": [], 
              "AWAYTEAMGOALS": [], 
              "HOMETEAM": "Blackburn Rovers"
              },
              {"AWAYTEAMSCORE": 0, 
              "HOMETEAMSCORE": 0, 
              "HOMETEAMCODE": null, 
              "MATCHSTATUS": "22:00 CAT", 
              "AWAYTEAMCODE": null, 
              "AWAYTEAM": "Sunderland", 
              "LIVE": false, 
              "AWAYTEAMCARDS": [], 
              "HOMETEAMGOALS": [], 
              "DATE": "20/03/12 20:00", 
              "HOMETEAMCARDS": [], 
              "AWAYTEAMGOALS": [], 
              "HOMETEAM": "Blackburn Rovers"
              }]
        """
        for game in data:
            game['DATE'] = game['DATE'].strftime('%d/%m/%y %H:%M')

        if data:
            cache.set('FOOTBALL_LIVE_SCORES', json.dumps(data))
            print 'Got data:'
            print cache.get('FOOTBALL_LIVE_SCORES')
        else:
            print 'No live scores.'
            if cache.get('FOOTBALL_LIVE_SCORES'):
                cache.delete('FOOTBALL_LIVE_SCORES')