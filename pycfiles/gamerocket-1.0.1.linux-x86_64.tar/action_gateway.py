# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/action_gateway.py
# Compiled at: 2013-08-22 08:14:43
from gamerocket.result.error_result import ErrorResult
from gamerocket.result.successful_result import SuccessfulResult
from gamerocket.exceptions.not_found_error import NotFoundError
from action import Action

class ActionGateway(object):

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, id):
        if id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().get('/games/' + self.config.apiKey + '/actions/' + id)
        if 'action' in response:
            return SuccessfulResult({'action': Action(self.gateway, response['action'])})
        else:
            if 'error' in response:
                return ErrorResult(response)
            return

    def run(self, id, attributes):
        if id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().post('/games/' + self.config.apiKey + '/actions/' + id + '/run', attributes)
        if 'data' in response:
            return SuccessfulResult(response)
        else:
            if 'error' in response:
                return ErrorResult(response)
            return