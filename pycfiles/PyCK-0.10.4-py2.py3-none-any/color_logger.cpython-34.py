# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/color_logger.py
# Compiled at: 2014-03-15 01:11:56
# Size of source mod 2**32: 1656 bytes
import sys, logging

class ColorLogger(logging.getLoggerClass()):
    __doc__ = '\n    Logger class that by default outputs to stderr\n    '
    out = sys.stdout
    err = sys.stderr
    INFO = '\x1b[92m'
    WARNING = '\x1b[93m'
    ERROR = '\x1b[91m'
    ENDC = '\x1b[0m'

    def __init__(self, name, output_file=sys.stdout, error_file=sys.stderr):
        self.out = output_file
        self.err = error_file

    def log(self, msg):
        self.out.write(msg + '\n')

    def warn(self, msg):
        self.err.write(self.WARNING + msg + self.ENDC + '\n')

    def error(self, msg):
        self.err.write(self.ERROR + msg + self.ENDC + '\n')

    def info(self, msg):
        self.out.write(self.INFO + msg + self.ENDC + '\n')


class ConsoleColorHandler(logging.StreamHandler):
    __doc__ = '\n    Log Handler for console that outputs colored log messages according to their severity\n    '
    _log_colors = {logging.CRITICAL: '\x1b[91m', 
     logging.ERROR: '\x1b[91m', 
     logging.WARNING: '\x1b[93m', 
     logging.INFO: '\x1b[92m', 
     logging.DEBUG: '\x1b[94m', 
     logging.NOTSET: '\x1b[0m'}
    terminator = '\x1b[0m\n'

    def __init__(self, stream=None):
        super(ConsoleColorHandler, self).__init__(stream)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(self._log_colors[record.levelno])
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)