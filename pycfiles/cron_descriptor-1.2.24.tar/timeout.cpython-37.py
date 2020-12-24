# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/util/timeout.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 9874 bytes
from __future__ import absolute_import
from socket import _GLOBAL_DEFAULT_TIMEOUT
import time
from ..exceptions import TimeoutStateError
_Default = object()
current_time = getattr(time, 'monotonic', time.time)

class Timeout(object):
    """Timeout"""
    DEFAULT_TIMEOUT = _GLOBAL_DEFAULT_TIMEOUT

    def __init__(self, total=None, connect=_Default, read=_Default):
        self._connect = self._validate_timeout(connect, 'connect')
        self._read = self._validate_timeout(read, 'read')
        self.total = self._validate_timeout(total, 'total')
        self._start_connect = None

    def __str__(self):
        return '%s(connect=%r, read=%r, total=%r)' % (
         type(self).__name__,
         self._connect,
         self._read,
         self.total)

    @classmethod
    def _validate_timeout(cls, value, name):
        """ Check that a timeout attribute is valid.

        :param value: The timeout value to validate
        :param name: The name of the timeout attribute to validate. This is
            used to specify in error messages.
        :return: The validated and casted version of the given value.
        :raises ValueError: If it is a numeric value less than or equal to
            zero, or the type is not an integer, float, or None.
        """
        if value is _Default:
            return cls.DEFAULT_TIMEOUT
            if value is None or value is cls.DEFAULT_TIMEOUT:
                return value
            if isinstance(value, bool):
                raise ValueError('Timeout cannot be a boolean value. It must be an int, float or None.')
        else:
            try:
                float(value)
            except (TypeError, ValueError):
                raise ValueError('Timeout value %s was %s, but it must be an int, float or None.' % (
                 name, value))

            try:
                if value <= 0:
                    raise ValueError('Attempted to set %s timeout to %s, but the timeout cannot be set to a value less than or equal to 0.' % (
                     name, value))
            except TypeError:
                raise ValueError('Timeout value %s was %s, but it must be an int, float or None.' % (
                 name, value))

        return value

    @classmethod
    def from_float(cls, timeout):
        """ Create a new Timeout from a legacy timeout value.

        The timeout value used by httplib.py sets the same timeout on the
        connect(), and recv() socket requests. This creates a :class:`Timeout`
        object that sets the individual timeouts to the ``timeout`` value
        passed to this function.

        :param timeout: The legacy timeout value.
        :type timeout: integer, float, sentinel default object, or None
        :return: Timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(read=timeout, connect=timeout)

    def clone(self):
        """ Create a copy of the timeout object

        Timeout properties are stored per-pool but each request needs a fresh
        Timeout object to ensure each one has its own start/stop configured.

        :return: a copy of the timeout object
        :rtype: :class:`Timeout`
        """
        return Timeout(connect=(self._connect), read=(self._read), total=(self.total))

    def start_connect(self):
        """ Start the timeout clock, used during a connect() attempt

        :raises urllib3.exceptions.TimeoutStateError: if you attempt
            to start a timer that has been started already.
        """
        if self._start_connect is not None:
            raise TimeoutStateError('Timeout timer has already been started.')
        self._start_connect = current_time()
        return self._start_connect

    def get_connect_duration(self):
        """ Gets the time elapsed since the call to :meth:`start_connect`.

        :return: Elapsed time in seconds.
        :rtype: float
        :raises urllib3.exceptions.TimeoutStateError: if you attempt
            to get duration for a timer that hasn't been started.
        """
        if self._start_connect is None:
            raise TimeoutStateError("Can't get connect duration for timer that has not started.")
        return current_time() - self._start_connect

    @property
    def connect_timeout(self):
        """ Get the value to use when setting a connection timeout.

        This will be a positive float or integer, the value None
        (never timeout), or the default system timeout.

        :return: Connect timeout.
        :rtype: int, float, :attr:`Timeout.DEFAULT_TIMEOUT` or None
        """
        if self.total is None:
            return self._connect
        if self._connect is None or self._connect is self.DEFAULT_TIMEOUT:
            return self.total
        return min(self._connect, self.total)

    @property
    def read_timeout(self):
        """ Get the value for the read timeout.

        This assumes some time has elapsed in the connection timeout and
        computes the read timeout appropriately.

        If self.total is set, the read timeout is dependent on the amount of
        time taken by the connect timeout. If the connection time has not been
        established, a :exc:`~urllib3.exceptions.TimeoutStateError` will be
        raised.

        :return: Value to use for the read timeout.
        :rtype: int, float, :attr:`Timeout.DEFAULT_TIMEOUT` or None
        :raises urllib3.exceptions.TimeoutStateError: If :meth:`start_connect`
            has not yet been called on this object.
        """
        if self.total is not None:
            if self.total is not self.DEFAULT_TIMEOUT:
                if self._read is not None:
                    if self._read is not self.DEFAULT_TIMEOUT:
                        if self._start_connect is None:
                            return self._read
                        return max(0, min(self.total - self.get_connect_duration(), self._read))
        if self.total is not None:
            if self.total is not self.DEFAULT_TIMEOUT:
                return max(0, self.total - self.get_connect_duration())
        return self._read