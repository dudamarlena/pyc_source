# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/greins/reloader.py
# Compiled at: 2011-09-19 19:30:16
import gunicorn.config, os, signal, sys, time, threading
from greins.synchronization import synchronized

class ReloaderSetting(gunicorn.config.Setting):
    name = 'reloader'
    section = 'Greins'
    cli = ['--reloader']
    validator = gunicorn.config.validate_bool
    action = 'store_true'
    default = False
    desc = '        Turn on automatic code reloading.\n\n        This setting is intended for development.\n        '


class Reloader(threading.Thread):
    synchronize_extra_files = synchronized('_extra_files_lock')

    def __init__(self, extra_files=None, interval=1):
        super(Reloader, self).__init__()
        self.setDaemon(True)
        self._extra_files = set(extra_files or ())
        self._extra_files_lock = threading.RLock()
        self._interval = interval

    @synchronize_extra_files
    def add_extra_file(self, filename):
        self._extra_files.add(filename)

    @synchronize_extra_files
    def extend_by_extra_files(self, destination):
        destination.extend(self._extra_files)

    def get_files(self):

        def iter_module_files():
            for module in sys.modules.values():
                filename = getattr(module, '__file__', None)
                if filename:
                    old = None
                    while not os.path.isfile(filename):
                        old = filename
                        filename = os.path.dirname(filename)
                        if filename == old:
                            break
                    else:
                        if filename[-4:] in ('.pyc', '.pyo'):
                            filename = filename[:-1]
                        yield filename

            return

        fnames = []
        fnames.extend(iter_module_files())
        self.extend_by_extra_files(fnames)
        return fnames

    def run(self):
        mtimes = {}
        while 1:
            for filename in self.get_files():
                try:
                    mtime = os.stat(filename).st_mtime
                except OSError:
                    continue

                old_time = mtimes.get(filename)
                if old_time is None:
                    mtimes[filename] = mtime
                    continue
                elif mtime > old_time:
                    print ' * Detected change in %r, reloading' % filename
                    os.kill(os.getpid(), signal.SIGQUIT)

            time.sleep(self._interval)

        return