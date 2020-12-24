# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/reloader.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1486 bytes
"""This module contains classes and functions to help
to reload plugins and configuration files on the fly.
"""
from .util.timer import Timer
from .util.log import getLogger

class Reloader(object):

    def __init__(self, elements, interval=20, log=None):
        """Create a new reloader manager.

        :type elements: list
        :param elements: a list with the object to reload. The objects must
            contain the ``reload`` method implemented.

        :type interval: int
        :param interval: the interval in seconds to reload elements.
            By default set to 20 seconds.

        :type log: :class:`Logger`
        :param log: if present used the provider logger to log,
            otherwise use default one provided by :meth:`getLogger`
        """
        self.elements = elements
        self.interval = interval
        self.log = log or getLogger()

    def reload(self):
        """Force a reload of the defined elements during reloader
        initialization.
        """
        for element in self.elements:
            fun = getattr(element, 'reload', None)
            if fun and hasattr(fun, '__call__'):
                self.log.debug('Reloading object: %s' % (
                 element.__class__.__name__,))
                fun()
                continue

    def start(self):
        """Start the reloader thread"""
        Timer(self.interval, self.reload).run()