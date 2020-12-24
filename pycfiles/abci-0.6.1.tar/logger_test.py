# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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