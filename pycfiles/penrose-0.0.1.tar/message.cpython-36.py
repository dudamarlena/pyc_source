# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vanessa/Desktop/sregistry-cli/sregistry/logger/message.py
# Compiled at: 2018-10-13 08:46:26
# Size of source mod 2**32: 10432 bytes
"""

Copyright (C) 2017-2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
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
PURPLE = '\x1b[95m'
YELLOW = '\x1b[93m'
RED = '\x1b[91m'
DARKRED = '\x1b[31m'
CYAN = '\x1b[36m'

class SRegistryMessage:

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
 
           Parameters
           ==========
           iteration: current iteration (Int)
           total: total iterations (Int)
           length: character length of bar (Int)
        """
        if not self.level == QUIET:
            percent = 100 * (iteration / float(total))
            progress = int(length * iteration // total)
            if suffix is None:
                suffix = ''
            if prefix is None:
                prefix = 'Progress'
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
    level = os.environ.get('MESSAGELEVEL', INFO)
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
    else:
        if level == 'DEBUG':
            return DEBUG
        return level


def get_user_color_preference():
    COLORIZE = os.environ.get('SINGULARITY_COLORIZE', None)
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


SRegistryMessage.spinner = Spinner()
bot = SRegistryMessage()