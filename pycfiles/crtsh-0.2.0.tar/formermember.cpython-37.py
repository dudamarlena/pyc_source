# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/formermember.py
# Compiled at: 2019-10-21 09:53:46
# Size of source mod 2**32: 1175 bytes
from pyroyale import Clan
from crtools.models import Demerit

class FormerMember:

    def __init__(self, config, historical_member, player_tag, processed_events):
        self.name = historical_member['name']
        self.tag = player_tag
        self.blacklist = False
        self.events = processed_events
        self.timestamp = self.events[(-1)].timestamp
        self.reason = 'Quit'
        self.notes = ''
        if player_tag in config['members']['warned']:
            demerit = config['members']['warned'][player_tag]
            if type(demerit) is Demerit:
                self.reason = 'Warned'
                self.notes = demerit.notes
        if player_tag in config['members']['kicked']:
            demerit = config['members']['kicked'][player_tag]
            if type(demerit) is Demerit:
                self.reason = 'Kicked'
                self.notes = demerit.notes
        if player_tag in config['members']['blacklist']:
            self.blacklist = True
            demerit = config['members']['blacklist'][player_tag]
            if type(demerit) is Demerit:
                self.reason = 'Blacklisted'
                self.notes = demerit.notes