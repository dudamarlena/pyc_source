# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/logcontext.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 3384 bytes
"""Treadmill log context helper classes."""
import logging, threading
LOCAL_ = threading.local()
LOCAL_.ctx = []

class Adapter(logging.LoggerAdapter):
    __doc__ = "\n    Prepends the log messages with the str representation of the thread local\n    list's last element if there's any.\n\n    This adapter makes possible to\n    * insert additional information into the log records w/o having to alter\n      the log formatter's definition inited by the etc/logging/*.yml files\n    * use logging (_LOGGER) in the same way as before apart from the\n      initialization of _LOGGER in a given modul\n    "

    def __init__(self, logger, extra=None):
        """
        Allow initializing w/o any 'extra' value.
        """
        super(Adapter, self).__init__(logger, extra)
        if self.extra:
            self.extra = [
             self.extra]
        else:
            self.extra = LOCAL_.ctx

    def warn(self, msg, *args, **kwargs):
        """
        Delegate warn() to warning().

        This is provided as a convenience method in Logger but it is apparently
        missing from LoggerAdapter, see

        https://hg.python.org/cpython/file/2.7/Lib/logging/__init__.py#l1181
        """
        self.warning(msg, *args, **kwargs)

    def process(self, msg, kwargs):
        """
        Add extra content to the log line but don't modify it if no element
        is contained by the thread local variable.
        """
        if not self.extra:
            return (msg, kwargs)
        return ('%s - %s' % (self._fmt(self.extra[(-1)]), msg), kwargs)

    def _fmt(self, extra):
        """Format the 'extra' content as it will be represented in the logs."""
        return extra


class ContainerAdapter(Adapter):
    __doc__ = '\n    Adapter to insert application unique name into the log record.\n    '

    def _fmt(self, extra):
        """Format the 'extra' content as it will be represented in the logs."""
        app_name, inst_id, uniq_id = self._dec_unique_name(extra)
        return '{name}#{inst} {uniq}'.format(name=app_name, inst=inst_id, uniq=uniq_id)

    def _dec_unique_name(self, unique_name):
        """
        Decompose unique app name into a list containing the app name,
        instance id and unique id. Return dummy entries if not an app unique
        name is passed in params.
        """
        parts = unique_name.rsplit('-', 2)
        if len(parts) != 3:
            return ['_'] * 3
        return parts


class LogContext(object):
    __doc__ = "\n    Context manager wrapping a logger adapter instance.\n\n    Ensures that a log record is processed always by the log adapter and the\n    corresponding internal sttate without having to worry about restoring the\n    logger's state to its original in case of an exception etc.\n    "

    def __init__(self, logger, extra, adapter_cls=Adapter):
        self.extra = extra
        self.logger = logger
        self.adapter_cls = adapter_cls

    def __enter__(self):
        """
        Save the original internal state of the logger adapter and
        replace it with the one got when instantiated.
        """
        LOCAL_.ctx.append(self.extra)
        return self.adapter_cls(self.logger)

    def __exit__(self, *args):
        """Restore the original internal state of the logger adapter."""
        LOCAL_.ctx.pop()