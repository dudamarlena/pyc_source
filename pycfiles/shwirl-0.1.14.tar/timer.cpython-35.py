# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/app/timer.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 5780 bytes
from __future__ import division
from ..util.event import Event, EmitterGroup
from ..util.ptime import time as precision_time
from ..ext.six import string_types
from .base import BaseTimerBackend as TimerBackend
from . import use_app, Application

class Timer(object):
    __doc__ = "Timer used to schedule events in the future or on a repeating schedule\n\n    Parameters\n    ----------\n    interval : float | 'auto'\n        Time between events in seconds. The default is 'auto', which\n        attempts to find the interval that matches the refresh rate of\n        the current monitor. Currently this is simply 1/60.\n    connect : function | None\n        The function to call.\n    iterations : int\n        Number of iterations. Can be -1 for infinite.\n    start : bool\n        Whether to start the timer.\n    app : instance of vispy.app.Application\n        The application to attach the timer to.\n    "

    def __init__(self, interval='auto', connect=None, iterations=-1, start=False, app=None):
        self.events = EmitterGroup(source=self, start=Event, stop=Event, timeout=Event)
        if app is None:
            self._app = use_app(call_reuse=False)
        else:
            if isinstance(app, Application):
                self._app = app
            else:
                if isinstance(app, string_types):
                    self._app = Application(app)
                else:
                    raise ValueError('Invalid value for app %r' % app)
        self._app.native
        self._backend = self._app.backend_module.TimerBackend(self)
        if interval == 'auto':
            interval = 0.016666666666666666
        self._interval = float(interval)
        self._running = False
        self._first_emit_time = None
        self._last_emit_time = None
        self.iter_count = 0
        self.max_iterations = iterations
        if connect is not None:
            self.connect(connect)
        if start:
            self.start()

    @property
    def app(self):
        """ The vispy Application instance on which this Timer is based.
        """
        return self._app

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, val):
        self._interval = val
        if self.running:
            self.stop()
            self.start()

    @property
    def elapsed(self):
        return precision_time() - self._first_emit_time

    @property
    def running(self):
        return self._running

    def start(self, interval=None, iterations=None):
        """Start the timer.

        A timeout event will be generated every *interval* seconds.
        If *interval* is None, then self.interval will be used.

        If *iterations* is specified, the timer will stop after
        emitting that number of events. If unspecified, then
        the previous value of self.iterations will be used. If the value is
        negative, then the timer will continue running until stop() is called.

        If the timer is already running when this function is called, nothing
        happens (timer continues running as it did previously, without
        changing the interval, number of iterations, or emitting a timer
        start event).
        """
        if self.running:
            return
        self.iter_count = 0
        if interval is not None:
            self.interval = interval
        if iterations is not None:
            self.max_iterations = iterations
        self._backend._vispy_start(self.interval)
        self._running = True
        self._first_emit_time = precision_time()
        self._last_emit_time = precision_time()
        self.events.start(type='timer_start')

    def stop(self):
        """Stop the timer."""
        self._backend._vispy_stop()
        self._running = False
        self.events.stop(type='timer_stop')

    @property
    def native(self):
        """ The native timer on which this Timer is based.
        """
        return self._backend._vispy_get_native_timer()

    def _timeout(self, *args):
        if not self.running:
            return
        if self.max_iterations >= 0 and self.iter_count >= self.max_iterations:
            self.stop()
            return
        now = precision_time()
        dt = now - self._last_emit_time
        elapsed = now - self._first_emit_time
        self._last_emit_time = now
        self.events.timeout(type='timer_timeout', iteration=self.iter_count, elapsed=elapsed, dt=dt, count=self.iter_count)
        self.iter_count += 1

    def connect(self, callback):
        """ Alias for self.events.timeout.connect() """
        return self.events.timeout.connect(callback)

    def disconnect(self, callback=None):
        """ Alias for self.events.timeout.disconnect() """
        return self.events.timeout.disconnect(callback)