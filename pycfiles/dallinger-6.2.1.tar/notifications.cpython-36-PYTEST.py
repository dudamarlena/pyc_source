# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Dallinger/Dallinger/dallinger/notifications.py
# Compiled at: 2020-04-26 19:37:24
# Size of source mod 2**32: 5205 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, six, smtplib
from cached_property import cached_property
from email.mime.text import MIMEText
logger = logging.getLogger(__file__)
CONFIG_PLACEHOLDER = '???'

class InvalidEmailConfig(ValueError):
    __doc__ = 'The configuration contained missing or invalid email-related values.\n    '


class SMTPMailer(object):

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self._sent = []

    @cached_property
    def server(self):
        return get_email_server(self.host)

    def send(self, subject, sender, recipients, body):
        msg = self._make_email(subject, sender, recipients, body)
        try:
            self.server.starttls()
            self.server.login(self.username, self.password)
            self.server.sendmail(sender, recipients, msg.as_string())
            self.server.quit()
        except smtplib.SMTPException as ex:
            six.raise_from(MessengerError('SMTP error sending HIT error email.'), ex)
        except Exception as ex:
            six.raise_from(MessengerError('Unknown error sending HIT error email.'), ex)

        self._sent.append(msg)

    def _make_email(self, subject, sender, recipients, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = ','.join(recipients)
        msg['From'] = sender
        return msg


class LoggingMailer(object):

    def __init__(self):
        self._sent = []

    def send(self, subject, sender, recipients, body):
        msg = '{}:\nSubject: {}\nSender: {}\nRecipients: {}\nBody:\n{}'.format(self.__class__.__name__, subject, sender, ', '.join(recipients), body)
        logger.info(msg)
        self._sent.append(msg)


def get_mailer(config, strict=False):
    """Return an appropriate Messenger.

    If we're in debug mode, or email settings aren't set, return a debug
    version which logs the message instead of attempting to send a real
    email.
    """
    settings = EmailConfig(config)
    if config.get('mode') == 'debug':
        return LoggingMailer()
    else:
        problems = settings.validate()
        if problems:
            if strict:
                raise InvalidEmailConfig(problems)
            logger.info(problems + ' Will log errors instead of emailing them.')
            return LoggingMailer()
        return SMTPMailer(settings.smtp_host, settings.smtp_username, settings.smtp_password)


def get_email_server(host):
    """Return an SMTP server using the specified host.

    Abandon attempts to connect after 8 seconds.
    """
    return smtplib.SMTP(host, timeout=8)


class MessengerError(Exception):
    __doc__ = 'A message could not be relayed.'


class EmailConfig(object):
    __doc__ = 'Extracts and validates email-related values from a Configuration\n    '
    mail_config_keys = {
     'smtp_host',
     'smtp_username',
     'smtp_password',
     'contact_email_on_error',
     'dallinger_email_address'}

    def __init__(self, config):
        self.smtp_host = config.get('smtp_host')
        self.smtp_username = config.get('smtp_username', None)
        self.contact_email_on_error = config.get('contact_email_on_error')
        self.smtp_password = config.get('smtp_password', None)
        self.dallinger_email_address = config.get('dallinger_email_address')

    def as_dict(self):
        cleaned = self.__dict__.copy()
        password = self.smtp_password
        if password:
            if password != CONFIG_PLACEHOLDER:
                cleaned['smtp_password'] = password[:3] + '......' + password[(-1)]
        return cleaned

    def validate(self):
        """Could this config be used to send a real email?"""
        missing = []
        for k in self.mail_config_keys:
            attr = getattr(self, k, False)
            if not attr or attr == CONFIG_PLACEHOLDER:
                missing.append(k)

        if missing:
            return 'Missing or invalid config values: {}'.format(', '.join(sorted(missing)))


class NotifiesAdmin(object):
    __doc__ = 'Quickly email the experiment admin/author with to/from addresses\n    taken from configuration.\n    '

    def __init__(self, email_settings, mailer):
        self.fromaddr = email_settings.dallinger_email_address
        self.toaddr = email_settings.contact_email_on_error
        self.mailer = mailer

    def send(self, subject, body):
        self.mailer.send(subject, self.fromaddr, [self.toaddr], body)


def admin_notifier(config):
    """Return an appropriate NotifiesAdmin implementation.

    If we're in debug mode, or email settings aren't set, return a debug
    version which logs the message instead of attempting to send a real
    email.
    """
    settings = EmailConfig(config)
    if config.get('mode') == 'debug':
        return NotifiesAdmin(settings, LoggingMailer())
    else:
        problems = settings.validate()
        if problems:
            logger.info(problems + ' Will log errors instead of emailing them.')
            return NotifiesAdmin(settings, LoggingMailer())
        return NotifiesAdmin(settings, SMTPMailer(settings.smtp_host, settings.smtp_username, settings.smtp_password))