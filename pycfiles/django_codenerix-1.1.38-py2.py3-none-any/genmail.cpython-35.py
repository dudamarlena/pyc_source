# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/br0th3r/salmonete/becas.com/codenerix/lib/genmail.py
# Compiled at: 2020-01-09 08:45:20
# Size of source mod 2**32: 2985 bytes
import smtplib
from django.core import mail
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.utils import DNS_NAME

class EmailMessage(mail.EmailMessage):

    def __init__(self, *args, **kwargs):
        new_args = list(args)
        if len(args) >= 3 and args[3] is None:
            new_args[3] = [x[1] for x in settings.ADMINS]
        else:
            if 'to' in kwargs and kwargs['to'] is None:
                kwargs['to'] = [x[1] for x in settings.ADMINS]
            else:
                if settings.DEBUG and settings.CLIENTS:
                    if len(args) >= 3:
                        new_args[3] = [x[1] for x in settings.CLIENTS]
                else:
                    kwargs['to'] = [x[1] for x in settings.CLIENTS]
        super(EmailMessage, self).__init__(*new_args, **kwargs)


class SSLEmailBackend(EmailBackend):

    def __init__(self, *args, **kwargs):
        timeout = getattr(settings, 'CLIENT_EMAIL_TIMEOUT', 10)
        kwargs.setdefault('timeout', timeout)
        super(SSLEmailBackend, self).__init__(*args, **kwargs)

    def open(self):
        if self.connection:
            return False
            try:
                self.connection = smtplib.SMTP_SSL(self.host, self.port, local_hostname=DNS_NAME.get_fqdn())
                if self.username and self.password:
                    self.connection.ehlo()
                    self.connection.esmtp_features['auth'] = 'PLAIN LOGIN'
                    self.connection.login(self.username, self.password)
                return True
            except smtplib.SMTPException:
                if not self.fail_silently:
                    raise


def get_connection(host=settings.CLIENT_EMAIL_HOST, port=settings.CLIENT_EMAIL_PORT, username=settings.CLIENT_EMAIL_USERNAME, password=settings.CLIENT_EMAIL_PASSWORD, use_tls=settings.CLIENT_EMAIL_USE_TLS, use_ssl=settings.CLIENT_EMAIL_USE_SSL):
    if use_ssl:
        backend = 'codenerix.lib.genmail.SSLEmailBackend'
    else:
        backend = 'django.core.mail.backends.smtp.EmailBackend'
    return mail.get_connection(backend=backend, host=host, port=port, username=username, password=password, use_tls=use_tls)