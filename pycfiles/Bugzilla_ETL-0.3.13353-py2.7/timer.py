# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\timer.py
# Compiled at: 2013-11-22 17:13:19
import time
from .strings import expand_template
from .logs import Log

class Timer:
    """
    USAGE:
    with Timer("doing hard time"):
        something_that_takes_long()
    OUTPUT:
        doing hard time took 45.468 sec
    """

    def __init__(self, description, param=None):
        self.description = expand_template(description, param)

    def __enter__(self):
        Log.note('Timer start: {{description}}', {'description': self.description})
        self.start = time.clock()
        return self

    def __exit__(self, type, value, traceback):
        self.end = time.clock()
        self.interval = self.end - self.start
        Log.note('Timer end  : {{description}} (took {{duration}} sec)', {'description': self.description, 
           'duration': round(self.interval, 3)})

    @property
    def duration(self):
        return self.interval