# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/activity.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 991 bytes
from .constant import ACTIVITY_MAP

class Activity(object):

    def __init__(self, data, player_map, get_team_data):
        self.actions = []
        self.date = data['date']
        for msg in data['messages']:
            team = ''
            action = 'UNKNOWN'
            player = ''
            msg_id = msg['messageTypeId']
            if msg_id == 244:
                team = get_team_data(msg['from'])
            else:
                if msg_id == 239:
                    team = get_team_data(msg['for'])
                else:
                    team = get_team_data(msg['to'])
            if msg_id in ACTIVITY_MAP:
                action = ACTIVITY_MAP[msg_id]
            if msg['targetId'] in player_map:
                player = player_map[msg['targetId']]
            self.actions.append((team, action, player))

    def __repr__(self):
        return 'Activity(' + ' '.join(('(%s,%s,%s)' % tup for tup in self.actions)) + ')'