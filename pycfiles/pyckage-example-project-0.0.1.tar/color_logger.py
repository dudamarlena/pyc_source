# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyck/lib/color_logger.py
# Compiled at: 2014-03-15 01:11:56
import sys, logging

class ColorLogger(logging.getLoggerClass()):
    """
    Logger class that by default outputs to stderr
    """
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
    """
    Log Handler for console that outputs colored log messages according to their severity
    """
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