# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/env.py
# Compiled at: 2020-04-13 03:23:35
# Size of source mod 2**32: 1844 bytes
from .event import Events

class Environment:
    events = None
    runner = None
    web_ui = None
    options = None
    host = None
    reset_stats = False
    step_load = False
    stop_timeout = None
    master_host = '127.0.0.1'
    master_port = 5557
    master_bind_host = '*'
    master_bind_port = 5557

    def __init__(self, events=None, options=None, host=None, reset_stats=False, step_load=False, stop_timeout=None):
        if events:
            self.events = events
        else:
            self.events = Events()
        self.options = options
        self.host = host
        self.reset_stats = reset_stats
        self.step_load = step_load
        self.stop_timeout = stop_timeout