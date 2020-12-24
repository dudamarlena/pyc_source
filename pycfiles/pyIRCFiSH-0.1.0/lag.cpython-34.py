# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/lag.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 2936 bytes
__doc__ = 'Latency measurements to the server.'
try:
    from time import monotonic as time
except ImportError:
    from time import time

from PyIRC.signal import event
from random import randint, choice
from string import ascii_letters as letters, digits
from logging import getLogger
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)

class LagCheck(BaseExtension):
    """LagCheck"""

    def __init__(self, *args, **kwargs):
        """Initialise the LagCheck extension.

        :key lagcheck:
            Time interval to do periodic lag checks to update the lag timer.
            Defaults to 15 seconds. Setting the value too low may result in
            being disconnected by the server.

        """
        super().__init__(*args, **kwargs)
        self.lagcheck = kwargs.get('lagcheck', 15)
        self.lag = None
        self.last = None
        self.timer = None

    @staticmethod
    def timestr(time):
        """Return a random string based on the current time."""
        length = randint(5, 10)
        chars = letters + digits
        randstr = ''.join(choice(chars) for x in range(length))
        return '{}-{}'.format(time, randstr)

    def ping(self):
        """Callback for ping."""
        if self.last is not None:
            raise OSError('Connection timed out')
        self.last = time()
        s = self.timestr(self.last)
        self.send('PING', [s])
        self.timer = self.schedule(self.lagcheck, self.ping)

    @event('link', 'disconnected')
    def close(self, _):
        """Reset state since we are disconnected."""
        self.last = None
        self.lag = None
        if self.timer is not None:
            try:
                self.unschedule(self.timer)
            except ValueError:
                pass

    @event('commands', Numerics.RPL_WELCOME)
    def start(self, _, line):
        """Begin sending PING requests as soon as possible."""
        self.ping()

    @event('commands', 'PONG')
    def pong(self, _, line):
        """Use PONG reply to check lag."""
        if self.last is None:
            return
        t, sep, s = line.params[(-1)].partition('-')
        if not sep or not s:
            return
        if t != str(self.last):
            return
        self.lag = round(time() - float(self.last), 3)
        self.last = None
        _logger.info('Lag: %f', self.lag)