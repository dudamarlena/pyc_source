# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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