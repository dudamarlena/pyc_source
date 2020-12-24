# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/player_gateway.py
# Compiled at: 2013-08-19 09:08:03
from gamerocket.result.error_result import ErrorResult
from gamerocket.result.successful_result import SuccessfulResult
from gamerocket.exceptions.not_found_error import NotFoundError
from player import Player

class PlayerGateway(object):

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params={}):
        response = self.config.http().post('/games/' + self.config.apiKey + '/players', params)
        if 'player' in response:
            return SuccessfulResult({'player': Player(self.gateway, response['player'])})
        if 'error' in response:
            return ErrorResult(response)

    def delete(self, player_id, params={}):
        response = self.config.http().delete('/players/' + player_id, params)
        if 'status' in response:
            return SuccessfulResult(response)
        if 'error' in response:
            return ErrorResult(response)

    def find(self, player_id):
        if player_id == None or player_id.strip() == '':
            raise NotFoundError()
        response = self.config.http().get('/players/' + player_id)
        if 'player' in response:
            return SuccessfulResult({'player': Player(self.gateway, response['player'])})
        else:
            if 'error' in response:
                return ErrorResult(response)
            return

    def update(self, player_id, params={}):
        response = self.config.http().put('/players/' + player_id, params)
        if 'player' in response:
            return SuccessfulResult({'player': Player(self.gateway, response['player'])})
        if 'error' in response:
            return ErrorResult(response)