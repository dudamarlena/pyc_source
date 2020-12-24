# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/logging_mixin.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 5197 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging, sys, warnings, six
from builtins import object
from contextlib import contextmanager
from logging import Handler, StreamHandler

class LoggingMixin(object):
    """LoggingMixin"""

    def __init__(self, context=None):
        self._set_context(context)

    @property
    def logger(self):
        warnings.warn('Initializing logger for {} using logger(), which will be replaced by .log in Airflow 2.0'.format(self.__class__.__module__ + '.' + self.__class__.__name__), DeprecationWarning)
        return self.log

    @property
    def log(self):
        try:
            return self._log
        except AttributeError:
            self._log = logging.root.getChild(self.__class__.__module__ + '.' + self.__class__.__name__)
            return self._log

    def _set_context(self, context):
        if context is not None:
            set_context(self.log, context)


class StreamLogWriter(object):
    encoding = False

    def __init__(self, logger, level):
        """
        :param log: The log level method to write to, ie. log.debug, log.warning
        :return:
        """
        self.logger = logger
        self.level = level
        self._buffer = str()

    def write(self, message):
        """
        Do whatever it takes to actually log the specified logging record
        :param message: message to log
        """
        if not message.endswith('\n'):
            self._buffer += message
        else:
            self._buffer += message
            self.logger.log(self.level, self._buffer.rstrip())
            self._buffer = str()

    def flush(self):
        """
        Ensure all logging output has been flushed
        """
        if len(self._buffer) > 0:
            self.logger.log(self.level, self._buffer)
            self._buffer = str()

    def isatty(self):
        """
        Returns False to indicate the fd is not connected to a tty(-like) device.
        For compatibility reasons.
        """
        return False


class RedirectStdHandler(StreamHandler):
    """RedirectStdHandler"""

    def __init__(self, stream):
        if not isinstance(stream, six.string_types):
            raise Exception("Cannot use file like objects. Use 'stdout' or 'stderr' as a str and without 'ext://'.")
        self._use_stderr = True
        if 'stdout' in stream:
            self._use_stderr = False
        Handler.__init__(self)

    @property
    def stream(self):
        if self._use_stderr:
            return sys.stderr
        else:
            return sys.stdout


@contextmanager
def redirect_stdout(logger, level):
    writer = StreamLogWriter(logger, level)
    try:
        sys.stdout = writer
        yield
    finally:
        sys.stdout = sys.__stdout__


@contextmanager
def redirect_stderr(logger, level):
    writer = StreamLogWriter(logger, level)
    try:
        sys.stderr = writer
        yield
    finally:
        sys.stderr = sys.__stderr__


def set_context(logger, value):
    """
    Walks the tree of loggers and tries to set the context for each handler
    :param logger: logger
    :param value: value to set
    """
    _logger = logger
    while _logger:
        for handler in _logger.handlers:
            try:
                handler.set_context(value)
            except AttributeError:
                pass

        if _logger.propagate is True:
            _logger = _logger.parent
        else:
            _logger = None