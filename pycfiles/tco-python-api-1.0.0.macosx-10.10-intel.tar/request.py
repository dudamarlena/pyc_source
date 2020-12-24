# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/twocheckout/request.py
# Compiled at: 2015-10-07 15:00:49
import requests, json, twocheckout

class Request(object):

    @classmethod
    def call(cls, method, path, args=None):
        url = cls.build_url(path)
        headers = cls.build_headers()
        if method == 'get':
            params = args
            data = None
        else:
            params = None
            data = json.dumps(args) if args else None
        r = requests.request(method, url, headers=headers, params=params, data=data, auth=(twocheckout.seller_id, twocheckout.private_key))
        response = json.loads(r.text)
        cls.check_for_error(r.status_code, response)
        return response

    @classmethod
    def build_headers(cls):
        headers = {'Accept': 'application/json', 
           'User-Agent': '2Checkout Python/0.1.0/%s', 
           'Content-Type': 'application/json'}
        return headers

    @classmethod
    def build_url(cls, path):
        if twocheckout.sandbox:
            url = twocheckout.sandbox_base_url
        else:
            url = twocheckout.base_url
        url += path
        return str(url)

    @classmethod
    def check_for_error(cls, code, response):
        if code != 200:
            raise twocheckout.TwoCheckoutError(response['error']['code'], response['error']['message'], response['error']['param'])