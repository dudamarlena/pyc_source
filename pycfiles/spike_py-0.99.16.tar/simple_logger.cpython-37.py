# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/simple_logger.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 3704 bytes
"""
Created by Lionel Chiron  18/10/2013 
Copyright (c) 2013 __NMRTEC__. All rights reserved.

Utility for reporting Standard Error (stderr) and Standard Output (stdout)
Typical syntax is: 
    import sys
    sys.stderr = Logger()
    f = open("fff.jpg")
If the picture "fff.jpg" doesn't exist, an arror message is sent by mail. 
"""
from __future__ import print_function
import sys, os
from time import sleep, localtime, strftime
import os.path as op
import unittest
from mail import GMAIL
import threading

class Writer(object):
    __doc__ = '\n    Writes two fluxes. One to the standard console(flux) and the other one in a file(log)\n    If mail is given, send a mail with attached report. \n    input: \n        flux: stderr or stdout\n        log: address of the log file\n        mail_address: mail address for mail alerts\n        log_name: log file for mail alerts\n        date_in: date indicated in log file\n    '

    def __init__(self, flux, log, mail_address=None, log_name=None, date_in=False):
        self.log = log
        self.flux = flux
        self.mail_address = mail_address
        self.log_name = log_name

    def send_mail(self):
        a = threading.Thread(None, self.mail_if_error, None)
        a.start()

    def mail_if_error(self):
        print('sending mail')
        sleep(1)
        gm = GMAIL()
        gm.send(to=(self.mail_address), subject='logger report', text='here is lof file attached',
          attach=(self.log_name))

    def write(self, message):
        """
        Writes the flux in console and in file
        """
        self.flux.write(message)
        self.log.write(message)

    def flush(self):
        """
        flushes all 
        """
        self.flux.close()
        self.log.close()
        if self.mail_address:
            self.send_mail()


class Logger(object):
    __doc__ = '\n    Simple logger.\n    input:\n        erase : by default False. if True erase the existing log file with the same name.\n        log_name : name of the log file, if no name given, it calls it anonymously "log_file"\n        date : if True adds the date after the name\n        date_in: date indicated in log file \n        mail: mail address for mail alerts  \n    output:\n        log file with name log_name\n    '

    def __init__(self, erase=False, log_name=None, date=False, date_in=False, mail=None):
        if not log_name:
            self.log_name = 'log_file'
        else:
            self.log_name = log_name
        if date:
            self.log_name += self.datetime()
        else:
            self.log_name += '.log'
            if erase:
                choice_write = 'w'
            else:
                choice_write = 'a'
        self.log = open(self.log_name, choice_write)
        self.stderr = Writer((sys.stderr), (self.log), mail_address=mail,
          log_name=(self.log_name))
        self.stdout = Writer((sys.stdout), (self.log), mail_address=mail,
          log_name=(self.log_name))
        sys.stderr = self.stderr
        sys.stdout = self.stdout

    def datetime(self):
        return strftime('%Y-%h-%d-%Hh%M', localtime())


class Test(unittest.TestCase):
    Logger(erase=True)
    print('hello toto')
    f = open('fff.jpg')


if __name__ == '__main__':
    unittest.main()