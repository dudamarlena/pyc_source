# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/mail_error_logger.py
# Compiled at: 2019-01-16 17:29:56
# Size of source mod 2**32: 3802 bytes
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
import sys, os, threading, smtplib, sys
if sys.version_info[0] < 3:
    import email.MIMEMultipart as MIMEMultipart
    import email.MIMEBase as MIMEBase
    import email.MIMEText as MIMEText
    from email import Encoders
else:
    from email import encoders as Encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
from time import sleep, localtime, strftime
from uuid import getnode as get_mac
import os.path as op
gmail_user = 'gmalert67@gmail.com'
gmail_pwd = 'igbmcalert'

def mail(to, subject, text='', attach=None):
    """
   Mailing part
   """
    print('text ', text)
    print('attach ', attach)
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    if text != '':
        msg.attach(MIMEText(text))
    if attach is not None:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename = "%s"' % os.path.basename(attach))
        msg.attach(part)
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()


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
        mac = self.mac() + '_'
        app = op.splitext(op.basename(applic))[0] + '_'
        self.log_name = 'log_' + app + mac + date + '.dat'
        self.log = open(self.log_name, 'w')
        self.trig = False

    def send_mail(self):
        a = threading.Thread(None, self.mail_if_error, None)
        a.start()

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
        if not self.trig:
            self.send_mail()
            self.trig = True

    def mail_if_error(self):
        sleep(1)
        self.log.close()
        mail('lionel.chiron@gmail.com', (self.log_name), attach=(self.log_name))
        os.remove(self.log_name)


if __name__ == '__main__':
    sys.stderr = Logger()
    f = open('fff.jpg')