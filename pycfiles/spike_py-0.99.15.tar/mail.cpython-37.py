# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/mail.py
# Compiled at: 2019-01-16 17:28:48
# Size of source mod 2**32: 2435 bytes
from __future__ import print_function
import smtplib, sys
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
import os.path as op
import unittest

class GMAIL(object):
    __doc__ = '\n    Class for sending mails with Gmail with smtp protocol.\n    input:\n        gmail_user : name of the Gmail account\n        gmail_pwd  : password of the Gmail account\n        to: destination of the mail\n        subject: subject of the mail\n        text: text to be sent\n        attach: Attached document\n    Usage: \n        gm = GMAIL()\n        gm.send(to = \'gmalert67@gmail.com\', subject = \'test gmail\', text = "hello", attach = None)\n    '

    def __init__(self, gmail_user='gmalert67@gmail.com', gmail_pwd='igbmcalert'):
        self.gmail_user = gmail_user
        self.gmail_pwd = gmail_pwd

    def send(self, to, subject, text='', attach=None):
        self.to = to
        self.subject = subject
        self.text = text
        self.attach = attach
        msg = MIMEMultipart()
        msg['From'] = self.gmail_user
        msg['To'] = self.to
        msg['Subject'] = self.subject
        if text != '':
            msg.attach(MIMEText(self.text))
        if attach != None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(self.attach, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename = "%s"' % op.basename(self.attach))
            msg.attach(part)
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.gmail_user, self.gmail_pwd)
        mailServer.sendmail(self.gmail_user, self.to, msg.as_string())
        mailServer.close()


class Test(unittest.TestCase):
    gm = GMAIL()
    gm.send(to='gmalert67@gmail.com', subject='test gmail', text='hello', attach=None)


if __name__ == '__main__':
    unittest.main()