# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/runtime.py
# Compiled at: 2013-12-04 06:19:08
"""runtime"""
from state import State
state = State()

def init(args=[], opts=None):
    global state
    state.args = args
    state.opts = opts
    state.bootstrap()
    state.initialize()


def types(name):
    return state.root['Types'][name]


def core(name):
    return state.root['Core'][name]


def find(name):
    return state.find(name)