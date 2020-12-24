# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/exc.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1160 bytes
"""Treadmill exceptions and utility functions."""
import functools, logging
from . import utils
_LOGGER = logging.getLogger(__name__)

class TreadmillError(Exception):
    __doc__ = 'Base class for all Treadmill errors'


class InvalidInputError(TreadmillError):
    __doc__ = 'Non-fatal error, indicating incorrect input.'

    def __init__(self, source, msg):
        self.source = source
        self.message = msg
        super(InvalidInputError, self).__init__()


class ContainerSetupError(TreadmillError):
    __doc__ = 'Fatal error, indicating problem setting up container environment.'


class NodeSetupError(TreadmillError):
    __doc__ = 'Fatal error, indicating problem initializing the node environment'


def exit_on_unhandled(func):
    """Decorator to exit thread on unhandled exception."""

    @functools.wraps(func)
    def _wrap(*args, **kwargs):
        """Wraps function to exit on unhandled exception."""
        try:
            return func(*args, **kwargs)
        except Exception:
            _LOGGER.exception('Unhandled exception - exiting.')
            utils.sys_exit(-1)

    return _wrap