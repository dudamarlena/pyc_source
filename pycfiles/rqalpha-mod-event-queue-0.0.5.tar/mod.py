# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cuiziqi/Documents/workspace/rqalpha-mod-event-queue/rqalpha_mod_event_queue/mod.py
# Compiled at: 2017-09-24 03:47:59
from rqalpha.interface import AbstractMod
from rqalpha.const import RUN_TYPE
from .queued_event_bus import QueuedEventBus

class EventQueueMod(AbstractMod):

    def __init__(self):
        self._env = None
        self._mod_config = None
        return

    def start_up(self, env, mod_config):
        self._env = env
        self._mod_config = mod_config
        if self._env.config.base.run_type == RUN_TYPE.BACKTEST:
            return
        self._env.event_bus = QueuedEventBus(self._env.event_bus)
        self._env.event_bus.start()

    def tear_down(self, code, exception=None):
        if self._env.config.base.run_type == RUN_TYPE.BACKTEST:
            return
        if isinstance(self._env.event_bus, QueuedEventBus):
            self._env.event_bus.stop()