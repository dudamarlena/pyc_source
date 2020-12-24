# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/portfoliopy/portfolio/ext/mailer.py
# Compiled at: 2015-06-17 05:11:51
import warnings, ses_mailer, flask_mail
from six.moves.urllib.parse import urlparse

class Mailer(object):
    """
    A simple wrapper to switch between SES-Mailer and Flask-Mail based on config
    """
    mail = None
    provider = None
    app = None

    def init_app(self, app):
        self.app = app
        provider = app.config.get('MAILER_PROVIDER', None)
        if provider:
            self.provider = provider.upper()
            if self.provider == 'SES':

                class _App(object):
                    config = {'SES_AWS_ACCESS_KEY': app.config.get('MAILER_SES_ACCESS_KEY'), 
                       'SES_AWS_SECRET_KEY': app.config.get('MAILER_SES_SECRET_KEY'), 
                       'SES_SENDER': app.config.get('MAILER_SENDER'), 
                       'SES_REPLY_TO': app.config.get('MAILER_REPLY_TO'), 
                       'SES_TEMPLATE': app.config.get('MAILER_TEMPLATE'), 
                       'SES_TEMPLATE_CONTEXT': app.config.get('MAILER_TEMPLATE_CONTEXT')}

                _app = _App()
                self.mail = ses_mailer.Mail(app=_app)
            elif self.provider == 'SMTP':
                uri = app.config.get('MAILER_SMTP_URI', None)
                if uri is None:
                    raise ValueError("<Portfolio:Component:Mailer: MAILER_SMTP_URI is empty'")
                parse_uri = urlparse(uri)
                if 'smtp' not in parse_uri.scheme:
                    raise ValueError("<Portfolio:Component:Mailer: MAILER_SMTP_URI must start with 'smtp://'")

                class _App(object):
                    config = {'MAIL_SERVER': parse_uri.hostname, 
                       'MAIL_USERNAME': parse_uri.username, 
                       'MAIL_PASSWORD': parse_uri.password, 
                       'MAIL_PORT': parse_uri.port, 
                       'MAIL_USE_TLS': True if 'tls' in parse_uri.scheme else False, 
                       'MAIL_USE_SSL': True if 'ssl' in parse_uri.scheme else False, 
                       'MAIL_DEFAULT_SENDER': app.config.get('MAILER_SENDER'), 
                       'TESTING': app.config.get('TESTING'), 
                       'DEBUG': app.config.get('DEBUG')}
                    debug = app.config.get('DEBUG')
                    testing = app.config.get('TESTING')

                _app = _App()
                self.mail = flask_mail.Mail(app=_app)
            else:
                raise warnings.warn("<Portfolio:Component:Mailer invalid provider '%s'>" % provider)
        return

    def send(self, to, subject, body, reply_to=None, **kwargs):
        """
        Send simple message
        """
        if self.provider == 'SES':
            self.mail.send(to=to, subject=subject, body=body, reply_to=reply_to, **kwargs)
        elif self.provider == 'SMTP':
            print body
            msg = flask_mail.Message(recipients=[isinstance(to, list) or to] if 1 else to, subject=subject, body=body, reply_to=reply_to, sender=self.app.config.get('MAILER_SENDER'))
            self.mail.send(msg)

    def send_template(self, template, to, reply_to=None, **context):
        """
        Send Template message
        """
        if self.provider == 'SES':
            self.mail.send_template(template=template, to=to, reply_to=reply_to, **context)
        elif self.provider == 'SMTP':
            _template = self.app.config.get('MAILER_TEMPLATE', None)
            template_context = self.app.config.get('MAILER_TEMPLATER_CONTEXT')
            ses_mail = ses_mailer.Mail(template=_template, template_context=template_context)
            data = ses_mail.parse_template(template=template, **context)
            msg = flask_mail.Message(recipients=[isinstance(to, list) or to] if 1 else to, subject=data['subject'], body=data['body'], reply_to=reply_to, sender=self.app.config.get('MAILER_SENDER'))
            self.mail.send(msg)
        return