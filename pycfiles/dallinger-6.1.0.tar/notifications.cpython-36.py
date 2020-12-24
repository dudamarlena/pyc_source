# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/notifications.py
# Compiled at: 2020-04-15 14:09:48
# Size of source mod 2**32: 3480 bytes
import logging, six, smtplib
from cached_property import cached_property
from email.mime.text import MIMEText
logger = logging.getLogger(__file__)
CONFIG_PLACEHOLDER = '???'

def get_email_server(host):
    """Return an SMTP server using the specified host.

    Abandon attempts to connect after 8 seconds.
    """
    return smtplib.SMTP(host, timeout=8)


class MessengerError(Exception):
    __doc__ = 'A message could not be relayed.'


class EmailConfig(object):
    __doc__ = 'Extracts and validates email-related values from a Configuration\n    '
    _map = {'username':'smtp_username', 
     'toaddr':'contact_email_on_error', 
     'fromaddr':'dallinger_email_address', 
     'password':'smtp_password'}

    def __init__(self, config):
        self.host = config.get('smtp_host')
        self.username = config.get('smtp_username', None)
        self.toaddr = config.get('contact_email_on_error')
        self.password = config.get('smtp_password', None)
        self.fromaddr = config.get('dallinger_email_address')

    def validate(self):
        """Could this config be used to send a real email?"""
        missing = []
        for k, v in self._map.items():
            attr = getattr(self, k, False)
            if not attr or attr == CONFIG_PLACEHOLDER:
                missing.append(v)

        if missing:
            return 'Missing or invalid config values: {}'.format(', '.join(sorted(missing)))


class BaseMessenger(object):

    def __init__(self, email_settings):
        self.host = email_settings.host
        self.username = email_settings.username
        self.fromaddr = email_settings.fromaddr
        self.toaddr = email_settings.toaddr
        self.password = email_settings.password


class EmailingMessenger(BaseMessenger):
    __doc__ = 'Actually sends an email message to the experiment owner.\n    '

    @cached_property
    def server(self):
        return get_email_server(self.host)

    def send(self, message):
        msg = MIMEText(message['body'])
        msg['Subject'] = message['subject']
        try:
            self.server.starttls()
            self.server.login(self.username, self.password)
            self.server.sendmail(self.fromaddr, self.toaddr, msg.as_string())
            self.server.quit()
        except smtplib.SMTPException as ex:
            six.raise_from(MessengerError('SMTP error sending HIT error email.'), ex)
        except Exception as ex:
            six.raise_from(MessengerError('Unknown error sending HIT error email.'), ex)


class DebugMessenger(BaseMessenger):
    __doc__ = 'Used in debug mode.\n\n    Prints the message contents to the log instead of sending an email.\n    '

    def send(self, message):
        logger.info('{}:\n{}\n{}'.format(self.__class__.__name__, message['subject'], message['body']))


def get_messenger(config):
    """Return an appropriate Messenger.

    If we're in debug mode, or email settings aren't set, return a debug
    version which logs the message instead of attempting to send a real
    email.
    """
    email_settings = EmailConfig(config)
    if config.get('mode') == 'debug':
        return DebugMessenger(email_settings)
    else:
        problems = email_settings.validate()
        if problems:
            logger.info(problems + ' Will log errors instead of emailing them.')
            return DebugMessenger(email_settings)
        return EmailingMessenger(email_settings)