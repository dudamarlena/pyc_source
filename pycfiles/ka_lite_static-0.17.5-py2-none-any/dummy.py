# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/mail/backends/dummy.py
# Compiled at: 2018-07-11 18:15:30
"""
Dummy email backend that does nothing.
"""
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        return len(email_messages)