# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/signing.py
# Compiled at: 2019-08-16 17:27:46
"""
Generic way to sign and unsign data for use in urls.
"""
from __future__ import absolute_import
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.core.signing import TimestampSigner
from sentry.utils.json import dumps, loads
SALT = 'sentry-generic-signing'

def sign(**kwargs):
    return urlsafe_b64encode(TimestampSigner(salt=SALT).sign(dumps(kwargs))).rstrip('=')


def unsign(data, max_age=172800):
    padding = len(data) % 4
    return loads(TimestampSigner(salt=SALT).unsign(urlsafe_b64decode(data + '=' * (4 - padding)), max_age=max_age))