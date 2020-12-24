# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/mail/backends.py
# Compiled at: 2018-10-05 12:52:39
# Size of source mod 2**32: 265 bytes
from djangoplus.mail.utils import dump_emails
from django.core.mail.backends.base import BaseEmailBackend

class EmailDebugBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        return dump_emails(email_messages)