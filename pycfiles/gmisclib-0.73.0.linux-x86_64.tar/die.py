# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/die.py
# Compiled at: 2011-04-10 18:39:27
from __future__ import with_statement
import os, sys, traceback, threading
debug = True
nocompress = False
Threads = False
_name = os.path.basename(sys.argv[0])

class counter:
    lock = threading.Lock()

    def __init__(self):
        self.reps = 0
        self.last = None
        self.sequence = 0
        self.memory = {}
        self.stderr = sys.stderr
        self.stdout = sys.stdout
        assert self.stderr is not None
        assert self.stdout is not None
        return

    def set_out_err(self, stdout, stderr):
        self.stdout.flush()
        self.stderr.flush()
        self.stdout = stdout
        self.stderr = stderr

    def incoming(self, msgtype, name, s):
        if Threads:
            id = '%s(%s)' % (msgtype, threading.currentThread().name)
        else:
            id = msgtype
        t = (
         id, name, s)
        if nocompress or t != self.last:
            self.showdump('%s: %s: %s\n' % (id, name, s))
            self.last = t
        else:
            self.clearmem()
            self.reps += 1
        assert self.stderr is not None
        assert self.stdout is not None
        return

    def showreps(self):
        if self.last is not None and self.reps > 1:
            self.stderr.write('%s: last message repeated %d times.\n' % (
             self.last[0], self.reps))
            self.last = None
            self.reps = 1
        return

    def showdump(self, s):
        self.stdout.flush()
        self.showreps()
        self.dumpmem()
        if s:
            try:
                self.stderr.write(s)
            except UnicodeEncodeError:
                self.stderr.write(repr(s))

        self.stderr.flush()

    def __del__(self):
        self.showreps()

    def clearmem(self):
        self.memory = {}
        self.sequence = 0

    def dumpmem(self):
        tmp = [ (sqn, k, val) for k, (sqn, val) in self.memory.items() ]
        tmp.sort()
        for sqn, k, val in tmp:
            try:
                self.stderr.write('#NOTE: %s = %s\n' % (k, val))
            except UnicodeEncodeError:
                self.stderr.write('#NOTE: %s = %s\n' % (k, repr(val)))

        self.clearmem()

    def memorize(self, key, value):
        self.memory[key] = (
         self.sequence, value)
        self.sequence += 1


_q = counter()

def die(s):
    """Output a fatal error message and terminate.
        Before the error message, it summarizes all the calls to L{note}.
        @param s: error message
        @type s: str
        """
    e = 'ERR: %s: %s' % (_name, s)
    exit(1, e)


def warn(s):
    """Output a non-fatal warning.
        Before the warning, it summarizes all the calls to L{note}.
        @param s: warning message
        @type s: str
        """
    global _q
    with _q.lock:
        _q.incoming('#WARN', _name, s)


def info(s):
    """Output useful information.
        Before the message, it summarizes all the calls to L{note}.
        @param s: message
        @type s: str
        """
    with _q.lock:
        _q.incoming('#INFO', _name, s)


def catch(extext=None):
    """Call this inside an except statement.
        It will report the exception and any other information it has.
        """
    etype, value, tback = sys.exc_info()
    if extext is None:
        extext = 'die.catch: exception caught.\n'
    with _q.lock:
        _q.showdump('')
        traceback.print_exception(etype, value, tback)
        etype = None
        value = None
        tback = None
        _q.stderr.flush()
        _q.stdout.flush()
    return


def catchexit(extext=None, n=1, text=None):
    """Call this inside an except statement.  It will report
        all information and then exit."""
    catch(extext)
    exit(n, text=text)


def dbg(s):
    """Output debugging information, if debug is nonzero.
        Before the debugging info, it prints all information given to L{note}.
        @param s: debug message
        @type s: str
        """
    if debug:
        _q.incoming('#DBG', _name, s)


def exit(n, text=None):
    """Exit, after dumping accumulated L{note}s.
        @param n: the processes' exit code
        @type n: int
        @param text: something to print
        @type text: L{str} or L{None}
        """
    with _q.lock:
        _q.showdump('')
        if text is not None:
            _q.stdout.write('%s\n' % text)
            _q.stdout.flush()
        if text is not None:
            _q.stderr.write('%s\n' % text)
            _q.stderr.flush()
    sys.exit(n)
    return


def note(key, value):
    """Memorize a note, which will be output along with the next error/warning/info message.
        These will be printed in the form '#NOTE key = value', with value converted to a string
        at the time of printing.   Note that only the most recent note is kept for each key.
        @type key: str
        @type value: anything
        """
    with _q.lock:
        _q.memorize(key, value)


def get(key):
    """Get the most recent value memorized by a call to L{note}.
        @type key: str
        @rtype: whatever was memorized
        """
    with _q.lock:
        try:
            return _q.memory[key][1]
        except KeyError:
            pass

    return


if __name__ == '__main__':
    debug = 1
    info('You should see a debug message next.')
    dbg('This is the debug message.')
    debug = 0
    note('gleep', 'oldest note')
    note('foo', 'bar')
    note('foo', 'fleep')
    note('foo', 'foo')
    note('farf', 'newest note')
    info('You should not see a debug message next.')
    dbg("This is the debug message you shouldn't see.")
    warn('This is a warning.')
    warn('This is a warning.')
    warn('This is a warning.')
    info('It should have been repeated three times.')
    die('This is the end.')