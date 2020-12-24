# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/vacation.py
# Compiled at: 2019-10-02 14:59:34
# Size of source mod 2**32: 171 bytes


class MemberVacation:

    def __init__(self, tag, start_date=0, end_date=0, notes=''):
        self.tag = tag
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes