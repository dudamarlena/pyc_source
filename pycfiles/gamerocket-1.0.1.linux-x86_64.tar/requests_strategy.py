# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/util/http_strategy/requests_strategy.py
# Compiled at: 2013-08-30 10:23:07
import requests

class RequestsStrategy(object):

    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        response = self.__request_function(http_verb)(path, headers=headers, data=request_body, verify=self.environment.ssl_certificate)
        return [
         response.status_code, response.text]

    def __request_function(self, method):
        if method == 'GET':
            return requests.get
        if method == 'POST':
            return requests.post
        if method == 'PUT':
            return requests.put
        if method == 'DELETE':
            return requests.delete