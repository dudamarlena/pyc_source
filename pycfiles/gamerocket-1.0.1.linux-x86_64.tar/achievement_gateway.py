# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/achievement_gateway.py
# Compiled at: 2013-08-19 09:09:40
from gamerocket.result.error_result import ErrorResult
from gamerocket.result.successful_result import SuccessfulResult
from gamerocket.exceptions.not_found_error import NotFoundError
from achievement import Achievement

class AchievementGateway(object):

    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, player_id, id, attributes):
        if player_id == None or player_id.strip() == '' or id == None or id.strip() == '':
            raise NotFoundError()
        response = self.config.http().get('/players/' + player_id + 'achievements/' + id, attributes)
        if 'achievement' in response:
            return SuccessfulResult({'achievement': Achievement(self.gateway, response['achievement'])})
        else:
            if 'error' in response:
                return ErrorResult(response)
            return