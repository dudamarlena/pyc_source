# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/log/handler.py
# Compiled at: 2015-11-06 23:45:35
import sys, logging
from .formatter import Formatter

def gen_handler(filename=None, stream=None):
    """
    Generate a log handler for either a file or a stream. If both are
    specified, only use the filename. If neither is specified, use stderr.

    KWArgs:
        @filename=None
        The file to which messages should be logged. If specified, takes
        precedence over @stream.

        @stream=None
        The file-like object to which log messages should be streamed.
    """
    if filename:
        hdlr = logging.FileHandler(filename)
    else:
        shortver = sys.version_info[:2]
        if shortver == (2, 6):
            if stream:
                hdlr = logging.StreamHandler(stream)
            else:
                hdlr = logging.StreamHandler()
        else:
            hdlr = logging.StreamHandler(stream=stream)
    hdlr.setFormatter(Formatter())
    return hdlr


try:
    NullHandler = logging.NullHandler
except AttributeError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass