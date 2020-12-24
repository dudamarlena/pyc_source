# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/victim.py
# Compiled at: 2018-05-03 06:13:03
import abce

class Victim(abce.Agent, abce.Household):

    def init(self):
        self.count = 1

    def am_I_dead(self):
        if self.id < self.round:
            raise Exception('should be dead %i' % self.id)