# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/transport/smtp.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 5392 bytes
"""Deliver messages using (E)SMTP."""
import socket
from smtplib import SMTP, SMTP_SSL, SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPServerDisconnected
from marrow.util.convert import boolean
from marrow.util.compat import native
from marrow.mailer.exc import TransportExhaustedException, TransportException, TransportFailedException, MessageFailedException
log = __import__('logging').getLogger(__name__)

class SMTPTransport(object):
    __doc__ = 'An (E)SMTP pipelining transport.'
    __slots__ = ('ephemeral', 'host', 'tls', 'certfile', 'keyfile', 'port', 'local_hostname',
                 'username', 'password', 'timeout', 'debug', 'pipeline', 'connection',
                 'sent')

    def __init__(self, config):
        self.host = native(config.get('host', '127.0.0.1'))
        self.tls = config.get('tls', 'optional')
        self.certfile = config.get('certfile', None)
        self.keyfile = config.get('keyfile', None)
        self.port = int(config.get('port', 465 if self.tls == 'ssl' else 25))
        self.local_hostname = native(config.get('local_hostname', '')) or None
        self.username = native(config.get('username', '')) or None
        self.password = native(config.get('password', '')) or None
        self.timeout = config.get('timeout', None)
        if self.timeout:
            self.timeout = int(self.timeout)
        self.debug = boolean(config.get('debug', False))
        self.pipeline = config.get('pipeline', None)
        if self.pipeline not in (None, True, False):
            self.pipeline = int(self.pipeline)
        self.connection = None
        self.sent = 0

    def startup(self):
        if not self.connected:
            self.connect_to_server()

    def shutdown(self):
        if self.connected:
            log.debug('Closing SMTP connection')
            try:
                try:
                    self.connection.quit()
                except SMTPServerDisconnected:
                    pass
                except (SMTPException, socket.error):
                    log.exception('Unhandled error while closing connection.')

            finally:
                self.connection = None

    def connect_to_server(self):
        if self.tls == 'ssl':
            connection = SMTP_SSL(local_hostname=(self.local_hostname), keyfile=(self.keyfile), certfile=(self.certfile),
              timeout=(self.timeout))
        else:
            connection = SMTP(local_hostname=(self.local_hostname), timeout=(self.timeout))
        log.info('Connecting to SMTP server %s:%s', self.host, self.port)
        connection.set_debuglevel(self.debug)
        connection.connect(self.host, self.port)
        connection.ehlo()
        if self.tls in ('required', 'optional', True):
            if connection.has_extn('STARTTLS'):
                connection.starttls(self.keyfile, self.certfile)
            else:
                if self.tls == 'required':
                    raise TransportException('TLS is required but not available on the server -- aborting')
        if self.username:
            if self.password:
                log.info('Authenticating as %s', self.username)
                connection.login(self.username, self.password)
        self.connection = connection
        self.sent = 0

    @property
    def connected(self):
        return getattr(self.connection, 'sock', None) is not None

    def deliver(self, message):
        if not self.connected:
            self.connect_to_server()
        try:
            self.send_with_smtp(message)
        finally:
            if not self.pipeline or self.sent >= self.pipeline:
                raise TransportExhaustedException()

    def send_with_smtp(self, message):
        try:
            sender = str(message.envelope)
            recipients = message.recipients.string_addresses
            content = str(message)
            self.connection.sendmail(sender, recipients, content)
            self.sent += 1
        except SMTPSenderRefused as e:
            try:
                log.error('%s REFUSED %s %s', message.id, e.__class__.__name__, e)
                raise MessageFailedException(str(e))
            finally:
                e = None
                del e

        except SMTPRecipientsRefused as e:
            try:
                log.warning('%s REFUSED %s %s', message.id, e.__class__.__name__, e)
                raise MessageFailedException(str(e))
            finally:
                e = None
                del e

        except SMTPServerDisconnected as e:
            try:
                if message.retries >= 0:
                    log.warning('%s DEFERRED %s', message.id, 'SMTPServerDisconnected')
                    message.retries -= 1
                raise TransportFailedException()
            finally:
                e = None
                del e

        except Exception as e:
            try:
                cls_name = e.__class__.__name__
                log.debug('%s EXCEPTION %s', (message.id), cls_name, exc_info=True)
                if message.retries >= 0:
                    log.exception('%s DEFERRED %s', message.id, cls_name)
                    message.retries -= 1
                else:
                    log.exception('%s REFUSED %s', message.id, cls_name)
                    raise TransportFailedException()
            finally:
                e = None
                del e