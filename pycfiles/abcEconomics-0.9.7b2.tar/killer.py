# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/killer.py
# Compiled at: 2018-05-03 06:13:03
import abce

class Killer(abce.Agent, abce.Household):

    def init(self):
        pass

    def kill_silent(self):
        return (
         'victim', self.round)

    def kill_loud(self):
        return (
         'loudvictim', self.round)