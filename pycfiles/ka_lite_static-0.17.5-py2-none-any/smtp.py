# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/mail/backends/smtp.py
# Compiled at: 2018-07-11 18:15:30
"""SMTP email backend class."""
import smtplib, ssl, threading
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.utils import DNS_NAME
from django.core.mail.message import sanitize_address
from django.utils.encoding import force_bytes

class EmailBackend(BaseEmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """

    def __init__(self, host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        if username is None:
            self.username = settings.EMAIL_HOST_USER
        else:
            self.username = username
        if password is None:
            self.password = settings.EMAIL_HOST_PASSWORD
        else:
            self.password = password
        if use_tls is None:
            self.use_tls = settings.EMAIL_USE_TLS
        else:
            self.use_tls = use_tls
        self.connection = None
        self._lock = threading.RLock()
        return

    def open(self):
        """
        Ensures we have a connection to the email server. Returns whether or
        not a new connection was required (True or False).
        """
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port, local_hostname=DNS_NAME.get_fqdn())
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise

    def close(self):
        """Closes the connection to the email server."""
        if self.connection is None:
            return
        else:
            try:
                try:
                    self.connection.quit()
                except (ssl.SSLError, smtplib.SMTPServerDisconnected):
                    self.connection.close()
                except:
                    if self.fail_silently:
                        return
                    raise

            finally:
                self.connection = None

            return

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return
        with self._lock:
            new_conn_created = self.open()
            if not self.connection:
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1

            if new_conn_created:
                self.close()
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.recipients():
            return False
        from_email = sanitize_address(email_message.from_email, email_message.encoding)
        recipients = [ sanitize_address(addr, email_message.encoding) for addr in email_message.recipients()
                     ]
        message = email_message.message()
        charset = message.get_charset().get_output_charset() if message.get_charset() else 'utf-8'
        try:
            self.connection.sendmail(from_email, recipients, force_bytes(message.as_string(), charset))
        except:
            if not self.fail_silently:
                raise
            return False

        return True