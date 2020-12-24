# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\ProgramData\Anaconda3\lib\site-packages\steemconnect_auth\auth\steemconnect.py
# Compiled at: 2019-05-20 22:15:48
# Size of source mod 2**32: 977 bytes
from django.contrib.auth import get_user_model
from django.http import Http404
import requests

class SteemConnectBackend:
    steem_api_url = 'https://api.steemjs.com/lookup_account_names?accountNames=%5B%22{}%22%5D'

    def authenticate(self, request, username=None, password=None):
        username = username.lower()
        if requests.get(self.steem_api_url.format(username)).text == '[null]':
            raise Http404
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username=username)
        if password is not None:
            if user.is_superuser:
                if user_model(username=username).check_password(password):
                    return user
                return
        return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return