# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\flask_helpers\mailer.py
# Compiled at: 2020-05-09 12:36:50
# Size of source mod 2**32: 1367 bytes
"""
mailer - send email
================================================
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from flask import current_app
from flask_mail import Message
debug = False

def sendmail(subject, fromaddr, toaddr, html, text='', ccaddr=None):
    """
    send mail

    :param subject: subject of email
    :param fromaddr: from address to use
    :param toaddr: to address to use, may be list of addresses
    :param html: html to send
    :param text: optional text alternative to send
    :returns: response from flask_mail.send
    """
    current_app.logger.info('sendmail(): from={}, to={}, cc={}, subject="{}"'.format(fromaddr, toaddr, ccaddr, subject))
    mail = current_app.extensions.get('mail')
    message = Message(sender=fromaddr,
      recipients=(toaddr if isinstance(toaddr, list) else [toaddr]),
      subject=subject,
      html=html,
      body=text)
    mail.send(message)
    if debug:
        current_app.logger.debug('sendmail(): message.html={}'.format(message.html))