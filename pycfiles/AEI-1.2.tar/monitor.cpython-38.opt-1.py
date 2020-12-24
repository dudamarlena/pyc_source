# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aehostd/monitor.py
# Compiled at: 2020-04-11 17:07:07
# Size of source mod 2**32: 2304 bytes
__doc__ = '\naehostd.monitor - write monitor data\n'
import time, logging, json, threading

class Monitor(threading.Thread):
    """Monitor"""

    def __init__(self, monitor_interval, server, user_refresh, netaddr_refresh):
        threading.Thread.__init__(self,
          group=None,
          target=None,
          name=None,
          args=(),
          kwargs={})
        self.enabled = True
        self._next_run = 0.0
        self._server = server
        self._user_refresh = user_refresh
        self._netaddr_refresh = netaddr_refresh
        self._schedule_interval = 0.2
        self._monitor_interval = monitor_interval

    def _log(self, log_level, msg, *args, **kwargs):
        """
        log one line prefixed with class name
        """
        msg = ' '.join((self.__class__.__name__, msg))
        (logging.log)(log_level, msg, *args, **kwargs)

    def run(self):
        """
        do the work
        """
        self._log(logging.DEBUG, 'Starting %s.run() with interval %0.1f secs', self.__class__.__name__, self._monitor_interval)
        while self.enabled:
            current_time = time.time()
            if current_time >= self._next_run:
                self._log(logging.INFO, '%s %s', self._server.__class__.__name__, json.dumps(self._server.get_monitor_data()))
                self._log(logging.INFO, '%s %s', self._user_refresh.__class__.__name__, json.dumps(self._user_refresh.get_monitor_data()))
                if self._netaddr_refresh is not None:
                    self._log(logging.INFO, '%s %s', self._netaddr_refresh.__class__.__name__, json.dumps(self._netaddr_refresh.get_monitor_data()))
                self._next_run = current_time + self._monitor_interval
            time.sleep(self._schedule_interval)

        self._log(logging.DEBUG, 'Exiting %s.run()', self.__class__.__name__)