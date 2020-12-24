# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\herokuify\mail\mailgun.py
# Compiled at: 2012-10-24 18:45:29
from __future__ import unicode_literals
import os
__all__ = [
 b'MAILGUN_API_KEY', b'MAILGUN_SMTP_SERVER', b'MAILGUN_SMTP_LOGIN',
 b'MAILGUN_SMTP_PASSWORD', b'MAILGUN_SMTP_PORT',
 b'EMAIL_HOST', b'EMAIL_HOST_USER', b'EMAIL_HOST_PASSWORD', b'EMAIL_PORT']
MAILGUN_API_KEY = os.environ.get(b'MAILGUN_API_KEY')
MAILGUN_SMTP_SERVER = os.environ.get(b'MAILGUN_SMTP_SERVER')
MAILGUN_SMTP_LOGIN = os.environ.get(b'MAILGUN_SMTP_LOGIN')
MAILGUN_SMTP_PASSWORD = os.environ.get(b'MAILGUN_SMTP_PASSWORD')
MAILGUN_SMTP_PORT = int(os.environ.get(b'MAILGUN_SMTP_PORT', 0)) or None
EMAIL_HOST = MAILGUN_SMTP_SERVER
EMAIL_HOST_USER = MAILGUN_SMTP_LOGIN
EMAIL_HOST_PASSWORD = MAILGUN_SMTP_PASSWORD
EMAIL_PORT = MAILGUN_SMTP_PORT