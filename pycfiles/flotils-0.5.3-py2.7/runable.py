# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flotils\runable.py
# Compiled at: 2019-04-14 10:12:08
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'the01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-19, Florian JUNG'
__license__ = b'All rights reserved'
__version__ = b'0.1.3'
__date__ = b'2019-03-21'
from abc import ABCMeta, abstractmethod
import time, signal
from .logable import Logable

class StartException(Exception):
    pass


class Startable(object):
    """
    Abstract interface to add a start method
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Startable, self).__init__()
        return

    @abstractmethod
    def start(self):
        """
        Start the interface

        :rtype: None
        """
        pass


class Stopable(object):
    """
    Abstract interface to add a stop method
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(Stopable, self).__init__()
        return

    @abstractmethod
    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        pass


class StartStopable(Startable, Stopable):
    """
    Abstract interface to add a start/stop method (e.g. for threading)
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(StartStopable, self).__init__(settings)
        self._is_running = False
        self._start_block_timeout = settings.get(b'start_blocking_timeout', 1.0)
        return

    @property
    def is_running(self):
        """
        Is this class currently running

        :return: Running state
        :rtype: bool
        """
        return self._is_running

    def start(self, blocking=False):
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :type blocking: bool
        :rtype: None
        """
        super(StartStopable, self).start()
        self._is_running = True
        try:
            while blocking and self._is_running:
                time.sleep(self._start_block_timeout)

        except IOError as e:
            if not str(e).lower().startswith(b'[errno 4]'):
                raise

    def stop(self):
        """
        Stop the interface

        :rtype: None
        """
        self._is_running = False
        super(StartStopable, self).stop()


class SignalStopWrapper(Logable, Stopable):
    """
    Catch SIGINT and SIGTERM to smoothly stop running
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(SignalStopWrapper, self).__init__(settings)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        self.info(b'Catching SIGINT and SIGTERM')
        return

    def _signal_handler(self, sig, frame):
        self.warning((b'Signal {} caught').format(sig))
        self.stop()