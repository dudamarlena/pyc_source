# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/util/daemon/posix.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1995 bytes
"""Generic linux daemon base class for python 3.x.

.. note::
    Most of this module is heavly based on the `work of Lone Wolves`_

.. _`work of Lone Wolves`: http://www.jejik.com/files/examples/daemon3x.py

"""
import sys, os, signal
from . import Daemon

class PosixDaemon(Daemon):

    def __init__(self, handler, exit_handler=None):
        """Implement a daemon for posix systems using generic posix
        daemon class.

        :type handler: callable
        :param handler: The handler to call to daemonize the process.

        :type exit_handler: callable
        :param exit_handler: The handler to call when exit the process if
            any.
        """
        self.handler = handler
        self.pid = 0
        if exit_handler:
            self.set_exit_handler(exit_handler)
        Daemon.__init__(self)

    def set_exit_handler(self, func):
        """Dynamically sets the exit_handler to specified function passed as
        argument.
        """
        signal.signal(signal.SIGTERM, func)

    def foreground(self):
        """Run the handler in foreground"""
        self.handler()

    def start(self):
        """Start the daemon

        :rtype: int
        :return: The PID of the child process which is running the handler.
        """
        self.pid = os.fork()
        if self.pid:
            return self.pid
        sys.stdin = open(os.devnull, 'r')
        sys.stdout = open(os.devnull, 'a+')
        sys.stderr = open(os.devnull, 'a+')
        self.handler()

    def stop(self):
        """Stop the daemon"""
        if self.pid:
            os.kill(self.pid, 2)
            self.pid = 0

    def restart(self):
        """Restart the daemon

        :rtype: int
        :return: The PID of the child process which is running the handler.
        """
        self.stop()
        return self.start()