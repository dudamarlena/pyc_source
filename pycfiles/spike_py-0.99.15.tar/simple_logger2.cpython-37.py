# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/simple_logger2.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 2850 bytes
"""
Created by Lionel Chiron  18/10/2013 
Copyright (c) 2013 __NMRTEC__. All rights reserved.

Utility for copying Standard Error (stderr) and Standard Output (stdout) to a file

"""
from __future__ import print_function
import sys, os
from datetime import datetime
import os.path as op
import unittest, threading

def strdate():
    n = datetime.now()
    return n.strftime('%a-%d-%b-%Y-%H-%M-%S')


class _Writer(object):
    __doc__ = '\n    Writes two fluxes. One to the standard console(flux) and the other one in a file(log)\n    input: \n        flux: stderr or stdout\n        log: file descriptor of the log file\n    '

    def __init__(self, flux, log, prefix=''):
        self.log = log
        self.flux = flux
        self.prefix = prefix
        self.newline = True

    def write(self, message):
        """
        Writes the flux in console and in file
        """
        self.flux.write(message)
        if self.newline:
            self.log.write(self.prefix + message)
        else:
            self.log.write(message)
        self.newline = message.endswith('\n')

    def close(self):
        """
        do nothing
        """
        pass

    def flush(self):
        """
        flush both flux
        """
        self.flux.flush()
        self.log.flush()


class TeeLogger(object):
    __doc__ = '\n    Simple logger.\n\n    TeeLogger(log_name = "log_file.log", erase = False, date_in = True, err_prefix = "___")\n    or \n    TeeLogger()\n\n    copies standard Error (stderr) and Standard Output (stdout) to a file\n    \n    log_name : name of the log file, if no name given, it is called "log_file.log"\n    erase : if True erase the existing log file with the same name.\n    date_in: in True (defualt) date is indicated in log file \n    err_prefix stderr is prefixed with this string\n    '

    def __init__(self, log_name='log_file.log', erase=False, date_in=True, err_prefix='___'):
        self.log_name = log_name
        if erase:
            choice_write = 'w'
        else:
            choice_write = 'a'
        self.log = open(self.log_name, choice_write)
        if date_in:
            self.log.write('\n========================================\nTeeLogging information from stdout and stderr\n%s\n\n' % strdate())
        self.stdout = _Writer(sys.stdout, self.log)
        self.stderr = _Writer((sys.stderr), (self.log), prefix=err_prefix)
        sys.stderr = self.stderr
        sys.stdout = self.stdout


if __name__ == '__main__':
    unittest.main()