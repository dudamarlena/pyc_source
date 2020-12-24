# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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