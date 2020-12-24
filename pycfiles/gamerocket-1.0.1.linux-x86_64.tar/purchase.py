# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/purchase.py
# Compiled at: 2013-08-19 09:06:53
from configuration import Configuration
from resource import Resource

class Purchase(Resource):

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

    @staticmethod
    def find(id):
        return Configuration.gateway().purchase.find(id)

    @staticmethod
    def buy(id, attributes):
        return Configuration.gateway().purchase.buy(id, attributes)