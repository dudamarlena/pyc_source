# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dronekit/util.py
# Compiled at: 2019-03-14 01:22:55
from __future__ import print_function
import logging, sys

def errprinter(*args):
    logger(*args)


def logger(*args):
    print(file=sys.stderr, *args)
    sys.stderr.flush()


class ErrprinterHandler(logging.Handler):
    """Logging handler to support the deprecated `errprinter` argument to connect()"""

    def __init__(self, errprinter):
        logging.Handler.__init__(self)
        self.errprinter = errprinter

    def emit(self, record):
        msg = self.format(record)
        self.errprinter(msg)