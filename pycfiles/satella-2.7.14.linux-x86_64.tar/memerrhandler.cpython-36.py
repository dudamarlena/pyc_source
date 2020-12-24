# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/exception_handling/memerrhandler.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 2428 bytes
import sys, time, typing as tp
from satella.coding.recast_exceptions import silence_excs
from satella.posix import suicide
from .exception_handlers import BaseExceptionHandler, ALWAYS_FIRST, ExceptionHandlerCallable

class MemoryErrorExceptionHandler(BaseExceptionHandler):
    __doc__ = "\n    A handler that terminates the entire process (or process group) is a MemoryError is seen.\n\n    `custom_hook` is an exception callable to implement you own behavior. If it returns True,\n    then MemoryErrorExceptionHandler won't kill anyone. You can also provide a CallableGroup\n    with gather=True - if any of callables returns True, the process won't be killed.\n    "
    __slots__ = ('priority', '_free_on_memory_error', 'custom_hook', 'kill_pg', 'installed')

    def __init__(self, custom_hook=lambda type_, value, traceback: False, kill_pg=False):
        """
        :param kill_pg: whether to kill entire process group, if applicable
        """
        super().__init__(ALWAYS_FIRST)
        self._free_on_memory_error = {'a': bytearray(2048)}
        self.custom_hook = custom_hook
        self.kill_pg = kill_pg
        self.installed = False

    def install(self):
        if self.installed:
            raise RuntimeError('already installed')
        from .global_eh import GlobalExcepthook
        GlobalExcepthook().add_hook(self)

    def handle_exception(self, type_, value, traceback) -> tp.Optional[bool]:
        if not issubclass(type_, MemoryError):
            return
        else:
            with silence_excs(KeyError):
                del self._free_on_memory_error['a']
            with silence_excs(Exception):
                val = self.custom_hook(type_, value, traceback)
                if isinstance(val, tp.Sequence):
                    val = any(val)
                if val:
                    return True
            try:
                sys.stderr.write('satella.exception_handling: MemoryError seen, killing\n')
                sys.stderr.flush()
            except (IOError, OSError):
                pass

            suicide(self.kill_pg)
            time.sleep(5)
            return True