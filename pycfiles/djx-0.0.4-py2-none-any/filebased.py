# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/mail/backends/filebased.py
# Compiled at: 2019-02-14 00:35:17
"""Email backend that writes messages to a file."""
import datetime, os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.utils import six

class EmailBackend(ConsoleEmailBackend):

    def __init__(self, *args, **kwargs):
        self._fname = None
        if 'file_path' in kwargs:
            self.file_path = kwargs.pop('file_path')
        else:
            self.file_path = getattr(settings, 'EMAIL_FILE_PATH', None)
        if not isinstance(self.file_path, six.string_types):
            raise ImproperlyConfigured('Path for saving emails is invalid: %r' % self.file_path)
        self.file_path = os.path.abspath(self.file_path)
        if os.path.exists(self.file_path) and not os.path.isdir(self.file_path):
            raise ImproperlyConfigured('Path for saving email messages exists, but is not a directory: %s' % self.file_path)
        elif not os.path.exists(self.file_path):
            try:
                os.makedirs(self.file_path)
            except OSError as err:
                raise ImproperlyConfigured('Could not create directory for saving email messages: %s (%s)' % (self.file_path, err))

        if not os.access(self.file_path, os.W_OK):
            raise ImproperlyConfigured('Could not write to directory: %s' % self.file_path)
        kwargs['stream'] = None
        super(EmailBackend, self).__init__(*args, **kwargs)
        return

    def write_message(self, message):
        self.stream.write(message.message().as_bytes() + '\n')
        self.stream.write('-' * 79)
        self.stream.write('\n')

    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            fname = '%s-%s.log' % (timestamp, abs(id(self)))
            self._fname = os.path.join(self.file_path, fname)
        return self._fname

    def open(self):
        if self.stream is None:
            self.stream = open(self._get_filename(), 'ab')
            return True
        else:
            return False

    def close(self):
        try:
            if self.stream is not None:
                self.stream.close()
        finally:
            self.stream = None

        return