# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_twilio_sms\serializers.py
# Compiled at: 2013-08-27 15:14:38
from __future__ import unicode_literals
from rest_framework import serializers
from .models import IncomingSMS, OutgoingSMS

class SMSRequestSerializer(serializers.ModelSerializer):
    SmsSid = serializers.CharField(max_length=34, required=True, source=b'sms_sid')
    AccountSid = serializers.CharField(max_length=34, required=True, source=b'account_sid')
    From = serializers.CharField(max_length=30, required=True, source=b'from_number')
    FromCity = serializers.CharField(max_length=30, required=False, source=b'from_city')
    FromState = serializers.CharField(max_length=30, required=False, source=b'from_state')
    FromZip = serializers.CharField(max_length=30, required=False, source=b'from_zip')
    FromCountry = serializers.CharField(max_length=120, required=False, source=b'from_country')
    To = serializers.CharField(max_length=30, required=True, source=b'to_number')
    Body = serializers.CharField(max_length=160, required=True, source=b'body')

    class Meta:
        model = IncomingSMS
        fields = [
         b'SmsSid', b'AccountSid', b'From', b'FromCity', b'FromState', b'FromZip',
         b'FromCountry', b'To', b'Body']


class SMSStatusSerializer(serializers.ModelSerializer):
    SmsSid = serializers.CharField(max_length=34, required=True, source=b'sms_sid')
    SmsStatus = serializers.CharField(max_length=30, required=True, source=b'status')

    class Meta:
        model = OutgoingSMS
        fields = [
         b'SmsSid', b'SmsStatus']