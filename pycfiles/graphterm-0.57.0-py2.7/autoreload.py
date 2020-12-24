# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/autoreload.py
# Compiled at: 2012-01-23 23:44:33
"""A module to automatically restart the server when a module is modified.

Most applications should not call this module directly.  Instead, pass the
keyword argument ``debug=True`` to the `tornado.web.Application` constructor.
This will enable autoreload mode as well as checking for changes to templates
and static resources.

This module depends on IOLoop, so it will not work in WSGI applications
and Google AppEngine.  It also will not work correctly when HTTPServer's
multi-process mode is used.
"""
from __future__ import with_statement
import functools, logging, os, pkgutil, sys, types, subprocess
from tornado import ioloop
from tornado import process
try:
    import signal
except ImportError:
    signal = None

def start(io_loop=None, check_time=500):
    """Restarts the process automatically when a module is modified.

    We run on the I/O loop, and restarting is a destructive operation,
    so will terminate any pending requests.
    """
    io_loop = io_loop or ioloop.IOLoop.instance()
    add_reload_hook(functools.partial(_close_all_fds, io_loop))
    modify_times = {}
    callback = functools.partial(_reload_on_update, modify_times)
    scheduler = ioloop.PeriodicCallback(callback, check_time, io_loop=io_loop)
    scheduler.start()


def wait():
    """Wait for a watched file to change, then restart the process.

    Intended to be used at the end of scripts like unit test runners,
    to run the tests again after any source file changes (but see also
    the command-line interface in `main`)
    """
    io_loop = ioloop.IOLoop()
    start(io_loop)
    io_loop.start()


_watched_files = set()

def watch(filename):
    """Add a file to the watch list.

    All imported modules are watched by default.
    """
    _watched_files.add(filename)


_reload_hooks = []

def add_reload_hook(fn):
    """Add a function to be called before reloading the process.

    Note that for open file and socket handles it is generally
    preferable to set the ``FD_CLOEXEC`` flag (using `fcntl` or
    `tornado.platform.auto.set_close_exec`) instead of using a reload
    hook to close them.
    """
    _reload_hooks.append(fn)


def _close_all_fds(io_loop):
    for fd in io_loop._handlers.keys():
        try:
            os.close(fd)
        except Exception:
            pass


_reload_attempted = False

def _reload_on_update(modify_times):
    global _reload_attempted
    if _reload_attempted:
        return
    else:
        if process.task_id() is not None:
            return
        for module in sys.modules.values():
            if not isinstance(module, types.ModuleType):
                continue
            path = getattr(module, '__file__', None)
            if not path:
                continue
            if path.endswith('.pyc') or path.endswith('.pyo'):
                path = path[:-1]
            _check_file(modify_times, path)

        for path in _watched_files:
            _check_file(modify_times, path)

        return


def _check_file(modify_times, path):
    try:
        modified = os.stat(path).st_mtime
    except Exception:
        return

    if path not in modify_times:
        modify_times[path] = modified
        return
    if modify_times[path] != modified:
        logging.info('%s modified; restarting server', path)
        _reload()


def _reload():
    global _reload_attempted
    _reload_attempted = True
    for fn in _reload_hooks:
        fn()

    if hasattr(signal, 'setitimer'):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
    if sys.platform == 'win32':
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    else:
        try:
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except OSError:
            os.spawnv(os.P_NOWAIT, sys.executable, [
             sys.executable] + sys.argv)
            sys.exit(0)


_USAGE = 'Usage:\n  python -m tornado.autoreload -m module.to.run [args...]\n  python -m tornado.autoreload path/to/script.py [args...]\n'

def main():
    """Command-line wrapper to re-run a script whenever its source changes.
    
    Scripts may be specified by filename or module name::

        python -m tornado.autoreload -m tornado.test.runtests
        python -m tornado.autoreload tornado/test/runtests.py

    Running a script with this wrapper is similar to calling
    `tornado.autoreload.wait` at the end of the script, but this wrapper
    can catch import-time problems like syntax errors that would otherwise
    prevent the script from reaching its call to `wait`.
    """
    global __file__
    original_argv = sys.argv
    sys.argv = sys.argv[:]
    if len(sys.argv) >= 3 and sys.argv[1] == '-m':
        mode = 'module'
        module = sys.argv[2]
        del sys.argv[1:3]
    else:
        if len(sys.argv) >= 2:
            mode = 'script'
            script = sys.argv[1]
            sys.argv = sys.argv[1:]
        else:
            print >> sys.stderr, _USAGE
            sys.exit(1)
        try:
            if mode == 'module':
                import runpy
                runpy.run_module(module, run_name='__main__', alter_sys=True)
            elif mode == 'script':
                with open(script) as (f):
                    __file__ = script
                    exec f.read() in globals(), globals()
        except SystemExit as e:
            logging.info('Script exited with status %s', e.code)
        except Exception as e:
            logging.warning('Script exited with uncaught exception', exc_info=True)
            if isinstance(e, SyntaxError):
                watch(e.filename)

        logging.info('Script exited normally')
    sys.argv = original_argv
    if mode == 'module':
        watch(pkgutil.get_loader(module).get_filename())
    wait()


if __name__ == '__main__':
    path_prefix = '.' + os.pathsep
    if sys.path[0] == '' and not os.environ.get('PYTHONPATH', '').startswith(path_prefix):
        os.environ['PYTHONPATH'] = path_prefix + os.environ.get('PYTHONPATH', '')
    elif sys.path[0] == os.path.dirname(__file__):
        del sys.path[0]
    main()