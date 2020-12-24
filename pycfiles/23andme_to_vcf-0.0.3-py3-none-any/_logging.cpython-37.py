# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/steven/Documents/Projects/radio/EOR/OthersCodes/21cmFAST/21cmFAST/src/py21cmfast/_logging.py
# Compiled at: 2020-02-13 15:47:20
# Size of source mod 2**32: 1129 bytes
__doc__ = 'Configure logging for py21cmfast.\n\nSignificantly, adds a new formatter which prepends the PID of the logging process to\nany output. This is helpful when running multiple threads in MPI.\n'
import logging, sys
from multiprocessing import current_process

class PIDFormatter(logging.Formatter):
    """PIDFormatter"""
    _mylogger = logging.getLogger('21cmFAST')

    def format(self, record):
        """Set the format of the log."""
        fmt = '{asctime} | {levelname} |'
        if self._mylogger.level <= logging.DEBUG:
            fmt += ' {filename}::{funcName}() |'
        if current_process().name != 'MainProcess':
            fmt += ' pid={process} |'
        self._style = logging.StrFormatStyle(fmt + ' {message}')
        return logging.Formatter.format(self, record)


def configure_logging():
    """Configure logging for the '21cmFAST' logger."""
    hdlr = logging.StreamHandler(sys.stderr)
    hdlr.setFormatter(PIDFormatter())
    logger = logging.getLogger('21cmFAST')
    logger.addHandler(hdlr)