# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/purchase_gateway.py
# Compiled at: 2013-08-22 05:48:35
from gamerocket.result.error_result import ErrorResult
from gamerocket.result.successful_result import SuccessfulResult
from purchase import Purchase
from gamerocket.exceptions.not_found_error import NotFoundError

class PurchaseGateway(object):

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, id):
        if id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().get('/games/' + self.config.apiKey + '/purchases/' + id)
        if 'purchase' in response:
            return SuccessfulResult({'purchase': Purchase(self.gateway, response['purchase'])})
        else:
            if 'error' in response:
                return ErrorResult(response)
            return

    def buy(self, id, attributes):
        if id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().post('/games/' + self.config.apiKey + '/purchases/' + id + '/buy', attributes)
        if 'data' in response:
            return SuccessfulResult(response)
        else:
            if 'error' in response:
                return ErrorResult(response)
            return