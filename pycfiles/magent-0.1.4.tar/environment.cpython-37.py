# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mariojayakumar/Documents/School/2019_2020/Sem2/MAgent/python/magent/environment.py
# Compiled at: 2020-04-02 21:26:17
# Size of source mod 2**32: 702 bytes
""" base class for environment """

class Environment:
    __doc__ = 'see subclass for detailed comment'

    def __init__(self):
        pass

    def reset(self):
        pass

    def get_observation(self, handle):
        pass

    def set_action(self, handle, actions):
        pass

    def step(self):
        pass

    def render(self):
        pass

    def render_next_file(self):
        pass

    def get_reward(self, handle):
        pass

    def get_num(self, handle):
        pass

    def get_action_space(self, handle):
        pass

    def get_view_space(self, handle):
        pass

    def get_feature_space(self, handle):
        pass