# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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