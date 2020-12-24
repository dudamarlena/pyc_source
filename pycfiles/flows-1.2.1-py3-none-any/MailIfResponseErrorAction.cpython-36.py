# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\MailIfResponseErrorAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 4026 bytes
"""
MailIfResponseErrorAction.py
-------------

Copyright 2016 Davide Mastromatteo
"""
import smtplib, urllib.parse, urllib.request
from email.mime.text import MIMEText
import time, flows.Global
from flows.Actions.Action import Action

class MailIfResponseErrorAction(Action):
    __doc__ = '\n    MailAction Class\n    send an email\n    '
    type = 'mail_if_response_error'

    def on_init(self):
        super().on_init()
        if 'smtp_server' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The smtp_server parameter is missing', self.name))
        if 'smtp_port' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The smtp_port parameter is missing', self.name))
        if 'subject' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The subject parameter is missing', self.name))
        if 'from' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The from parameter is missing', self.name))
        if 'to' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The to parameter is missing', self.name))
        if 'body' not in self.configuration:
            raise ValueError(str.format('The mail action {0} is not properly configured.The body parameter is missing', self.name))
        self.url = self.configuration['url']

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        status = ''
        try:
            response = urllib.request.urlopen(self.url)
            status = response.getcode()
        except urllib.error.HTTPError as err:
            status = err.code
        except urllib.error.URLError as err:
            status = ''

        if 'verbose' in self.configuration:
            flows.Global.LOGGER.info(str.format('{0} - {1}', self.name, status))
        if status != 200:
            input_message = str(status)
            body = self.configuration['body']
            body = body.replace('{input}', input_message)
            body = body.replace('{date}', time.strftime('%d/%m/%Y'))
            body = body.replace('{time}', time.strftime('%H:%M:%S'))
            msg = MIMEText(body)
            subject = self.configuration['subject']
            subject = subject.replace('{input}', input_message)
            subject = subject.replace('{date}', time.strftime('%d/%m/%Y'))
            subject = subject.replace('{time}', time.strftime('%H:%M:%S'))
            msg['Subject'] = subject
            msg['From'] = self.configuration['from']
            msg['To'] = self.configuration['to']
            if 'cc' in self.configuration:
                msg['Cc'] = self.configuration['cc']
            try:
                smtp_obj = smtplib.SMTP(self.configuration['smtp_server'] + ':' + self.configuration['smtp_port'])
                smtp_obj.send_message(msg)
                smtp_obj.quit()
                flows.Global.LOGGER.debug('Successfully sent email')
            except Exception as exc:
                flows.Global.LOGGER.error(str(exc))
                flows.Global.LOGGER.error('Error: unable to send email')

            self.send_message(body)