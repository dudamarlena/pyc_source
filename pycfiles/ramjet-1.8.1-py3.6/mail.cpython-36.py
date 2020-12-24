# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/utils/mail.py
# Compiled at: 2017-11-06 22:07:51
# Size of source mod 2**32: 968 bytes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ramjet.settings import MAIL_FROM_ADDR, MAIL_HOST, MAIL_PASSWD, MAIL_PORT, MAIL_USERNAME

def send_mail(*, to_addrs, subject, content, from_addr=MAIL_FROM_ADDR):
    """Send email

    Args:
        fr (string):
        to (list): receivers' addresses
    """
    smtp = smtplib.SMTP(host=MAIL_HOST, port=MAIL_PORT)
    smtp.starttls()
    smtp.login(MAIL_USERNAME, MAIL_PASSWD)
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf-8')
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs[0].split(';'))
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'plain'))
    try:
        smtp.sendmail(from_addr, to_addrs, msg.as_string())
    except Exception:
        smtp.close()
        raise


if __name__ == '__main__':
    send_mail(to_addrs=['ppcelery@gmail.com'], subject='test', content='yooo')