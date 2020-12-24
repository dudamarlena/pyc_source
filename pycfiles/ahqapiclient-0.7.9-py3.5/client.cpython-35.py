# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/client.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1280 bytes
from ahqapiclient.resources import Resource

class Client(Resource):

    def __init__(self, http_client):
        super(Client, self).__init__('/clients', http_client)

    def create_client(self, client):
        return self.post(path=self.rurl(), data=client)

    def update_client(self, _id, client):
        return self.put(path=self.rurl(_id), data=client)

    def get_clients(self, limit=10, offset=0, query=''):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset, 
         'query': query})

    def get_client(self, _id):
        return self.get(path=self.rurl(_id))

    def handle(self, _id, cooldown, period, action=None, comment=None, incident_id=None):
        return self.post(path=self.rurl('%s/handle' % _id), data={'cooldown': cooldown, 
         'period': period, 
         'action': action, 
         'comment': comment, 
         'incident_id': incident_id})

    def get_client_infections(self, _id):
        return self.get(path=self.rurl('%s/infections' % _id))