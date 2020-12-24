# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/vanessa/Documents/Dropbox/Code/share/containershare-python/containershare/logger/message.py
# Compiled at: 2018-07-30 07:44:25
# Size of source mod 2**32: 10870 bytes
__doc__ = '\n\nlogger/message.py: Python logger base for expfactory\n\nCopyright (c) 2016-2017 Vanessa Sochat\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
import os, sys
from .spinner import Spinner
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
TEST = 5
PURPLE = '\x1b[95m'
YELLOW = '\x1b[93m'
RED = '\x1b[91m'
DARKRED = '\x1b[31m'
CYAN = '\x1b[36m'

class ContainerShareMessage:

    def __init__(self, MESSAGELEVEL=None):
        self.level = get_logging_level()
        self.history = []
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
         TEST: PURPLE, 
         'OFF': '\x1b[0m', 
         'CYAN': CYAN, 
         'PURPLE': PURPLE, 
         'RED': RED, 
         'DARKRED': DARKRED, 
         'YELLOW': YELLOW}

    def useColor(self):
        """useColor will determine if color should be added
        to a print. Will check if being run in a terminal, and
        if has support for asci"""
        COLORIZE = get_user_color_preference()
        if COLORIZE is not None:
            return COLORIZE
        else:
            streams = [
             self.errorStream, self.outputStream]
            for stream in streams:
                if not hasattr(stream, 'isatty'):
                    return False
                if not stream.isatty():
                    return False

            return True

    def addColor(self, level, text):
        """addColor to the prompt (usually prefix) if terminal
        supports, and specified to do so"""
        if self.colorize:
            if level in self.colors:
                text = '%s%s%s' % (self.colors[level],
                 text,
                 self.colors['OFF'])
        return text

    def emitError(self, level):
        """determine if a level should print to
        stderr, includes all levels but INFO and QUIET"""
        if level in [ABORT,
         ERROR,
         WARNING,
         VERBOSE,
         VERBOSE1,
         VERBOSE2,
         VERBOSE3,
         DEBUG]:
            return True
        else:
            return False

    def emitOutput(self, level):
        """determine if a level should print to stdout
        only includes INFO"""
        if level in [LOG,
         INFO]:
            return True
        else:
            return False

    def isEnabledFor(self, messageLevel):
        """check if a messageLevel is enabled to emit a level
        """
        if messageLevel <= self.level:
            return True
        else:
            return False

    def emit(self, level, message, prefix=None, color=None):
        """emit is the main function to print the message
        optionally with a prefix
        :param level: the level of the message
        :param message: the message to print
        :param prefix: a prefix for the message
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
        if self.level == QUIET:
            pass
        else:
            if self.isEnabledFor(level):
                if self.emitError(level):
                    self.write(self.errorStream, message)
                else:
                    self.write(self.outputStream, message)
            self.history.append(message)

    def write(self, stream, message):
        """write will write a message to a stream,
        first checking the encoding
        """
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        stream.write(message)

    def get_logs(self, join_newline=True):
        """'get_logs will return the complete history, joined by newline
        (default) or as is.
        """
        if join_newline:
            return '\n'.join(self.history)
        else:
            return self.history

    def show_progress(self, iteration, total, length=40, min_level=0, prefix=None, carriage_return=True, suffix=None, symbol=None):
        """create a terminal progress bar, default bar shows for verbose+
        :param iteration: current iteration (Int)
        :param total: total iterations (Int)
        :param length: character length of bar (Int)
        """
        percent = 100 * (iteration / float(total))
        progress = int(length * iteration // total)
        if suffix is None:
            suffix = ''
        else:
            if prefix is None:
                prefix = 'Progress'
            else:
                if percent >= 100:
                    percent = 100
                    progress = length
                if symbol is None:
                    symbol = '='
            if progress < length:
                bar = symbol * progress + '|' + '-' * (length - progress - 1)
            else:
                bar = symbol * progress + '-' * (length - progress)
        if self.level > min_level:
            percent = '%5s' % '{0:.1f}'.format(percent)
            output = '\r' + prefix + ' |%s| %s%s %s' % (bar, percent, '%', suffix)
            (sys.stdout.write(output),)
            if iteration == total:
                if carriage_return:
                    sys.stdout.write('\n')
            sys.stdout.flush()

    def abort(self, message):
        self.emit(ABORT, message, 'ABORT')

    def critical(self, message):
        self.emit(CRITICAL, message, 'CRITICAL')

    def error(self, message):
        self.emit(ERROR, message, 'ERROR')

    def warning(self, message):
        self.emit(WARNING, message, 'WARNING')

    def log(self, message):
        self.emit(LOG, message, 'LOG')

    def custom(self, prefix, message, color=PURPLE):
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

    def test(self, message):
        self.emit(TEST, message, 'TEST')

    def is_quiet(self):
        """is_quiet returns true if the level is under 1
        """
        if self.level < 1:
            return False
        else:
            return True

    def table(self, rows, col_width=2):
        """table will print a table of entries. If the rows is 
        a dictionary, the keys are interpreted as column names. if
        not, a numbered list is used.
        """
        labels = [str(x) for x in range(1, len(rows) + 1)]
        if isinstance(rows, dict):
            labels = list(rows.keys())
            rows = list(rows.values())
        for row in rows:
            label = labels.pop(0)
            label = label.ljust(col_width)
            message = '\t'.join(row)
            self.custom(prefix=label, message=message)


def get_logging_level():
    """get_logging_level will configure a logging to standard out based on the user's
    selected level, which should be in an environment variable called
    MESSAGELEVEL. if MESSAGELEVEL is not set, the maximum level
    (5) is assumed (all messages).
    """
    try:
        level = int(os.environ.get('MESSAGELEVEL', INFO))
    except ValueError:
        level = os.environ.get('MESSAGELEVEL', INFO)
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
        if level == 'TEST':
            return TEST
        if level.startswith('VERBOSE'):
            return VERBOSE3
        if level == 'LOG':
            return LOG
        if level == 'DEBUG':
            return DEBUG

    return level


def get_user_color_preference():
    COLORIZE = os.environ.get('CONTAINERSHARE_COLORIZE', None)
    if COLORIZE is not None:
        COLORIZE = convert2boolean(COLORIZE)
    return COLORIZE


def convert2boolean(arg):
    """convert2boolean is used for environmental variables that must be
    returned as boolean"""
    if not isinstance(arg, bool):
        return arg.lower() in ('yes', 'true', 't', '1', 'y')
    else:
        return arg


ContainerShareMessage.spinner = Spinner()
bot = ContainerShareMessage()