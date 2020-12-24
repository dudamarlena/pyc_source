# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/turbomail/adapters/tm_pylons.py
# Compiled at: 2009-08-26 19:42:26
"""Pylons (and thus TurboGears 2) helper functions."""
import atexit, re
from paste.deploy.converters import asbool
from pylons import config
from turbomail.control import interface
__all__ = [
 'start_extension', 'shutdown_extension']

class FakeConfigObj(object):
    """TODO: Docstring incomplete."""

    def __init__(self, real_config):
        self._config = real_config
        self._nr_regex = re.compile('^(\\d+)$')

    def get(self, option, default):
        value = self._config.get(option, default)
        return self._convert(option, value)

    def _convert(self, option, value):
        if value is not None:
            boolean_options = ('mail.smtp.tls', 'mail.tls', 'mail.smtp.debug', 'mail.debug')
            should_be_bool = option.endswith('.on') or option in boolean_options
            if should_be_bool:
                value = asbool(value)
            elif hasattr(value, 'isdigit') and value.isdigit():
                value = int(value)
        return value

    def update(self, new_value_dict):
        self._config.update(new_value_dict)


def start_extension():
    atexit.register(shutdown_extension)
    interface.start(FakeConfigObj(config))


def shutdown_extension():
    interface.stop()