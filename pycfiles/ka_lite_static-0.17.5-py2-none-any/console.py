# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/mail/backends/console.py
# Compiled at: 2018-07-11 18:15:30
"""
Email backend that writes messages to console instead of sending them.
"""
import sys, threading
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):

    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop('stream', sys.stdout)
        self._lock = threading.RLock()
        super(EmailBackend, self).__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        """Write all messages to the stream in a thread-safe way."""
        if not email_messages:
            return
        with self._lock:
            try:
                stream_created = self.open()
                for message in email_messages:
                    self.stream.write('%s\n' % message.message().as_string())
                    self.stream.write('-' * 79)
                    self.stream.write('\n')
                    self.stream.flush()

                if stream_created:
                    self.close()
            except:
                if not self.fail_silently:
                    raise

        return len(email_messages)