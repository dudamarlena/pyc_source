# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/membercustomrecord.py
# Compiled at: 2019-10-16 14:39:11
# Size of source mod 2**32: 125 bytes


class MemberCustomRecord:

    def __init__(self, tag, role, notes=''):
        self.tag = tag
        self.role = role
        self.notes = notes