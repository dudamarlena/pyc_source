# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/memberevent.py
# Compiled at: 2019-10-02 11:37:32
# Size of source mod 2**32: 558 bytes
from datetime import datetime

class MemberEvent:

    def __init__(self, config, event_dict):
        self.date = datetime.fromtimestamp(event_dict['date']).strftime('%x')
        self.timestamp = event_dict['date']
        self.event = event_dict['event']
        self.message = {'join':config['strings']['memberEventJoinedClan'], 
         'role change':config['strings']['memberEventRoleChange'].format(event_dict['role']), 
         'quit':config['strings']['memberEventExitClan']}[self.event]