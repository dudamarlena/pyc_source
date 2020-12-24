# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/log.py
# Compiled at: 2019-02-16 11:54:14
# Size of source mod 2**32: 912 bytes
from __future__ import print_function
import os
from pysimplelog import Logger as LOG

class pdbparserLogger(LOG):

    def __new__(cls, *args, **kwds):
        thisSingleton = cls.__dict__.get('__thisSingleton__')
        if thisSingleton is not None:
            return thisSingleton
        cls.__thisSingleton__ = thisSingleton = LOG.__new__(cls)
        return thisSingleton

    def __init__(self, *args, **kwargs):
        (super(pdbparserLogger, self).__init__)(*args, **kwargs)
        logFile = os.path.join(os.getcwd(), 'pdbparser')
        self.set_log_file_basename(logFile)
        self._pdbparserLogger__set_logger_params_from_file()

    def __set_logger_params_from_file(self):
        pass


Logger = pdbparserLogger(name='pdbparser')