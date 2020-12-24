# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/vacation.py
# Compiled at: 2019-10-02 14:59:34
# Size of source mod 2**32: 171 bytes


class MemberVacation:

    def __init__(self, tag, start_date=0, end_date=0, notes=''):
        self.tag = tag
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes