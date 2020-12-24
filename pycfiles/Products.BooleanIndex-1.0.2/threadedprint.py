# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/threadedprint.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = "\nthreadedprint.py\n================\n\n:author: Ian Bicking\n:date: 12 Jul 2004\n\nMulti-threaded printing; allows the output produced via print to be\nseparated according to the thread.\n\nTo use this, you must install the catcher, like::\n\n    threadedprint.install()\n\nThe installation optionally takes one of three parameters:\n\ndefault\n    The default destination for print statements (e.g., ``sys.stdout``).\nfactory\n    A function that will produce the stream for a thread, given the\n    thread's name.\nparamwriter\n    Instead of writing to a file-like stream, this function will be\n    called like ``paramwriter(thread_name, text)`` for every write.\n\nThe thread name is the value returned by\n``threading.currentThread().getName()``, a string (typically something\nlike Thread-N).\n\nYou can also submit file-like objects for specific threads, which will\noverride any of these parameters.  To do this, call ``register(stream,\n[threadName])``.  ``threadName`` is optional, and if not provided the\nstream will be registered for the current thread.\n\nIf no specific stream is registered for a thread, and no default has\nbeen provided, then an error will occur when anything is written to\n``sys.stdout`` (or printed).\n\nNote: the stream's ``write`` method will be called in the thread the\ntext came from, so you should consider thread safety, especially if\nmultiple threads share the same writer.\n\nNote: if you want access to the original standard out, use\n``sys.__stdout__``.\n\nYou may also uninstall this, via::\n\n    threadedprint.uninstall()\n\nTODO\n----\n\n* Something with ``sys.stderr``.\n* Some default handlers.  Maybe something that hooks into `logging`.\n* Possibly cache the results of ``factory`` calls.  This would be a\n  semantic change.\n\n"
import threading, sys
from paste.util import filemixin

class PrintCatcher(filemixin.FileMixin):

    def __init__(self, default=None, factory=None, paramwriter=None, leave_stdout=False):
        assert len(filter(lambda x: x is not None, [
         default, factory, paramwriter])) <= 1, 'You can only provide one of default, factory, or paramwriter'
        if leave_stdout:
            assert not default, 'You cannot pass in both default (%r) and leave_stdout=True' % default
            default = sys.stdout
        if default:
            self._defaultfunc = self._writedefault
        elif factory:
            self._defaultfunc = self._writefactory
        elif paramwriter:
            self._defaultfunc = self._writeparam
        else:
            self._defaultfunc = self._writeerror
        self._default = default
        self._factory = factory
        self._paramwriter = paramwriter
        self._catchers = {}

    def write(self, v, currentThread=threading.currentThread):
        name = currentThread().getName()
        catchers = self._catchers
        if not catchers.has_key(name):
            self._defaultfunc(name, v)
        else:
            catcher = catchers[name]
            catcher.write(v)

    def seek(self, *args):
        name = threading.currentThread().getName()
        catchers = self._catchers
        if name not in catchers:
            self._default.seek(*args)
        else:
            catchers[name].seek(*args)

    def read(self, *args):
        name = threading.currentThread().getName()
        catchers = self._catchers
        if name not in catchers:
            self._default.read(*args)
        else:
            catchers[name].read(*args)

    def _writedefault(self, name, v):
        self._default.write(v)

    def _writefactory(self, name, v):
        self._factory(name).write(v)

    def _writeparam(self, name, v):
        self._paramwriter(name, v)

    def _writeerror(self, name, v):
        assert False, 'There is no PrintCatcher output stream for the thread %r' % name

    def register(self, catcher, name=None, currentThread=threading.currentThread):
        if name is None:
            name = currentThread().getName()
        self._catchers[name] = catcher
        return

    def deregister(self, name=None, currentThread=threading.currentThread):
        if name is None:
            name = currentThread().getName()
        assert self._catchers.has_key(name), 'There is no PrintCatcher catcher for the thread %r' % name
        del self._catchers[name]
        return


_printcatcher = None
_oldstdout = None

def install(**kw):
    global _oldstdout
    global _printcatcher
    global deregister
    global register
    if not _printcatcher or sys.stdout is not _printcatcher:
        _oldstdout = sys.stdout
        _printcatcher = sys.stdout = PrintCatcher(**kw)
        register = _printcatcher.register
        deregister = _printcatcher.deregister


def uninstall():
    global _oldstdout
    global _printcatcher
    global deregister
    global register
    if _printcatcher:
        sys.stdout = _oldstdout
        _printcatcher = _oldstdout = None
        register = not_installed_error
        deregister = not_installed_error
    return


def not_installed_error(*args, **kw):
    assert False, 'threadedprint has not yet been installed (call threadedprint.install())'


register = deregister = not_installed_error

class StdinCatcher(filemixin.FileMixin):

    def __init__(self, default=None, factory=None, paramwriter=None):
        assert len(filter(lambda x: x is not None, [
         default, factory, paramwriter])) <= 1, 'You can only provide one of default, factory, or paramwriter'
        if default:
            self._defaultfunc = self._readdefault
        elif factory:
            self._defaultfunc = self._readfactory
        elif paramwriter:
            self._defaultfunc = self._readparam
        else:
            self._defaultfunc = self._readerror
        self._default = default
        self._factory = factory
        self._paramwriter = paramwriter
        self._catchers = {}

    def read(self, size=None, currentThread=threading.currentThread):
        name = currentThread().getName()
        catchers = self._catchers
        if not catchers.has_key(name):
            return self._defaultfunc(name, size)
        else:
            catcher = catchers[name]
            return catcher.read(size)

    def _readdefault(self, name, size):
        self._default.read(size)

    def _readfactory(self, name, size):
        self._factory(name).read(size)

    def _readparam(self, name, size):
        self._paramreader(name, size)

    def _readerror(self, name, size):
        assert False, 'There is no StdinCatcher output stream for the thread %r' % name

    def register(self, catcher, name=None, currentThread=threading.currentThread):
        if name is None:
            name = currentThread().getName()
        self._catchers[name] = catcher
        return

    def deregister(self, catcher, name=None, currentThread=threading.currentThread):
        if name is None:
            name = currentThread().getName()
        assert self._catchers.has_key(name), 'There is no StdinCatcher catcher for the thread %r' % name
        del self._catchers[name]
        return


_stdincatcher = None
_oldstdin = None

def install_stdin(**kw):
    global _oldstdin
    global _stdincatcher
    global deregister_stdin
    global register_stdin
    if not _stdincatcher:
        _oldstdin = sys.stdin
        _stdincatcher = sys.stdin = StdinCatcher(**kw)
        register_stdin = _stdincatcher.register
        deregister_stdin = _stdincatcher.deregister


def uninstall():
    global _stdincatcher
    global deregister_stdin
    global register_stdin
    if _stdincatcher:
        sys.stdin = _oldstdin
        _stdincatcher = _oldstdin = None
        register_stdin = deregister_stdin = not_installed_error_stdin
    return


def not_installed_error_stdin(*args, **kw):
    assert False, 'threadedprint has not yet been installed for stdin (call threadedprint.install_stdin())'