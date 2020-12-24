# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pauloostenrijk/WebProjects/django-user-verification/verification/backends/twilio.py
# Compiled at: 2016-05-16 16:32:02
# Size of source mod 2**32: 1103 bytes
from __future__ import absolute_import
from twilio.rest.client import TwilioRestClient
from .base import BaseBackend

class TwilioBackend(BaseBackend):
    default_message = 'Welcome, click on the link to continue: {link}'

    def __init__(self, **options):
        super(TwilioBackend, self).__init__(**options)
        options = {key.lower():value for key, value in options.items()}
        if not options:
            raise ValueError('Missing sid, secret, from, for TwilioBackend')
        self._sid = options.get('sid')
        self._secret = options.get('secret')
        self._from = options.get('from')
        self._message = options.get('message', self.default_message)
        self.client = TwilioRestClient(account=self._sid, token=self._secret)

    def send(self, number, url):
        message = self._generate_message(url)
        return self.client.messages.create(to=number, body=message, from_=self._from)

    def _generate_message(self, url):
        return self._message.format(link=url)