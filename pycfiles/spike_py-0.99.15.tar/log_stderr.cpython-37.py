# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/log_stderr.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 1878 bytes
"""
Created by Lionel Chiron  18/10/2013 
Copyright (c) 2013 __NMRTEC__. All rights reserved.

Utility for reporting error from standard error output via gmail. 
When sys.stderr performs a "write", a mail is sent with a report. 
Typical syntax is: 
    import sys
    sys.stderr = Logger()
    f = open("fff.jpg")
If the picture "fff.jpg" doesn't exist, an arror message is sent by mail. 
"""
from __future__ import print_function
import sys, os, threading
from time import sleep, localtime, strftime
from uuid import getnode as get_mac
import os.path as op

class Logger(object):
    __doc__ = '\n    Standard error logger.\n    '

    def __init__(self):
        try:
            applic = sys.modules['__main__'].__file__
        except Exception:
            print('no __file__')
            applic = ''

        self.terminal = sys.stderr
        date = self.datetime()
        app = op.splitext(op.basename(applic))[0] + '_'
        self.log_name = 'log_' + app + date + '.dat'
        self.log = open(self.log_name, 'w')

    def mac(self):
        mac_addr = str(get_mac())
        mac_dic = {'149885691548389': 'kartikeya'}
        if mac_addr in mac_dic:
            return mac_dic[mac_addr]
        return mac_addr

    def datetime(self):
        return strftime('%Y-%m-%d-%H-%M', localtime())

    def write(self, message):
        """
        If error, sys.stderr will call this method
        """
        self.terminal.write(message)
        self.log.write(message)


if __name__ == '__main__':
    sys.stderr = Logger()
    f = open('fff.jpg')