# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/algorithm/experience_replay/experience_replay.py
# Compiled at: 2016-10-27 05:00:52
import random

class ExperienceReplay(object):

    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []

    def store_transition(self, state, action, reward, next_state):
        if len(self.queue) >= self.max_size:
            self.queue.pop(0)
        self.queue.append((state, action, reward, next_state))

    def sample_minibatch(self, minibatch_size):
        return random.sample(self.queue, minibatch_size)

    def dump(self):
        return (
         self.max_size, self.queue)

    def load(self, serial):
        self.max_size, self.queue = serial