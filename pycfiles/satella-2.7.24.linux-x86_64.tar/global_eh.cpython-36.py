# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/exception_handling/global_eh.py
# Compiled at: 2020-05-12 15:04:16
# Size of source mod 2**32: 3639 bytes
import sys, threading, typing as tp
from satella.coding import wraps
from satella.coding.structures import Singleton
from satella.instrumentation import Traceback
from .exception_handlers import BaseExceptionHandler, FunctionExceptionHandler, exception_handler
__all__ = [
 'GlobalExcepthook']

@Singleton
class GlobalExcepthook:
    __doc__ = '\n    Global event interceptor.\n\n    Always installed\n    '
    __slots__ = ('installed_hooks', 'ignore_failed_hooks', 'old_excepthook')

    def __init__(self):
        self.installed_hooks = []
        self.ignore_failed_hooks = True
        self._GlobalExcepthook__install()

    def remove_hook(self, hook: BaseExceptionHandler):
        """
        Unregister a hook

        :param hook: hook to remove
        :raise ValueError: if hook not in list
        """
        self.installed_hooks.remove(hook)

    def add_hook(self, new_hook: tp.Union[(
 tp.Callable, BaseExceptionHandler)]) -> BaseExceptionHandler:
        """
        Register a hook to fire in case of an exception.

        :param new_hook: callable(type, value, traceback) or instance of BaseExceptionHandler to use
        """
        if not isinstance(new_hook, BaseExceptionHandler):
            new_hook = FunctionExceptionHandler(new_hook)
        if new_hook not in self.installed_hooks:
            self.installed_hooks.append(new_hook)
        return new_hook

    def __install(self):
        """Enable _GlobalExceptHook to intercept exception_handling"""
        self.old_excepthook = exception_handler(priority=10000)(sys.excepthook)
        sys.excepthook = self._GlobalExcepthook__except_handle
        init_old = threading.Thread.__init__
        my_self = self

        @wraps(threading.Thread.__init__)
        def init(self, *args, **kwargs):
            init_old(self, *args, **kwargs)
            run_old = self.run

            @wraps(run_old)
            def run_with_except_hook(*args, **kw):
                try:
                    return run_old(*args, **kw)
                except Exception as e:
                    try:
                        (my_self._GlobalExcepthook__except_handle)(*sys.exc_info())
                    except AttributeError:
                        pass

                    raise

            self.run = run_with_except_hook

        threading.Thread.__init__ = init

    def __except_handle(self, type_, value, traceback) -> None:
        hooks_to_run = self.installed_hooks + [self.old_excepthook]
        for hook in sorted(hooks_to_run, key=(lambda h: h.priority)):
            try:
                if hook.handle_exception(type_, value, traceback):
                    break
            except Exception as e:
                tb = Traceback()
                sys.stderr.write('Error while processing a hook: \n')
                tb.pretty_print(output=(sys.stderr))
                if not self.ignore_failed_hooks:
                    raise NotImplementedError('Hook failed (%s), but ignore_failed_hooks was false' % repr(e))


GlobalExcepthook()