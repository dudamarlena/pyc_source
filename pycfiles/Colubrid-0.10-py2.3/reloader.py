# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/colubrid/reloader.py
# Compiled at: 2006-04-13 04:57:18
"""
    Reloader Module
    ===============

    Taken from django, which took it from cherrypy / paste
"""
import os, sys, thread, time
RUN_RELOADER = True

def reloader_thread(watch):
    """This thread watches Python and "watch" files and reloads the
    application if something changes."""
    mtimes = {}
    win = sys.platform == 'win32'
    while RUN_RELOADER:
        for filename in [ getattr(m, '__file__', '') for m in sys.modules.values() ] + watch:
            if filename[-4:] in ('.pyo', '.pyc'):
                filename = filename[:-1]
            if not os.path.exists(filename):
                continue
            stat = os.stat(filename)
            mtime = stat.st_mtime
            if win:
                mtime -= stat.st_ctime
            if filename not in mtimes:
                mtimes[filename] = mtime
                continue
            if mtime != mtimes[filename]:
                sys.exit(3)

        time.sleep(1)


def restart_with_reloader():
    """Spawn a new Python interpreter with the same arguments as this one,
    but running the reloader thread."""
    while True:
        args = [
         sys.executable] + sys.argv
        if sys.platform == 'win32':
            args = [ '"%s"' % arg for arg in args ]
        new_environ = os.environ.copy()
        new_environ['RUN_MAIN'] = 'true'
        exit_code = os.spawnve(os.P_WAIT, sys.executable, args, new_environ)
        if exit_code != 3:
            return exit_code


def main(main_func, watch=[]):
    """Call this to initialize the reloader."""
    if os.environ.get('RUN_MAIN') == 'true':
        thread.start_new_thread(main_func, ())
        try:
            reloader_thread(watch)
        except KeyboardInterrupt:
            pass

    else:
        try:
            sys.exit(restart_with_reloader())
        except KeyboardInterrupt:
            pass