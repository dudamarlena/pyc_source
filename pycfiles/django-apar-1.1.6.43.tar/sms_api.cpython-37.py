# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/sms_api.py
# Compiled at: 2020-04-01 13:43:20
# Size of source mod 2**32: 1031 bytes
import abc, six
from kavenegar import *
from aparnik.settings import aparnik_settings

@six.add_metaclass(abc.ABCMeta)
class SMSAPI:

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def otp(self, receptor, otp, app_signature, first_name, last_name):
        pass


class SMSAPIKavenegar(SMSAPI):

    def otp(self, receptor, otp, app_signature, first_name, last_name):
        try:
            if not app_signature:
                app_signature = 'Code:%s' % otp
            api = KavenegarAPI(aparnik_settings.SMS_API_KEY)
            params = {'receptor':receptor, 
             'template':aparnik_settings.SMS_OTA_NAME, 
             'token':otp, 
             'token2':app_signature, 
             'type':'sms'}
            response = api.verify_lookup(params)
        except APIException as e:
            try:
                print(e)
            finally:
                e = None
                del e

        except HTTPException as e:
            try:
                print(e)
            finally:
                e = None
                del e