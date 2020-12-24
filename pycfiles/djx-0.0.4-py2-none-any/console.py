# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/mail/backends/console.py
# Compiled at: 2019-02-14 00:35:17
"""
Email backend that writes messages to console instead of sending them.
"""
import sys, threading
from django.core.mail.backends.base import BaseEmailBackend
from django.utils import six

class EmailBackend(BaseEmailBackend):

    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop('stream', sys.stdout)
        self._lock = threading.RLock()
        super(EmailBackend, self).__init__(*args, **kwargs)

    def write_message(self, message):
        msg = message.message()
        msg_data = msg.as_bytes()
        if six.PY3:
            charset = msg.get_charset().get_output_charset() if msg.get_charset() else 'utf-8'
            msg_data = msg_data.decode(charset)
        self.stream.write('%s\n' % msg_data)
        self.stream.write('-' * 79)
        self.stream.write('\n')

    def send_messages(self, email_messages):
        """Write all messages to the stream in a thread-safe way."""
        if not email_messages:
            return
        msg_count = 0
        with self._lock:
            try:
                stream_created = self.open()
                for message in email_messages:
                    self.write_message(message)
                    self.stream.flush()
                    msg_count += 1

                if stream_created:
                    self.close()
            except Exception:
                if not self.fail_silently:
                    raise

        return msg_count