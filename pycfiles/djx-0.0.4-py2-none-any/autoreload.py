# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/autoreload.py
# Compiled at: 2019-02-14 00:35:17
import os, signal, subprocess, sys, time, traceback
from django.apps import apps
from django.conf import settings
from django.core.signals import request_finished
from django.utils import six
from django.utils._os import npath
from django.utils.encoding import get_system_encoding
from django.utils.six.moves import _thread as thread
try:
    import threading
except ImportError:
    pass

try:
    import termios
except ImportError:
    termios = None

USE_INOTIFY = False
try:
    import pyinotify
    fd = pyinotify.INotifyWrapper.create().inotify_init()
    if fd >= 0:
        USE_INOTIFY = True
        os.close(fd)
except ImportError:
    pass

RUN_RELOADER = True
FILE_MODIFIED = 1
I18N_MODIFIED = 2
_mtimes = {}
_win = sys.platform == 'win32'
_exception = None
_error_files = []
_cached_modules = set()
_cached_filenames = []

def gen_filenames(only_new=False):
    """
    Returns a list of filenames referenced in sys.modules and translation
    files.
    """
    global _cached_filenames
    global _cached_modules
    module_values = set(sys.modules.values())
    _cached_filenames = clean_files(_cached_filenames)
    if _cached_modules == module_values:
        if only_new:
            return []
        else:
            return _cached_filenames + clean_files(_error_files)

    new_modules = module_values - _cached_modules
    new_filenames = clean_files([ filename.__file__ for filename in new_modules if hasattr(filename, '__file__')
                                ])
    if not _cached_filenames and settings.USE_I18N:
        basedirs = [
         os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf', 'locale'),
         'locale']
        for app_config in reversed(list(apps.get_app_configs())):
            basedirs.append(os.path.join(npath(app_config.path), 'locale'))

        basedirs.extend(settings.LOCALE_PATHS)
        basedirs = [ os.path.abspath(basedir) for basedir in basedirs if os.path.isdir(basedir)
                   ]
        for basedir in basedirs:
            for dirpath, dirnames, locale_filenames in os.walk(basedir):
                for filename in locale_filenames:
                    if filename.endswith('.mo'):
                        new_filenames.append(os.path.join(dirpath, filename))

    _cached_modules = _cached_modules.union(new_modules)
    _cached_filenames += new_filenames
    if only_new:
        return new_filenames + clean_files(_error_files)
    else:
        return _cached_filenames + clean_files(_error_files)


def clean_files(filelist):
    filenames = []
    for filename in filelist:
        if not filename:
            continue
        if filename.endswith('.pyc') or filename.endswith('.pyo'):
            filename = filename[:-1]
        if filename.endswith('$py.class'):
            filename = filename[:-9] + '.py'
        if os.path.exists(filename):
            filenames.append(filename)

    return filenames


def reset_translations():
    import gettext
    from django.utils.translation import trans_real
    gettext._translations = {}
    trans_real._translations = {}
    trans_real._default = None
    trans_real._active = threading.local()
    return


def inotify_code_changed():
    """
    Checks for changed code using inotify. After being called
    it blocks until a change event has been fired.
    """

    class EventHandler(pyinotify.ProcessEvent):
        modified_code = None

        def process_default(self, event):
            if event.path.endswith('.mo'):
                EventHandler.modified_code = I18N_MODIFIED
            else:
                EventHandler.modified_code = FILE_MODIFIED

    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, EventHandler())

    def update_watch(sender=None, **kwargs):
        if sender and getattr(sender, 'handles_files', False):
            return
        mask = pyinotify.IN_MODIFY | pyinotify.IN_DELETE | pyinotify.IN_ATTRIB | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE | pyinotify.IN_DELETE_SELF | pyinotify.IN_MOVE_SELF
        for path in gen_filenames(only_new=True):
            wm.add_watch(path, mask)

    request_finished.connect(update_watch)
    update_watch()
    notifier.check_events(timeout=None)
    notifier.read_events()
    notifier.process_events()
    notifier.stop()
    return EventHandler.modified_code


def code_changed():
    global _mtimes
    global _win
    for filename in gen_filenames():
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
                if filename.endswith('.mo'):
                    return I18N_MODIFIED
                else:
                    return FILE_MODIFIED

    return False


def check_errors(fn):

    def wrapper(*args, **kwargs):
        global _exception
        try:
            fn(*args, **kwargs)
        except Exception:
            _exception = sys.exc_info()
            et, ev, tb = _exception
            if getattr(ev, 'filename', None) is None:
                filename = traceback.extract_tb(tb)[(-1)][0]
            else:
                filename = ev.filename
            if filename not in _error_files:
                _error_files.append(filename)
            raise

        return

    return wrapper


def raise_last_exception():
    if _exception is not None:
        six.reraise(*_exception)
    return


def ensure_echo_on():
    if termios:
        fd = sys.stdin
        if fd.isatty():
            attr_list = termios.tcgetattr(fd)
            if not attr_list[3] & termios.ECHO:
                attr_list[3] |= termios.ECHO
                if hasattr(signal, 'SIGTTOU'):
                    old_handler = signal.signal(signal.SIGTTOU, signal.SIG_IGN)
                else:
                    old_handler = None
                termios.tcsetattr(fd, termios.TCSANOW, attr_list)
                if old_handler is not None:
                    signal.signal(signal.SIGTTOU, old_handler)
    return


def reloader_thread():
    ensure_echo_on()
    if USE_INOTIFY:
        fn = inotify_code_changed
    else:
        fn = code_changed
    while RUN_RELOADER:
        change = fn()
        if change == FILE_MODIFIED:
            sys.exit(3)
        elif change == I18N_MODIFIED:
            reset_translations()
        time.sleep(1)


def restart_with_reloader():
    while True:
        args = [sys.executable] + [ '-W%s' % o for o in sys.warnoptions ] + sys.argv
        new_environ = os.environ.copy()
        if _win and six.PY2:
            encoding = get_system_encoding()
            for key in new_environ.keys():
                str_key = key.decode(encoding).encode('utf-8')
                str_value = new_environ[key].decode(encoding).encode('utf-8')
                del new_environ[key]
                new_environ[str_key] = str_value

        new_environ['RUN_MAIN'] = 'true'
        exit_code = subprocess.call(args, env=new_environ)
        if exit_code != 3:
            return exit_code


def python_reloader(main_func, args, kwargs):
    if os.environ.get('RUN_MAIN') == 'true':
        thread.start_new_thread(main_func, args, kwargs)
        try:
            reloader_thread()
        except KeyboardInterrupt:
            pass

    else:
        try:
            exit_code = restart_with_reloader()
            if exit_code < 0:
                os.kill(os.getpid(), -exit_code)
            else:
                sys.exit(exit_code)
        except KeyboardInterrupt:
            pass


def jython_reloader(main_func, args, kwargs):
    from _systemrestart import SystemRestart
    thread.start_new_thread(main_func, args)
    while True:
        if code_changed():
            raise SystemRestart
        time.sleep(1)


def main(main_func, args=None, kwargs=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}
    if sys.platform.startswith('java'):
        reloader = jython_reloader
    else:
        reloader = python_reloader
    wrapped_main_func = check_errors(main_func)
    reloader(wrapped_main_func, args, kwargs)
    return