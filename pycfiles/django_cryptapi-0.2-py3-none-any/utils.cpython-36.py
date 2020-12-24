# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/utils.py
# Compiled at: 2020-05-04 20:03:31
# Size of source mod 2**32: 1159 bytes
import requests
from django.shortcuts import reverse
from cryptapi.config import CRYPTAPI_URL
from urllib.parse import urlencode

def build_query_string(data):
    return urlencode(data)


def build_callback_url(_r, params):
    base_url = '{scheme}://{host}'.format(scheme=(_r.scheme), host=(_r.get_host()))
    base_request = requests.Request(url=('{}{}'.format(base_url, reverse('cryptapi:callback'))),
      params=params).prepare()
    return base_request.url


def process_request(coin, endpoint='create', params=None):
    response = requests.get(url='{base_url}{coin}/{endpoint}'.format(base_url=CRYPTAPI_URL,
      coin=(coin.replace('_', '/')),
      endpoint=endpoint),
      params=params)
    return response


def get_active_providers():
    from cryptapi.models import Provider
    provider_qs = Provider.objects.filter(active=True)
    return [(p.coin, p.get_coin_display()) for p in provider_qs]


def get_order_request(order_id):
    from cryptapi.models import Request
    return Request.objects.filter(order_id=order_id)