# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../Pinyin2Hanzi/interface.py
# Compiled at: 2016-02-06 23:25:25


class AbstractHmmParams(object):

    def start(self, state):
        """ get start prob of state(hanzi) """
        pass

    def emission(self, state, observation):
        """ state (hanzi) -> observation (pinyin) """
        pass

    def transition(self, from_state, to_state):
        """ state -> state """
        pass

    def get_states(self, observation):
        """ get states which produce the given obs """
        pass


class AbstractDagParams(object):

    def get_phrase(self, pinyin_list, num):
        pass