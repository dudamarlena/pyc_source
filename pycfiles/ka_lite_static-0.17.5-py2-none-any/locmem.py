# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/mail/backends/locmem.py
# Compiled at: 2018-07-11 18:15:30
"""
Backend for test environment.
"""
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    """A email backend for use during test sessions.

    The test connection stores email messages in a dummy outbox,
    rather than sending them out on the wire.

    The dummy outbox is accessible through the outbox instance attribute.
    """

    def __init__(self, *args, **kwargs):
        super(EmailBackend, self).__init__(*args, **kwargs)
        if not hasattr(mail, 'outbox'):
            mail.outbox = []

    def send_messages(self, messages):
        """Redirect messages to the dummy outbox"""
        for message in messages:
            message.message()

        mail.outbox.extend(messages)
        return len(messages)