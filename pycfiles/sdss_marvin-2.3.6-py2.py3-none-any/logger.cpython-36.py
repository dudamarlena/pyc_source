# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/marvin_brain/python/brain/core/logger.py
# Compiled at: 2018-08-13 18:12:44
# Size of source mod 2**32: 7994 bytes
"""
This module defines a logging class based on the built-in logging module.
The module is heavily based on the astropy logging system.
"""
from __future__ import print_function
import logging, os, re, shutil, sys, warnings
from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
from textwrap import TextWrapper
from brain.core.colourPrint import colourPrint
from brain.core.exceptions import BrainError, BrainWarning
log = None
IMPORTANT = 25
logging.addLevelName(IMPORTANT, 'IMPORTANT')
ansi_escape = re.compile('\\x1b[^m]*m')

def important(self, message, *args, **kws):
    (self._log)(IMPORTANT, message, args, **kws)


logging.Logger.important = important

def initLog(logFilePath, logLevel='INFO', logFileLevel='DEBUG', mode='append', wrapperLength=80):
    logging.setLoggerClass(BrainLogger)
    log = logging.getLogger('Brain')
    log._set_defaults(logLevel=logLevel, logFileLevel=logFileLevel, logFilePath=logFilePath, mode=mode,
      wrapperLength=wrapperLength)
    return log


class MyFormatter(logging.Formatter):
    warning_fmp = '%(asctime)s - %(levelname)s: %(message)s [%(origin)s]'
    info_fmt = '%(asctime)s - %(levelname)s - %(message)s [%(funcName)s @ ' + '%(filename)s]'

    def __init__(self, fmt='%(levelname)s - %(message)s [%(funcName)s @ ' + '%(filename)s]'):
        logging.Formatter.__init__(self, fmt, datefmt='%Y-%m-%d %H:%M:%S')

    def format(self, record):
        format_orig = self._fmt
        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.info_fmt
        else:
            if record.levelno == logging.INFO:
                self._fmt = MyFormatter.info_fmt
            else:
                if record.levelno == logging.ERROR:
                    self._fmt = MyFormatter.info_fmt
                else:
                    if record.levelno == logging.WARNING:
                        self._fmt = MyFormatter.warning_fmp
                    else:
                        if record.levelno == IMPORTANT:
                            self._fmt = MyFormatter.info_fmt
        record.msg = ansi_escape.sub('', record.msg)
        result = logging.Formatter.format(self, record)
        self._fmt = format_orig
        return result


Logger = logging.getLoggerClass()
fmt = MyFormatter()

class BrainLogger(Logger):
    __doc__ = 'This class is used to set up the logging system.\n\n    The main functionality added by this class over the built-in\n    logging.Logger class is the ability to keep track of the origin of the\n    messages, the ability to enable logging of warnings.warn calls and\n    exceptions, and the addition of colorized output and context managers to\n    easily capture messages to a file or list.\n\n    '

    def saveLog(self, path):
        shutil.copyfile(self.logFilename, os.path.expanduser(path))

    def _warn(self, *args, **kwargs):
        """Overrides `warnings.warn`

        Before calling the original `warnings.warn` function it makes sure
        the warning is redirected to the correct ``showwarning`` function.

        """
        if issubclass(kwargs['category'], BrainWarning):
            (self._show_warning)(*args, **kwargs)
        else:
            (warnings._showwarning_orig)(*args, **kwargs)

    def _show_warning(self, *args, **kwargs):
        warning = args[0]
        message = '{0}: {1}'.format(warning.__class__.__name__, args[0])
        mod_path = args[2]
        mod_name = None
        mod_path, __ = os.path.splitext(mod_path)
        for __, mod in sys.modules.items():
            mod_file = getattr(mod, '__file__', '')
            if mod_file is not None:
                path = os.path.splitext(mod_file)[0]
                if path == mod_path:
                    mod_name = mod.__name__
                    break

        if mod_name is not None:
            self.warning(message, extra={'origin': mod_name})
        else:
            self.warning(message, extra={'origin': 'no_module'})

    def warning(self, message, *args, **kwargs):
        if args:
            message = message % args
        extra = kwargs.get('extra', None)
        if extra is None:
            extra = {'origin': ''}
        super(BrainLogger, self).warning(message, extra=extra)

    def _stream_formatter(self, record):
        """The formatter for standard output."""
        if record.levelno < logging.DEBUG:
            print((record.levelname), end='')
        else:
            if record.levelno < logging.INFO:
                colourPrint((record.levelname), 'green', end='')
            else:
                if record.levelno < IMPORTANT:
                    colourPrint((record.levelname), 'magenta', end='')
                else:
                    if record.levelno < logging.WARNING:
                        colourPrint((record.levelname), 'lightblue', end='')
                    else:
                        if record.levelno < logging.ERROR:
                            colourPrint((record.levelname), 'brown', end='')
                        else:
                            colourPrint((record.levelname), 'red', end='')
            if record.levelno == logging.WARN:
                message = '{0}'.format(record.msg[record.msg.find(':') + 2:])
            else:
                message = '{0}'.format(record.msg)
        if len(message) > self.wrapperLength:
            tw = TextWrapper()
            tw.width = self.wrapperLength
            tw.subsequent_indent = ' ' * (len(record.levelname) + 2)
            tw.break_on_hyphens = False
            message = '\n'.join(tw.wrap(message))
        print(': ' + message)

    def _set_defaults(self, logLevel='WARNING', logFileLevel='INFO', logFilePath='~/.brain/brain.log', mode='append', wrapperLength=70):
        """Reset logger to its initial state."""
        for handler in self.handlers[:]:
            self.removeHandler(handler)

        self.setLevel('DEBUG')
        self.sh = logging.StreamHandler()
        self.sh.emit = self._stream_formatter
        self.addHandler(self.sh)
        self.wrapperLength = wrapperLength
        logFilePath = os.path.expanduser(logFilePath)
        logDir = os.path.dirname(logFilePath)
        if not os.path.exists(logDir):
            os.mkdir(logDir)
        try:
            if mode.lower() == 'overwrite':
                self.fh = FileHandler(logFilePath, mode='w')
            else:
                if mode.lower() == 'append':
                    self.fh = TimedRotatingFileHandler(logFilePath,
                      when='midnight', utc=True)
                else:
                    raise BrainError('logger mode {0} not recognised'.format(mode))
        except (IOError, OSError) as e:
            warnings.warn('log file {0!r} could not be opened for writing: {1}'.format(logFilePath, unicode(e)), RuntimeWarning)
        else:
            self.fh.setFormatter(fmt)
            self.addHandler(self.fh)
        self.sh.setLevel(logging.CRITICAL)
        self.fh.setLevel(logging.DEBUG)
        self.debug('')
        self.debug('--------------------------------')
        self.debug('----- Restarting logger. -------')
        self.debug('--------------------------------')
        self.sh.setLevel(logLevel)
        self.fh.setLevel(logFileLevel)
        self.logFilename = logFilePath