# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football/templatetags/football_tags.py
# Compiled at: 2012-11-15 06:10:12
import json
from django.core.cache import cache
from django import template
register = template.Library()

@register.inclusion_tag('football/inclusion_tags/live_scores.html')
def live_scores():
    """
    Displays live scores, if there are any - cache-based.

    Uses something like this:
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
    live_scores = cache.get('FOOTBALL_LIVE_SCORES')
    if live_scores:
        scores_array = []
        for score in json.loads(live_scores)[0:3]:
            if not score['LIVE']:
                scores_array.append(score)

        return {'live_scores': scores_array}
    else:
        return {}