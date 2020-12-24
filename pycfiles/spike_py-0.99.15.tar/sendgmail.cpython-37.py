# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/sendgmail.py
# Compiled at: 2019-01-16 17:23:58
# Size of source mod 2**32: 2051 bytes
"""
Sending informations about result etc with Gmail
recipient (to) and attached document (attach) can be a list
"""
from __future__ import print_function
import smtplib, os, sys
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
gmail_user = 'gmalert67@gmail.com'
gmail_pwd = 'IGBMCAlert67'

def add_to_msg(msg, f):
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(f, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)
    return msg


def mail(to, subject, text='', attach=None):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    if type(to) != list:
        msg['To'] = to
    else:
        msg['To'] = ', '.join(to)
    msg['Subject'] = subject
    if text != '':
        msg.attach(MIMEText(text))
    elif attach is not None:
        if type(attach) == list:
            for f in attach:
                msg = add_to_msg(msg, f)

    else:
        msg = add_to_msg(msg, attach)
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()


if __name__ == '__main__':
    mail('lionel.chiron@gmail.com', 'Hello from python!', 'This is a email sent with python', '/Users/chiron/Pictures/kotok.jpg')