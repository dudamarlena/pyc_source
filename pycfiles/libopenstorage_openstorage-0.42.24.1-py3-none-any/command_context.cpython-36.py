# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/cli/command_context.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 796 bytes
from contextlib import contextmanager
from pip._vendor.contextlib2 import ExitStack

class CommandContextMixIn(object):

    def __init__(self):
        super(CommandContextMixIn, self).__init__()
        self._in_main_context = False
        self._main_context = ExitStack()

    @contextmanager
    def main_context(self):
        assert not self._in_main_context
        self._in_main_context = True
        try:
            with self._main_context:
                yield
        finally:
            self._in_main_context = False

    def enter_context(self, context_provider):
        assert self._in_main_context
        return self._main_context.enter_context(context_provider)