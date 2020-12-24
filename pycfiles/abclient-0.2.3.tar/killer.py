# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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