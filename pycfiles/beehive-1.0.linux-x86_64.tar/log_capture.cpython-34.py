# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/log_capture.py
# Compiled at: 2014-11-03 05:47:13
# Size of source mod 2**32: 7428 bytes
import logging, functools
from logging.handlers import BufferingHandler
import re

class RecordFilter(object):
    __doc__ = 'Implement logging record filtering as per the configuration\n    --logging-filter option.\n    '

    def __init__(self, names):
        self.include = set()
        self.exclude = set()
        for name in names.split(','):
            if name[0] == '-':
                self.exclude.add(name[1:])
            else:
                self.include.add(name)

    def filter(self, record):
        if self.exclude:
            return record.name not in self.exclude
        return record.name in self.include


class LoggingCapture(BufferingHandler):
    __doc__ = "Capture logging events in a memory buffer for later display or query.\n\n    Captured logging events are stored on the attribute\n    :attr:`~LoggingCapture.buffer`:\n\n    .. attribute:: buffer\n\n       This is a list of captured logging events as `logging.LogRecords`_.\n\n    .. _`logging.LogRecords`:\n       http://docs.python.org/library/logging.html#logrecord-objects\n\n    By default the format of the messages will be::\n\n        '%(levelname)s:%(name)s:%(message)s'\n\n    This may be overridden using standard logging formatter names in the\n    configuration variable ``logging_format``.\n\n    The level of logging captured is set to ``logging.NOTSET`` by default. You\n    may override this using the configuration setting ``logging_level`` (which\n    is set to a level name.)\n\n    Finally there may be `filtering of logging events`__ specified by the\n    configuration variable ``logging_filter``.\n\n    .. __: beehive.html#command-line-arguments\n\n    "

    def __init__(self, config, level=None):
        BufferingHandler.__init__(self, 1000)
        self.config = config
        self.old_handlers = []
        self.old_level = None
        fmt = datefmt = None
        if config.logging_format:
            fmt = config.logging_format
        else:
            fmt = '%(levelname)s:%(name)s:%(message)s'
        if config.logging_datefmt:
            datefmt = config.logging_datefmt
        fmt = logging.Formatter(fmt, datefmt)
        self.setFormatter(fmt)
        if level is not None:
            self.level = level
        else:
            if config.logging_level:
                self.level = config.logging_level
            else:
                self.level = logging.NOTSET
        if config.logging_filter:
            self.addFilter(RecordFilter(config.logging_filter))

    def __nonzero__(self):
        return bool(self.buffer)

    def flush(self):
        pass

    def truncate(self):
        self.buffer = []

    def getvalue(self):
        return '\n'.join(self.formatter.format(r) for r in self.buffer)

    def findEvent(self, pattern):
        """Search through the buffer for a message that matches the given
        regular expression.

        Returns boolean indicating whether a match was found.
        """
        pattern = re.compile(pattern)
        for record in self.buffer:
            if pattern.search(record.getMessage()) is not None:
                return True

        return False

    def any_errors(self):
        """Search through the buffer for any ERROR or CRITICAL events.

        Returns boolean indicating whether a match was found.
        """
        return any(record for record in self.buffer if record.levelname in ('ERROR',
                                                                            'CRITICAL'))

    def inveigle(self):
        """Turn on logging capture by replacing all existing handlers
        configured in the logging module.

        If the config var logging_clear_handlers is set then we also remove
        all existing handlers.

        We also set the level of the root logger.

        The opposite of this is :meth:`~LoggingCapture.abandon`.
        """
        root_logger = logging.getLogger()
        if self.config.logging_clear_handlers:
            for logger in logging.Logger.manager.loggerDict.values():
                if hasattr(logger, 'handlers'):
                    for handler in logger.handlers:
                        self.old_handlers.append((logger, handler))
                        logger.removeHandler(handler)

                    continue

        for handler in root_logger.handlers[:]:
            if isinstance(handler, LoggingCapture):
                root_logger.handlers.remove(handler)
            elif self.config.logging_clear_handlers:
                self.old_handlers.append((root_logger, handler))
                root_logger.removeHandler(handler)
                continue

        root_logger.addHandler(self)
        self.old_level = root_logger.level
        root_logger.setLevel(self.level)

    def abandon(self):
        """Turn off logging capture.

        If other handlers were removed by :meth:`~LoggingCapture.inveigle` then
        they are reinstated.
        """
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if handler is self:
                root_logger.handlers.remove(handler)
                continue

        if self.config.logging_clear_handlers:
            for logger, handler in self.old_handlers:
                logger.addHandler(handler)

        if self.old_level is not None:
            root_logger.setLevel(self.old_level)
            self.old_level = None


MemoryHandler = LoggingCapture

def capture(*args, **kw):
    """Decorator to wrap an *environment file function* in log file capture.

    It configures the logging capture using the *beehive* context - the first
    argument to the function being decorated (so don't use this to decorate
    something that doesn't have *context* as the first argument.)

    The basic usage is:

    .. code-block: python

        @capture
        def after_scenario(context, scenario):
            ...

    The function prints any captured logging (at the level determined by the
    ``log_level`` configuration setting) directly to stdout, regardless of
    error conditions.

    It is mostly useful for debugging in situations where you are seeing a
    message like::

        No handlers could be found for logger "name"

    The decorator takes an optional "level" keyword argument which limits the
    level of logging captured, overriding the level in the run's configuration:

    .. code-block: python

        @capture(level=logging.ERROR)
        def after_scenario(context, scenario):
            ...

    This would limit the logging captured to just ERROR and above, and thus
    only display logged events if they are interesting.
    """

    def create_decorator(func, level=None):

        def f(context, *args):
            h = LoggingCapture(context.config, level=level)
            h.inveigle()
            try:
                func(context, *args)
            finally:
                h.abandon()

            v = h.getvalue()
            if v:
                print('Captured Logging:')
                print(v)

        return f

    if not args:
        return functools.partial(create_decorator, level=kw.get('level'))
    else:
        return create_decorator(args[0])