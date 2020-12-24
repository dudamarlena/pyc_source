# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/cli/command_context.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 975 bytes
from contextlib import contextmanager
from pip._vendor.contextlib2 import ExitStack
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Iterator, ContextManager, TypeVar
    _T = TypeVar('_T', covariant=True)

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