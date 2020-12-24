# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_handlers_light/email_handlers/sendgrid.py
# Compiled at: 2019-04-03 15:46:51
# Size of source mod 2**32: 750 bytes
from ohm2_handlers_light.definitions import EmailHandler
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

class Sendgrid(EmailHandler):

    def __init__(self, *args, **kwargs):
        self.API_KEY = kwargs.pop('key')
        super(Sendgrid, self).__init__(*args, **kwargs)

    def send(self, tries=2, delay=0.1):
        message = Mail(from_email=self.from_email, to_emails=self.to_email, subject=self.subject, html_content=self.content)
        for x in range(tries):
            try:
                sg = SendGridAPIClient(self.API_KEY)
                res = sg.send(message)
            except Exception as e:
                res = None

            if res != None and (res.status_code == 200 or res.status_code == 202):
                return True
            time.sleep(delay)