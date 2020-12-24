# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/namanbharadwaj/en/lib/python2.6/site-packages/bobb/internal.py
# Compiled at: 2013-08-06 13:27:48
_target_builder_map = {}
_action_map = {}

def has_builder(tgt):
    return tgt in _target_builder_map


def register_builder(tgt, builder):
    _target_builder_map[tgt] = builder


def get_builder(tgt):
    return _target_builder_map[tgt]


def get_targets():
    return _target_builder_map.keys()


def has_action(name):
    return name in _action_map


def register_action(action):
    _action_map[action.__name__] = action


def get_action(name):
    return _action_map[name]