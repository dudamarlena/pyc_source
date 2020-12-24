# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/action.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1833 bytes
from ahqapiclient.resources import Resource

class Action(Resource):

    def __init__(self, http_client):
        super(Action, self).__init__('/actions', http_client)

    def make_doc(self, name, endpoint_id, path, method, success_code, payload=[]):
        return {'name': name, 
         'endpoint': endpoint_id, 
         'path': path, 
         'method': method, 
         'success_code': success_code, 
         'payload': payload}

    def create_action(self, name, endpoint_id, path, method, success_code, payload=[]):
        return self.post(path=self.rurl(), data=self.make_doc(name, endpoint_id, path, method, success_code, payload))

    def get_action(self, _id):
        return self.get(path=self.rurl(_id))

    def update_action(self, _id, name, endpoint_id, path, method, success_code, payload=[]):
        return self.put(path=self.rurl(_id), data=self.make_doc(name, endpoint_id, path, method, success_code, payload))

    def delete_action(self, _id):
        return self.delete(path=self.rurl(_id))

    def get_actions(self, limit=10, offset=0, raw=False):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset}, raw=raw)

    def execute_action(self, _id, params):
        return self.post(path=self.rurl('%s/execute' % _id), data=params)

    def total(self):
        total = self.get_actions(limit=0, raw=True)
        try:
            return total.headers['x-total']
        except KeyError:
            return