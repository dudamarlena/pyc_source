# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/cli/spinners.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 5509 bytes
from __future__ import absolute_import, division
import contextlib, itertools, logging, sys, time
from pip._vendor.progress import HIDE_CURSOR, SHOW_CURSOR
from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.logging import get_indentation
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Iterator, IO
logger = logging.getLogger(__name__)

class SpinnerInterface(object):

    def spin(self):
        raise NotImplementedError()

    def finish(self, final_status):
        raise NotImplementedError()


class InteractiveSpinner(SpinnerInterface):

    def __init__(self, message, file=None, spin_chars='-\\|/', min_update_interval_seconds=0.125):
        self._message = message
        if file is None:
            file = sys.stdout
        self._file = file
        self._rate_limiter = RateLimiter(min_update_interval_seconds)
        self._finished = False
        self._spin_cycle = itertools.cycle(spin_chars)
        self._file.write(' ' * get_indentation() + self._message + ' ... ')
        self._width = 0

    def _write(self, status):
        assert not self._finished
        backup = '\x08' * self._width
        self._file.write(backup + ' ' * self._width + backup)
        self._file.write(status)
        self._width = len(status)
        self._file.flush()
        self._rate_limiter.reset()

    def spin(self):
        if self._finished:
            return
        else:
            return self._rate_limiter.ready() or None
        self._write(next(self._spin_cycle))

    def finish(self, final_status):
        if self._finished:
            return
        self._write(final_status)
        self._file.write('\n')
        self._file.flush()
        self._finished = True


class NonInteractiveSpinner(SpinnerInterface):

    def __init__(self, message, min_update_interval_seconds=60):
        self._message = message
        self._finished = False
        self._rate_limiter = RateLimiter(min_update_interval_seconds)
        self._update('started')

    def _update(self, status):
        assert not self._finished
        self._rate_limiter.reset()
        logger.info('%s: %s', self._message, status)

    def spin(self):
        if self._finished:
            return
        else:
            return self._rate_limiter.ready() or None
        self._update('still running...')

    def finish(self, final_status):
        if self._finished:
            return
        self._update(("finished with status '{final_status}'".format)(**locals()))
        self._finished = True


class RateLimiter(object):

    def __init__(self, min_update_interval_seconds):
        self._min_update_interval_seconds = min_update_interval_seconds
        self._last_update = 0

    def ready(self):
        now = time.time()
        delta = now - self._last_update
        return delta >= self._min_update_interval_seconds

    def reset(self):
        self._last_update = time.time()


@contextlib.contextmanager
def open_spinner(message):
    if sys.stdout.isatty() and logger.getEffectiveLevel() <= logging.INFO:
        spinner = InteractiveSpinner(message)
    else:
        spinner = NonInteractiveSpinner(message)
    try:
        with hidden_cursor(sys.stdout):
            yield spinner
    except KeyboardInterrupt:
        spinner.finish('canceled')
        raise
    except Exception:
        spinner.finish('error')
        raise
    else:
        spinner.finish('done')


@contextlib.contextmanager
def hidden_cursor(file):
    if WINDOWS:
        yield
    else:
        if not file.isatty() or logger.getEffectiveLevel() > logging.INFO:
            yield
        else:
            file.write(HIDE_CURSOR)
            try:
                yield
            finally:
                file.write(SHOW_CURSOR)