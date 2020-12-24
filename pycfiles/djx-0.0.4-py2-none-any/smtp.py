# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/mail/backends/smtp.py
# Compiled at: 2019-02-14 00:35:17
"""SMTP email backend class."""
import smtplib, socket, ssl, threading
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from django.core.mail.utils import DNS_NAME
from django.utils.encoding import force_str

class EmailBackend(BaseEmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """

    def __init__(self, host=None, port=None, username=None, password=None, use_tls=None, fail_silently=False, use_ssl=None, timeout=None, ssl_keyfile=None, ssl_certfile=None, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        self.username = settings.EMAIL_HOST_USER if username is None else username
        self.password = settings.EMAIL_HOST_PASSWORD if password is None else password
        self.use_tls = settings.EMAIL_USE_TLS if use_tls is None else use_tls
        self.use_ssl = settings.EMAIL_USE_SSL if use_ssl is None else use_ssl
        self.timeout = settings.EMAIL_TIMEOUT if timeout is None else timeout
        self.ssl_keyfile = settings.EMAIL_SSL_KEYFILE if ssl_keyfile is None else ssl_keyfile
        self.ssl_certfile = settings.EMAIL_SSL_CERTFILE if ssl_certfile is None else ssl_certfile
        if self.use_ssl and self.use_tls:
            raise ValueError('EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set one of those settings to True.')
        self.connection = None
        self._lock = threading.RLock()
        return

    @property
    def connection_class(self):
        if self.use_ssl:
            return smtplib.SMTP_SSL
        return smtplib.SMTP

    def open(self):
        """
        Ensure an open connection to the email server. Return whether or not a
        new connection was required (True or False) or None if an exception
        passed silently.
        """
        if self.connection:
            return False
        else:
            connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
            if self.timeout is not None:
                connection_params['timeout'] = self.timeout
            if self.use_ssl:
                connection_params.update({'keyfile': self.ssl_keyfile, 
                   'certfile': self.ssl_certfile})
            try:
                self.connection = self.connection_class(self.host, self.port, **connection_params)
                if not self.use_ssl and self.use_tls:
                    self.connection.starttls(keyfile=self.ssl_keyfile, certfile=self.ssl_certfile)
                if self.username and self.password:
                    self.connection.login(force_str(self.username), force_str(self.password))
                return True
            except (smtplib.SMTPException, socket.error):
                if not self.fail_silently:
                    raise

            return

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
                except smtplib.SMTPException:
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
        else:
            with self._lock:
                new_conn_created = self.open()
                if not self.connection or new_conn_created is None:
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
        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [ sanitize_address(addr, encoding) for addr in email_message.recipients() ]
        message = email_message.message()
        try:
            self.connection.sendmail(from_email, recipients, message.as_bytes(linesep='\r\n'))
        except smtplib.SMTPException:
            if not self.fail_silently:
                raise
            return False

        return True