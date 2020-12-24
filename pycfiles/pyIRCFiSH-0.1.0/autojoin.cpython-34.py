# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/autojoin.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 2833 bytes
__doc__ = 'Join channels on connection automatically.'
from collections.abc import Mapping
from functools import partial
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics

class AutoJoin(BaseExtension):
    """AutoJoin"""

    def __init__(self, *args, **kwargs):
        """Initialise the AutoJoin extension.

        :key join:
            A Mapping (dictionary type) or Iterable of channels to join.
            If a Mapping is passed, keys are treated as channel names and
            values are used as keys to join the channel.
            If an Iterable is passed, each value is a channel and no keys are
            specified when joining.

        :key autojoin_wait_start:
            How much time, in seconds, to wait for autojoin to begin.
            The default is 0.75 seconds.

        :key autojoin_wait_interval:
            How much time, in seconds, to wait between each join.
            The default is 0.25 seconds.

        """
        super().__init__(*args, **kwargs)
        self.join_dict = kwargs.get('join', {})
        if not isinstance(self.join_dict, Mapping):
            self.join_dict = {channel:None for channel in self.join_dict}
        self.wait_start = kwargs.get('autojoin_wait_start', 0.75)
        self.wait_interval = kwargs.get('autojoin_wait_interval', 0.25)
        self.sched = []

    def do_join(self, params):
        self.send('JOIN', params)
        self.sched.pop(0)

    @event('commands', Numerics.RPL_WELCOME)
    def autojoin(self, caller, line):
        t = self.wait_start
        for channel, key in self.join_dict.items():
            if key is None:
                params = [
                 channel]
            else:
                params = [
                 channel, key]
            sched = self.schedule(t, partial(self.do_join, params))
            self.sched.append(sched)
            t += self.wait_interval

    @event('link', 'disconnected')
    def close(self, caller):
        for sched in self.sched:
            try:
                self.unschedule(sched)
            except ValueError:
                pass

        self.sched.clear()