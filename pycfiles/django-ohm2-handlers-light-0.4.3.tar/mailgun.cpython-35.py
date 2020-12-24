# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_handlers_light/email_handlers/mailgun.py
# Compiled at: 2019-04-03 14:49:45
# Size of source mod 2**32: 972 bytes
from ohm2_handlers_light.definitions import EmailHandler
import requests, time

class Mailgun(EmailHandler):

    def __init__(self, *args, **kwargs):
        self.MAILGUN_DOMAIN_NAME = kwargs.pop('domain')
        self.MAILGUN_API_KEY = kwargs.pop('key')
        super(Mailgun, self).__init__(*args, **kwargs)
        self.auth = (
         'api', self.MAILGUN_API_KEY)
        address = kwargs.get('address', None)
        if address:
            self.address = address
        else:
            self.address = 'https://api.mailgun.net/v3/' + self.MAILGUN_DOMAIN_NAME + '/messages'

    def send(self, tries=2, delay=0.1):
        data = {'from': self.from_email, 
         'to': self.to_email, 
         'subject': self.subject, 
         'html': self.content}
        for x in range(tries):
            try:
                res = requests.post(self.address, auth=self.auth, data=data)
            except Exception as e:
                res = None

            if res != None and res.status_code == 200:
                r = res.json()
                return True
            time.sleep(delay)

        return False