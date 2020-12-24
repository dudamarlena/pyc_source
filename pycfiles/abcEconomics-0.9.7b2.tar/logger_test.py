# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/logger_test.py
# Compiled at: 2018-03-08 03:37:49
import abce, time

class LoggerTest(abce.Agent):

    def init(self, rounds):
        self.last_round = rounds - 1
        self.create('money', 50)
        self.create('cookies', 3)

    def one(self):
        self.log('possessions', self.possessions())
        self.log('round_log', self.round)

    def two(self):
        pass

    def three(self):
        pass

    def clean_up(self):
        pass

    def all_tests_completed(self):
        if self.round == self.last_round:
            time.sleep(0.5)
            print 'Check database whether logging succeeded'