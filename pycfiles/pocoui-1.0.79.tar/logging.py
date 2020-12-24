# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/logging.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.logging\n    ~~~~~~~~~~~~~~~~~~~\n\n    Pocoo logging module.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
import sys
from datetime import datetime

class Logger(object):
    """
    Generic logging class.
    """
    __module__ = __name__

    def __init__(self, ctx=None, stream=None, timeformat='%H:%M:%S', system=''):
        if stream is not None:
            self._stream = stream
        elif ctx is not None:
            stream = ctx.cfg.get('development', 'log_output', 'stderr')
            if not stream or stream == 'None':
                self._stream = None
            elif stream == 'stdout':
                self._stream = sys.stdout
            elif stream == 'stderr':
                self._stream = sys.stderr
            else:
                self._stream = file(stream, 'w+')
        else:
            self._stream = sys.stderr
        self._timeformat = timeformat
        self._system = system
        self._write = self._stream.write
        if hasattr(self._stream, 'flush'):
            self._flush = self._stream.flush
        else:
            self._flush = lambda : None
        return

    def log(self, msg):
        self._log(1, self._system, msg)

    def info(self, msg):
        self._log(2, self._system, msg)

    def warn(self, msg):
        self._log(3, self._system, msg)

    def fail(self, msg):
        self._log(4, self._system, msg)

    def _log(self, level, system, msg):
        time = datetime.now().strftime(self._timeformat)
        lv = {0: '', 1: 'i ', 2: 'I ', 3: 'W ', 4: 'E '}.get(level, '? ')
        self._write('%s[%s] %s: %s\n' % (lv, time, system, msg))
        self._flush()