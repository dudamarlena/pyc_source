# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/membercustomrecord.py
# Compiled at: 2019-10-16 14:39:11
# Size of source mod 2**32: 125 bytes


class MemberCustomRecord:

    def __init__(self, tag, role, notes=''):
        self.tag = tag
        self.role = role
        self.notes = notes