# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\HuoYan_monitoring\utils.py
# Compiled at: 2020-05-06 01:17:04
# Size of source mod 2**32: 1999 bytes
import os, sys, logging, smtplib, mimetypes
from email.message import EmailMessage
import logging, time, io, datetime
from imbox import Imbox
import re, email.header

def fetch_mail(user: str, passwd: str, atatch_dir: str, imap_server: str='mail.genomics.cn', port: int=143, start_time: datetime.datetime=datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().date().timetuple()))):
    out_path = atatch_dir
    imbox = Imbox(imap_server, username=user, password=passwd, ssl=False, starttls=False)
    messages = imbox.messages(date__gt=start_time)
    for _, message in messages:
        subject = message.subject
        if subject.startswith('新冠报告'):
            for attachment in message.attachments:
                name, _ = email.header.decode_header(attachment['filename'])[0]
                if name.startswith('报告'):
                    filename = os.path.join(out_path, 'tmp', name)
                    filename = re.sub('\\?\\=\\ \\=\\?UTF\\-8\\?Q\\?', '', filename)
                    content = attachment['content']
                    with open(filename, 'wb') as (w_f):
                        w_f.write(content.getvalue())


def send_mail(mail_to: list=[], mail_cc: list=[], mail_bcc: list=[], mail_subject: str='', mail_body: str='', user: str='bgi-peta@genomics.cn', passwd: str='Peta2018_6', host: str='mail.genomics.cn', port: int=25):
    msg = EmailMessage()
    msg['Subject'] = mail_subject
    msg['To'] = ','.join(mail_to)
    msg['From'] = user
    msg['CC'] = ','.join(mail_cc)
    msg.set_content(mail_body)
    with smtplib.SMTP(host, port) as (sender):
        sender.ehlo()
        sender.starttls()
        sender.login(user, passwd)
        sender.send_message(msg)
        sender.quit()