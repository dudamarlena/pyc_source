# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/printer.py
# Compiled at: 2015-09-04 08:27:04
from __future__ import print_function

class Printer:
    """Output printing abstraction"""

    def print(self, text, end='\n'):
        raise NotImplementedError

    def __enter__(self):
        return self

    def close(self):
        raise NotImplementedError

    def __exit__(self, type, value, traceback):
        self.close()


class StdoutPrinter(Printer):
    """Prints to stdout"""

    def print(self, text, end='\n'):
        print(text, end=end)

    def close(self):
        pass


class FilePrinter(Printer):

    def __init__(self, fs_path):
        self.__f = fs_path.open('w')

    def print(self, text, end='\n'):
        print(text, file=self.__f, end=end)

    def close(self):
        self.__f.close()