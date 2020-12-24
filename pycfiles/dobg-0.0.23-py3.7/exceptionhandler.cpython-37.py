# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/helper/exceptionhandler.py
# Compiled at: 2019-07-25 10:35:19
# Size of source mod 2**32: 783 bytes
import sys
sys.path.append('..')
from digitalocean import DataReadError
from dobg.exceptions.dropletexceptions import InvalidIdException
from dobg.exceptions.configexceptions import TokenException

class ExceptionHandler:

    def __init__(self, exception):
        self.exception = exception

    def handle(self):
        """ Handles thrown exceptions from main script """
        if isinstance(self.exception, TokenException):
            print(self.exception)
        else:
            if isinstance(self.exception, InvalidIdException):
                print(self.exception)
            else:
                print(self.exception)