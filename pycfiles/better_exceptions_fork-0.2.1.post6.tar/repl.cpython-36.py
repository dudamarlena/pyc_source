# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\adrie\Desktop\Programmation\better-exceptions\better_exceptions\repl.py
# Compiled at: 2018-01-24 17:26:56
# Size of source mod 2**32: 1412 bytes
from code import InteractiveConsole
import sys
REPL_ID_PREFIX = '@@@REPL@@@'
repl = None

class BetterExceptionsConsole(InteractiveConsole, object):

    def __init__(self):
        super(BetterExceptionsConsole, self).__init__()
        self.last_command = None
        self.entries = dict()
        self.last_code = None
        self.last_id = None
        self.counter = 0

    def runcode(self, code):
        assert self.last_code is not None
        self.entries[self.last_id] = (code,) + self.last_code
        return super(BetterExceptionsConsole, self).runcode(code)

    def runsource(self, source, loc='<input>', symbol='single'):
        self.last_code = (
         loc, source)
        self.last_id = loc = '{}{}'.format(REPL_ID_PREFIX, self.counter)
        self.counter += 1
        return super(BetterExceptionsConsole, self).runsource(source, loc, symbol)

    def showtraceback(self):
        try:
            exctype, val, tb = sys.exc_info()
            sys.excepthook(exctype, val, tb)
        finally:
            del tb


def get_repl():
    global repl
    return repl


def interact(quiet=False, banner=None):
    global repl
    repl = BetterExceptionsConsole()
    banner = '' if quiet else banner
    repl.interact(banner)