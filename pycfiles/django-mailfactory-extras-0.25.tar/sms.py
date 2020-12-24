# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sms/twilio/sms.py
# Compiled at: 2014-08-01 07:08:10
from django.conf import settings
from ..base import BaseSMS
from twilio.rest import TwilioRestClient

class TwilioSMS(BaseSMS):

    def send(self, to_phone, from_phone=None):
        from_phone = from_phone or settings.TWILIO_PHONE_SERVER
        message = self.create_sms_msg()
        client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        response = client.messages.create(to=to_phone, from_=from_phone, body=message)
        return response