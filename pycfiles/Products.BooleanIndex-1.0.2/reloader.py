# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/reloader.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = '\nA file monitor and server restarter.\n\nUse this like:\n\n..code-block:: Python\n\n    import reloader\n    reloader.install()\n\nThen make sure your server is installed with a shell script like::\n\n    err=3\n    while test "$err" -eq 3 ; do\n        python server.py\n        err="$?"\n    done\n\nor is run from this .bat file (if you use Windows)::\n\n    @echo off\n    :repeat\n        python server.py\n    if %errorlevel% == 3 goto repeat\n\nor run a monitoring process in Python (``paster serve --reload`` does\nthis).  \n\nUse the ``watch_file(filename)`` function to cause a reload/restart for\nother other non-Python files (e.g., configuration files).  If you have\na dynamic set of files that grows over time you can use something like::\n\n    def watch_config_files():\n        return CONFIG_FILE_CACHE.keys()\n    paste.reloader.add_file_callback(watch_config_files)\n\nThen every time the reloader polls files it will call\n``watch_config_files`` and check all the filenames it returns.\n'
import os, sys, time, threading, traceback
from paste.util.classinstance import classinstancemethod

def install(poll_interval=1):
    """
    Install the reloading monitor.

    On some platforms server threads may not terminate when the main
    thread does, causing ports to remain open/locked.  The
    ``raise_keyboard_interrupt`` option creates a unignorable signal
    which causes the whole application to shut-down (rudely).
    """
    mon = Monitor(poll_interval=poll_interval)
    t = threading.Thread(target=mon.periodic_reload)
    t.setDaemon(True)
    t.start()


class Monitor(object):
    instances = []
    global_extra_files = []
    global_file_callbacks = []

    def __init__(self, poll_interval):
        self.module_mtimes = {}
        self.keep_running = True
        self.poll_interval = poll_interval
        self.extra_files = list(self.global_extra_files)
        self.instances.append(self)
        self.file_callbacks = list(self.global_file_callbacks)

    def periodic_reload(self):
        while True:
            if not self.check_reload():
                os._exit(3)
                break
            time.sleep(self.poll_interval)

    def check_reload(self):
        filenames = list(self.extra_files)
        for file_callback in self.file_callbacks:
            try:
                filenames.extend(file_callback())
            except:
                print >> sys.stderr, 'Error calling paste.reloader callback %r:' % file_callback
                traceback.print_exc()

        for module in sys.modules.values():
            try:
                filename = module.__file__
            except (AttributeError, ImportError), exc:
                continue

            if filename is not None:
                filenames.append(filename)

        for filename in filenames:
            try:
                stat = os.stat(filename)
                if stat:
                    mtime = stat.st_mtime
                else:
                    mtime = 0
            except (OSError, IOError):
                continue

            if filename.endswith('.pyc'):
                if os.path.exists(filename[:-1]):
                    mtime = max(os.stat(filename[:-1]).st_mtime, mtime)
                elif filename.endswith('$py.class') and os.path.exists(filename[:-9] + '.py'):
                    mtime = max(os.stat(filename[:-9] + '.py').st_mtime, mtime)
                self.module_mtimes[filename] = self.module_mtimes.has_key(filename) or mtime
            elif self.module_mtimes[filename] < mtime:
                print >> sys.stderr, '%s changed; reloading...' % filename
                return False

        return True

    def watch_file(self, cls, filename):
        """Watch the named file for changes"""
        filename = os.path.abspath(filename)
        if self is None:
            for instance in cls.instances:
                instance.watch_file(filename)

            cls.global_extra_files.append(filename)
        else:
            self.extra_files.append(filename)
        return

    watch_file = classinstancemethod(watch_file)

    def add_file_callback(self, cls, callback):
        """Add a callback -- a function that takes no parameters -- that will
        return a list of filenames to watch for changes."""
        if self is None:
            for instance in cls.instances:
                instance.add_file_callback(callback)

            cls.global_file_callbacks.append(callback)
        else:
            self.file_callbacks.append(callback)
        return

    add_file_callback = classinstancemethod(add_file_callback)


if sys.platform.startswith('java'):
    try:
        from _systemrestart import SystemRestart
    except ImportError:
        pass
    else:

        class JythonMonitor(Monitor):
            """
            Monitor that utilizes Jython's special
            ``_systemrestart.SystemRestart`` exception.

            When raised from the main thread it causes Jython to reload
            the interpreter in the existing Java process (avoiding
            startup time).

            Note that this functionality of Jython is experimental and
            may change in the future.
            """

            def periodic_reload(self):
                while True:
                    if not self.check_reload():
                        raise SystemRestart()
                    time.sleep(self.poll_interval)


watch_file = Monitor.watch_file
add_file_callback = Monitor.add_file_callback