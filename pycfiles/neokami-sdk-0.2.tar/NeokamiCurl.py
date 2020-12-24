# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neokami1/Dropbox/Neokami/Code/Bitbucket/neokami-python-sdk/neokami/src/Neokami/HttpClients/NeokamiCurl.py
# Compiled at: 2015-09-08 04:46:19
""" Copyright 2015 Neokami GmbH. """
import requests

class NeokamiHttpClient:

    def get(self, route, payload):
        r = requests.get(route, params=payload)
        return r

    def post(self, route, api_key, payload):
        headers = {'apikey': api_key}
        r = requests.post(route, data=payload, headers=headers)
        return r

    def postBinary(self, route, bytestream, api_key, params={}):
        """
        :param route:
        :param bytestream:
        :param api_key:
        :param params:
        :return:
        """
        headers = {'apikey': api_key}
        files = {'data': bytestream}
        r = requests.post(url=route, data=params, files=files, headers=headers)
        return r