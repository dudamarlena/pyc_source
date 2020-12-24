# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/algorithm/experience_replay/experience_replay_test.py
# Compiled at: 2016-10-27 05:00:52
from tests.base_unittest import BaseUnitTest
from kyoka.algorithm.experience_replay.experience_replay import ExperienceReplay
from mock import patch

class ExperienceReplayTest(BaseUnitTest):

    def test_queue_size_upper_bound(self):
        er = ExperienceReplay(max_size=2)
        experiences = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 0, 1)]
        for e in experiences:
            er.store_transition(state=e[0], action=e[1], reward=e[2], next_state=e[3])

        self.neq(er.queue[0], experiences[0])
        self.eq(er.queue[0], experiences[1])
        self.eq(er.queue[1], experiences[2])

    def test_sample_minibatch(self):
        er = ExperienceReplay(max_size=3)
        experiences = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 0, 1)]
        for e in experiences:
            er.store_transition(state=e[0], action=e[1], reward=e[2], next_state=e[3])

        self.eq(1, len(er.sample_minibatch(minibatch_size=1)))
        with patch('random.sample', side_effect=lambda lst, num: lst[len(lst) - num:]):
            minibatch = er.sample_minibatch(minibatch_size=2)
            expected = experiences[1:]
            self.eq(expected, minibatch)

    def test_dump_load(self):
        er = ExperienceReplay(max_size=2)
        experiences = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 0, 1)]
        for e in experiences:
            er.store_transition(state=e[0], action=e[1], reward=e[2], next_state=e[3])

        dump = er.dump()
        new_er = ExperienceReplay(max_size=3)
        new_er.load(dump)
        self.eq(er.max_size, new_er.max_size)
        self.eq(er.queue, new_er.queue)