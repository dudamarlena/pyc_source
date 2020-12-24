# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/game_gateway.py
# Compiled at: 2013-08-19 09:08:27
from gamerocket.result.error_result import ErrorResult
from gamerocket.result.successful_result import SuccessfulResult
from gamerocket.exceptions.not_found_error import NotFoundError
from game import Game

class GameGateway(object):

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, id):
        if id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().get('/games/' + id)
        if 'game' in response:
            return SuccessfulResult({'game': Game(self.gateway, response['game'])})
        else:
            if 'error' in response:
                return ErrorResult(response)
            return