# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/game.py
# Compiled at: 2013-08-19 09:08:34
from configuration import Configuration
from resource import Resource

class Game(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

    @staticmethod
    def find(id):
        return Configuration.gateway().game.find(id)