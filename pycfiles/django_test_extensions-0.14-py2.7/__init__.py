# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test_extensions/__init__.py
# Compiled at: 2009-10-24 11:46:38
import os, sys, traceback
from django.utils import autoreload
_mtimes = autoreload._mtimes
_win = autoreload._win
_code_changed = autoreload.code_changed
_error_files = []

def my_code_changed():
    global _mtimes
    global _win
    for filename in filter(lambda v: v, map(lambda m: getattr(m, '__file__', None), sys.modules.values())) + _error_files:
        if filename.endswith('.pyc') or filename.endswith('.pyo'):
            filename = filename[:-1]
        if not os.path.exists(filename):
            continue
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if _win:
            mtime -= stat.st_ctime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            try:
                del _error_files[_error_files.index(filename)]
            except ValueError:
                pass
            else:
                return True

    return False


def check_errors(fn):

    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except (ImportError, IndentationError, NameError, SyntaxError, TypeError):
            et, ev, tb = sys.exc_info()
            if getattr(ev, 'filename', None) is None:
                filename = traceback.extract_tb(tb)[(-1)][0]
            else:
                filename = ev.filename
            if filename not in _error_files:
                _error_files.append(filename)
            raise

        return

    return wrapper


_main = autoreload.main

def my_main(main_func, args=None, kwargs=None):
    wrapped_main_func = check_errors(main_func)
    _main(wrapped_main_func, args=args, kwargs=kwargs)


autoreload.code_changed = my_code_changed
autoreload.main = my_main