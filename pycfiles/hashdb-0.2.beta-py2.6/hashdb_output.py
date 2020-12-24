# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_output.py
# Compiled at: 2011-01-06 01:19:27
import logging, sys, hashdb_onsigint
from hashdb_onsigint import isatty
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
QUIET = WARNING
DEFAULT = INFO
VERBOSE = DEFAULT - 1

class LevelFilter(logging.Filter, object):

    def __init__(self, levelfrom, levelto, include=True):
        super(LevelFilter, self).__init__()
        self.levelfrom = levelfrom
        self.levelto = levelto
        self.include = include

    def filter(self, record):
        f = self.levelfrom or record.levelno
        t = self.levelto or record.levelno + 1
        if self.include:
            return record.levelno >= f and record.levelno < t
        else:
            return record.levelno < f or record.levelno >= t


class StdStream(logging.StreamHandler, object):
    ESC_RESET = '\x1b[0m'
    ESC_FG = '\x1b[22;3%dm'
    ESC_FG_BRIGHT = '\x1b[1;3%dm'
    ESC_FG_DEFAULT = '\x1b[39m'
    ESC_BG = '\x1b[22;4%dm'
    ESC_BG_BRIGHT = '\x1b[1;4%dm'
    ESC_BG_DEFAULT = '\x1b[49m'
    ESC_BOLD = '\x1b[1m'
    (ESC_FG_BLACK, ESC_FG_RED, ESC_FG_GREEN, ESC_FG_YELLOW, ESC_FG_BLUE, ESC_FG_MAGENTA, ESC_FG_CYAN, ESC_FG_WHITE) = [ ESC_FG % i for i in range(8) ]
    (ESC_FG_BBLACK, ESC_FG_BRED, ESC_FG_BGREEN, ESC_FG_BYELLOW, ESC_FG_BBLUE, ESC_FG_BMAGENTA, ESC_FG_BCYAN, ESC_FG_BWHITE) = [ ESC_FG_BRIGHT % i for i in range(8) ]
    (ESC_BG_BLACK, ESC_BG_RED, ESC_BG_GREEN, ESC_BG_YELLOW, ESC_BG_BLUE, ESC_BG_MAGENTA, ESC_BG_CYAN, ESC_BG_WHITE) = [ ESC_BG % i for i in range(8) ]
    (ESC_BG_BBLACK, ESC_BG_BRED, ESC_BG_BGREEN, ESC_BG_BYELLOW, ESC_BG_BBLUE, ESC_BG_BMAGENTA, ESC_BG_BCYAN, ESC_BG_BWHITE) = [ ESC_BG_BRIGHT % i for i in range(8) ]

    def __init__(self, stream=None, levelfrom=None, levelto=None, include=True):
        super(StdStream, self).__init__(stream)
        f = LevelFilter(levelfrom, levelto, include)
        self.addFilter(f)

    def format_block(self, prefix, record, suffix):
        if record.levelno >= logging.WARNING and isatty(sys.stderr) or record.levelno < logging.WARNING and isatty(sys.stdout):
            return prefix + super(StdStream, self).format(record) + suffix + self.ESC_RESET
        else:
            return super(StdStream, self).format(record)

    def format(self, record):
        if record.levelno >= logging.ERROR:
            return self.format_block(self.ESC_BG_RED + '%s:' % record.levelname + self.ESC_RESET + '\n', record, '\n' + self.ESC_BG_RED + 'END OF %s' % record.levelname + self.ESC_RESET + '\n')
        else:
            if record.levelno >= logging.WARNING:
                return self.format_block(self.ESC_BG_MAGENTA + '%s:' % record.levelname + self.ESC_RESET + ' ', record, '')
            if record.levelno <= logging.DEBUG:
                return self.format_block(self.ESC_FG_BGREEN, record, '')
            if record.levelno < logging.INFO:
                return self.format_block(self.ESC_FG_BLUE, record, '')
            return super(StdStream, self).format(record)


class Logger(logging.getLoggerClass(), object):

    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)
        console = StdStream()
        self.addHandler(StdStream(sys.stdout, levelto=WARNING))
        self.addHandler(StdStream(sys.stderr, levelfrom=WARNING))

    is_quiet = property(lambda self: self.level <= QUIET)
    is_default = property(lambda self: self.level <= DEFAULT)
    is_verbose = property(lambda self: self.level <= VERBOSE)
    is_debug = property(lambda self: self.level <= DEBUG)

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def default(self, msg, *args, **kwargs):
        return super(Logger, self).info(msg, *args, **kwargs)

    def verbose(self, msg, *args, **kwargs):
        return super(Logger, self).log((logging.INFO - 1), msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return super(Logger, self).debug(msg, *args, **kwargs)


logging.setLoggerClass(Logger)
log = logging.getLogger('hashdb')
log.setLevel(DEBUG)
if __name__ == '__main__':
    log.setLevel(DEBUG)
    print 'quiet  : ', log.is_quiet
    print 'default: ', log.is_default
    print 'verbose: ', log.is_verbose
    print 'debug  : ', log.is_debug
    log.default('default message')
    log.verbose('verbose message')
    log.debug('debug message')
    log.warning('warning message')
    log.error('error message')
    try:
        raise RuntimeError, 'this is an exception'
    except Exception, ex:
        log.exception('exception message')