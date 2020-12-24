# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergii/eclipse-workspaces/django_handlebars/django_handlebars/utils.py
# Compiled at: 2012-03-11 16:18:35
import os, sys, re
from threading import Lock

def cant_compile():
    blockers = []
    try:
        import spidermonkey
    except ImportError:
        blockers.append('Missing "python-spidermonkey" module')

    return blockers


def cant_observe():
    blockers = []
    if sys.platform != 'linux2':
        blockers.append('Available only on Linux platform with "pyinotify" module istalled')
    else:
        try:
            import pyinotify
        except ImportError:
            blockers.append('Missing "pyinotify" module')

    return blockers


def is_outdated(src_file, compiled_file):
    return not os.path.exists(compiled_file) or int(os.stat(compiled_file).st_mtime * 1000) < int(os.stat(src_file).st_mtime * 1000)


def thread_safe(func):
    lock = Lock()

    def decorated(*args, **kwargs):
        with lock:
            ret = func(*args, **kwargs)
            return ret

    return decorated


class ReadableError(Exception):
    pass


class Console(object):
    colors = {'black': '\x1b[30m', 
       'red': '\x1b[31m', 'green': '\x1b[32m', 
       'yellow': '\x1b[33m', 'blue': '\x1b[34m', 
       'purple': '\x1b[35m', 'cyan': '\x1b[36m', 
       'reset': '\x1b[0m'}

    def __init__(self, out=None, err=None, raw=False):
        self._out = out or sys.stdout
        self._err = err or sys.stderr
        self.raw = raw
        self.re = re.compile('<color:(%s)>' % ('|').join(self.colors.keys()))

    def _colorize(self, match):
        if self.raw:
            return ''
        return self.colors.get(match.group(1), '')

    def _format(self, s):
        return self.re.sub(self._colorize, '%s<color:reset>\n' % s)

    def set_out(self, out):
        self._out = out

    def set_err(self, err):
        self._err = err

    @thread_safe
    def out(self, s):
        self._out.write(self._format(s))
        self._out.flush()

    @thread_safe
    def err(self, s):
        self._err.write(self._format(s))
        self._err.flush()


class NullConsole(object):
    _stub = lambda *args, **kwargs: None
    __init__ = _stub
    set_out = _stub
    set_err = _stub
    out = _stub
    err = _stub