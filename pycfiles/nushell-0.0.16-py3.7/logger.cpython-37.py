# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/logger.py
# Compiled at: 2019-10-24 14:13:34
# Size of source mod 2**32: 7416 bytes
import os, sys
ABORT = -5
CRITICAL = -4
ERROR = -3
WARNING = -2
LOG = -1
INFO = 1
CUSTOM = 1
QUIET = 0
VERBOSE = VERBOSE1 = 2
VERBOSE2 = 3
VERBOSE3 = 4
DEBUG = 5
PURPLE = '\x1b[95m'
YELLOW = '\x1b[93m'
RED = '\x1b[91m'
DARKRED = '\x1b[31m'
CYAN = '\x1b[36m'

class NushellLogger:

    def __init__(self, logfile=None, level=None):
        """the logger is based on discovery in the environment, and is
           initialized by the plugin. By default we print logs to an output
           file that is named according to the plugin, unless the user
           sets the level to quiet.

           Parameters
           ==========
           logfile: should be the path to write the logfile
           level: can be an integer or string level, defaults to DEBUG
        """
        self.level = get_logging_level(level)
        self.logfile = logfile
        self.errorStream = sys.stderr
        self.outputStream = sys.stdout
        self.colorize = self.useColor()
        self.colors = {ABORT: DARKRED, 
         CRITICAL: RED, 
         ERROR: RED, 
         WARNING: YELLOW, 
         LOG: PURPLE, 
         CUSTOM: PURPLE, 
         DEBUG: CYAN, 
         'OFF': '\x1b[0m', 
         'CYAN': CYAN, 
         'PURPLE': PURPLE, 
         'RED': RED, 
         'DARKRED': DARKRED, 
         'YELLOW': YELLOW}

    def useColor(self):
        """useColor will determine if color should be added
           to a print. If logging to file, no color is used. Otherwise, we
           check if being run in a terminal, and if has support for ascii
        """
        if self.logfile:
            return False
        streams = [self.errorStream, self.outputStream]
        for stream in streams:
            if hasattr(stream, 'isatty'):
                return stream.isatty() or False

        return True

    def addColor(self, level, text):
        """addColor to the prompt (usually prefix) if terminal
           supports, and specified to do so
        """
        if self.colorize:
            if level in self.colors:
                text = '%s%s%s' % (self.colors[level],
                 text,
                 self.colors['OFF'])
        return text

    def emitError(self, level):
        """determine if a level should print to
           stderr, includes all levels but INFO and QUIET
        """
        return level in [ABORT,
         ERROR,
         WARNING,
         VERBOSE,
         VERBOSE1,
         VERBOSE2,
         VERBOSE3,
         DEBUG]

    def emitOutput(self, level):
        """determine if a level should print to stdout (only INFO and LOG)
        """
        return level in [LOG, INFO]

    def isEnabledFor(self, messageLevel):
        """check if a messageLevel is enabled to emit a level
        """
        return messageLevel <= self.level and not self.is_quiet()

    def emit(self, level, message, prefix=None, color=None):
        """emit is the main function to print the message
           optionally with a prefix. If we have a logfile, we print
           to it instead.

           Parameters
           ==========
           level: the level of the message
           message: the message to print
           prefix: a prefix for the message
        """
        if color is None:
            color = level
        else:
            if prefix is not None:
                prefix = self.addColor(color, '%s ' % prefix)
            else:
                prefix = ''
                message = self.addColor(color, message)
            message = '%s%s' % (prefix, message)
            if not message.endswith('\n'):
                message = '%s\n' % message
            if self.logfile and self.isEnabledFor(level):
                self.writeFile(message)
            else:
                if self.isEnabledFor(level):
                    if self.emitError(level):
                        self.write(self.errorStream, message)
                    else:
                        self.write(self.outputStream, message)

    def write(self, stream, message):
        """write a message to a stream, and check the encoding
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        stream.write(message)

    def writeFile(self, message):
        """write a message to a stream, and check the encoding
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        with open(self.logfile, 'a') as (filey):
            filey.writelines(message)

    def abort(self, message):
        self.emit(ABORT, message, 'ABORT')

    def critical(self, message):
        self.emit(CRITICAL, message, 'CRITICAL')

    def error(self, message):
        self.emit(ERROR, message, 'ERROR')

    def exit(self, message, return_code=1):
        self.emit(ERROR, message, 'ERROR')
        sys.exit(return_code)

    def warning(self, message):
        self.emit(WARNING, message, 'WARNING')

    def log(self, message):
        self.emit(LOG, message, 'LOG')

    def custom(self, prefix, message='', color=PURPLE):
        self.emit(CUSTOM, message, prefix, color)

    def info(self, message):
        self.emit(INFO, message)

    def newline(self):
        return self.info('')

    def verbose(self, message):
        self.emit(VERBOSE, message, 'VERBOSE')

    def verbose1(self, message):
        self.emit(VERBOSE, message, 'VERBOSE1')

    def verbose2(self, message):
        self.emit(VERBOSE2, message, 'VERBOSE2')

    def verbose3(self, message):
        self.emit(VERBOSE3, message, 'VERBOSE3')

    def debug(self, message):
        self.emit(DEBUG, message, 'DEBUG')

    def is_quiet(self):
        """is_quiet returns true if the level is 0
        """
        return self.level == QUIET


def get_logging_level(default_level=None):
    """get_logging_level based on an int or user specific string, default INFO
    """
    if not default_level:
        default_level = DEBUG
    level = os.environ.get('MESSAGELEVEL', default_level)
    if isinstance(level, int):
        return level
    if level == 'CRITICAL':
        return CRITICAL
    if level == 'ABORT':
        return ABORT
    if level == 'ERROR':
        return ERROR
    if level == 'WARNING':
        return WARNING
    if level == 'LOG':
        return LOG
    if level == 'INFO':
        return INFO
    if level == 'QUIET':
        return QUIET
    if level.startswith('VERBOSE'):
        return VERBOSE3
    if level == 'LOG':
        return LOG
    if level == 'DEBUG':
        return DEBUG
    return level