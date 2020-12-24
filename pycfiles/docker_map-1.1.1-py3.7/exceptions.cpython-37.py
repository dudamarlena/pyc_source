# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/exceptions.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 2281 bytes
from __future__ import unicode_literals
import traceback, six

class SourceExceptionMixin(object):

    def __init__(self, src_exc, *args, **kwargs):
        self._src_exc = src_exc
        (super(SourceExceptionMixin, self).__init__)(*args, **kwargs)

    @property
    def source_exception(self):
        """
        The original exception information from where the error occurred. Tuple of exception type and exception
        instance (e.g. the output of ``sys.exc_info()``).

        :return: Exception tuple.
        :rtype: tuple
        """
        return self._src_exc

    @property
    def source_message(self):
        """
        Formatted output of the exception, without the stack trace.

        :return: Exception text.
        :rtype: unicode | str
        """
        return ''.join(traceback.format_exception_only(self._src_exc[0], self._src_exc[1]))

    def reraise(self):
        """
        Utility method for re-raising the original exception, including output of its stacktrace.
        """
        (six.reraise)(*self._src_exc)


class PartialResultsMixin(object):

    def __init__(self, partial_results, *args, **kwargs):
        self._results = partial_results
        (super(PartialResultsMixin, self).__init__)(*args, **kwargs)

    @property
    def results(self):
        """
        Partial results before the exception occurred.

        :return: list
        """
        return self._results


@six.python_2_unicode_compatible
class PartialResultsError(SourceExceptionMixin, PartialResultsMixin, Exception):
    __doc__ = '\n    Exception where partial results might be available.\n    '

    def __str__(self):
        return self.source_message


@six.python_2_unicode_compatible
class DockerStatusError(Exception):

    def __init__(self, message, detail):
        self._message = message
        if isinstance(detail, dict):
            detail.pop('message', None)
            if not detail:
                self._detail = None
            else:
                self._detail = detail
        elif detail:
            self._detail = detail

    @property
    def message(self):
        return self._message

    @property
    def detail(self):
        return self._detail

    def __str__(self):
        return self._message