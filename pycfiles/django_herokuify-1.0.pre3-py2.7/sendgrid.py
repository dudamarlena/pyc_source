# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\herokuify\mail\sendgrid.py
# Compiled at: 2013-01-22 21:14:34
from __future__ import unicode_literals
import os
__all__ = [
 b'SENDGRID_SMTP_SERVER', b'SENDGRID_USERNAME', b'SENDGRID_PASSWORD',
 b'SENDGRID_SMTP_PORT',
 b'EMAIL_HOST', b'EMAIL_HOST_USER', b'EMAIL_HOST_PASSWORD', b'EMAIL_PORT',
 b'EMAIL_USE_TLS']
SENDGRID_SMTP_SERVER = b'smtp.sendgrid.net'
SENDGRID_USERNAME = os.environ.get(b'SENDGRID_USERNAME')
SENDGRID_PASSWORD = os.environ.get(b'SENDGRID_PASSWORD')
SENDGRID_SMTP_PORT = 587
EMAIL_HOST = SENDGRID_SMTP_SERVER
EMAIL_HOST_USER = SENDGRID_USERNAME
EMAIL_HOST_PASSWORD = SENDGRID_PASSWORD
EMAIL_PORT = SENDGRID_SMTP_PORT
EMAIL_USE_TLS = True