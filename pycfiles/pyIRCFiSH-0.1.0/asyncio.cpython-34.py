# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/io/asyncio.py
# Compiled at: 2015-10-08 05:15:52
# Size of source mod 2**32: 4993 bytes
__doc__ = 'Support for asyncio, available in Python 3.4 and later (and 3.3 via a\nbackport).\n'
try:
    import asyncio
except ImportError as e:
    from sys import version_info
    if version_info < (3, 3):
        raise ImportError('Must have Python 3.3 or greater to use this module') from e
    else:
        raise ImportError('Must install asyncio module from PyPI') from e

from collections import namedtuple
from functools import update_wrapper, partial
from logging import getLogger
from PyIRC.base import IRCBase, Event
from PyIRC.line import Line
_logger = getLogger(__name__)

class IRCProtocol(IRCBase, asyncio.Protocol):
    """IRCProtocol"""
    _ScheduleItem = namedtuple('_ScheduleItem', 'time callback sched')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sched_events = set()
        self.data = None
        if self.unload_extension('StartTLS'):
            _logger.critical('Removing StartTLS extension due to asyncio limitations')

    def connect(self):
        """Create a connection.

        :returns:
            An asyncio coroutine representing the connection.
        """
        loop = asyncio.get_event_loop()
        return loop.create_connection(lambda : self, self.server, self.port, ssl=self.ssl)

    def close(self):
        super().close(self)
        for sched in self.sched_events:
            self.unschedule(sched)

    def connection_made(self, transport):
        self.transport = transport
        self.data = ''
        super().connect()

    def data_received(self, data):
        data = self.data + data
        lines = data.split('\r\n')
        self.data = lines.pop()
        for line in lines:
            line = Line.parse(line.decode('utf-8', 'ignore'))
            _logger.debug('IN: %s', str(line).rstrip())
            try:
                super().recv(line)
            except Exception:
                _logger.exception('Exception received in recv loop')
                self.send('QUIT', ['Exception received!'])
                self.transport.close()
                loop = asyncio.get_event_loop()
                loop.stop()
                raise

    def connection_closed(self, exc):
        """Handle an abrupt disconnection."""
        _logger.info('Connection lost: %s', str(exc))
        super().close()

    def send(self, command, params):
        line = super().send(command, params)
        if line is None:
            return
        self.transport.write(bytes(line))
        _logger.debug('OUT: %s', str(line).rstrip())

    def call_event(self, hclass, event, *args, **kwargs):
        """Call an (hclass, event) signal.

        If no args are passed in, and the signal is in a deferred state, the
        arguments from the last call_event will be used.

        """
        signal = self.signals.get_signal((hclass, event))
        event = Event(signal.name, self)
        ret = signal.call(event, *args, **kwargs)
        return (
         event, ret)

    def schedule(self, time, callback):

        def cb_cleanup(time, callback):
            self.sched_events.discard((time, callback))
            return callback()

        callback_wrap = partial(cb_cleanup, time, callback)
        update_wrapper(callback_wrap, callback)
        loop = asyncio.get_event_loop()
        val = loop.call_later(time, callback_wrap)
        return self._ScheduleItem(time, callback, val)

    def unschedule(self, sched):
        self.sched_events.discard((sched.time, sched.callback))
        sched.sched.cancel()

    def wrap_ssl(self):
        raise NotImplementedError('Cannot wrap SSL after connect due to asyncio limitations (see https://bugs.python.org/issue23749)')