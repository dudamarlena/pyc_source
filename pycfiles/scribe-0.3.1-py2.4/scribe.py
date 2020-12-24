# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.6.0-Power_Macintosh/egg/scribe.py
# Compiled at: 2006-04-02 06:13:26
import logging, sys, os.path
from pprint import pformat
casual_format = logging.Formatter('%(message)s')
formal_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(casual_format)
current_file = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
verbosity = logging.WARNING
if '-v' in sys.argv:
    verbosity = logging.DEBUG

class Scribe:
    __module__ = __name__

    def __init__(self, name):
        self._scribe = logging.getLogger(name)

    def __getattr__(self, key):
        return getattr(self._scribe, key)

    def setLevel(self, lvl):
        if type(lvl) is type(''):
            lvl = getattr(logging, lvl.upper())
        self._scribe.setLevel(lvl)


class CasualScribe(Scribe):
    __module__ = __name__

    def __init__(self, name='scribe', verbosity=logging.WARNING):
        Scribe.__init__(self, name)
        self._scribe.addHandler(stdout_handler)
        self._scribe.setLevel(verbosity)


class FormalScribe(Scribe):
    __module__ = __name__

    def __init__(self, name='scribe', verbosity=logging.WARNING, file='%s.log' % current_file):
        Scribe.__init__(self, name)
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formal_format)
        self._scribe.addHandler(file_handler)
        self._scribe.addHandler(stdout_handler)
        self._scribe.setLevel(verbosity)


loggingapi = CasualScribe(verbosity=verbosity)
_scribe = CasualScribe(verbosity=verbosity)

def setScribe(logger):
    _scribe = logger


def setLevel(lvl):
    _scribe.setLevel(lvl)


def log(lvl, msg, *args, **kwargs):
    _scribe.log(lvl, msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    log(logging.CRITICAL, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    log(logging.ERROR, msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    log(logging.WARNING, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    log(logging.INFO, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    log(logging.DEBUG, msg, *args, **kwargs)


def dump(*args, **kwargs):
    msg = ''
    if len(args):
        msg += pformat(args)
    if len(kwargs.keys()):
        msg += pformat(kwargs)
    debug(msg)