# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/autoreload.py
# Compiled at: 2010-03-01 05:38:51
import os, sys, thread, time
RUN_RELOADER = True
reloadFiles = []
termination_func = None

def install_terminator(tfunct):
    global termination_func
    termination_func = tfunct


def reloader_thread():
    mtimes = {}
    while RUN_RELOADER:
        for filename in filter(lambda v: v, map(lambda m: getattr(m, '__file__', None), sys.modules.values())) + reloadFiles:
            if filename.endswith('.pyc'):
                filename = filename[:-1]
            mtime = os.stat(filename).st_mtime
            if filename not in mtimes:
                mtimes[filename] = mtime
                continue
            if mtime > mtimes[filename]:
                if termination_func is not None:
                    termination_func('Reload triggered', 3)
                else:
                    sys.exit(3)

        time.sleep(1)

    return


def restart_with_reloader():
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


def main(main_func, args=None, kwargs=None):
    if os.environ.get('RUN_MAIN') == 'true':
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        thread.start_new_thread(main_func, args, kwargs)
        try:
            reloader_thread()
        except KeyboardInterrupt:
            pass

    else:
        try:
            sys.exit(restart_with_reloader())
        except KeyboardInterrupt:
            pass

        return