# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/demerit.py
# Compiled at: 2019-10-17 14:46:54
# Size of source mod 2**32: 496 bytes


class Demerit:

    def __init__(self, tag, status, action=None, date=0, notes=''):
        self.tag = tag.strip()
        self.action = action
        self.status = status
        self.date = date
        self.notes = notes

    def __str__(self):
        return str(self.__dict__)

    def merge(self, other_demerit):
        self.notes = '{}<br>- {}'.format(other_demerit.notes, self.notes)
        if not self.notes.startswith('<br>- '):
            self.notes = '<br>- {}'.format(self.notes)