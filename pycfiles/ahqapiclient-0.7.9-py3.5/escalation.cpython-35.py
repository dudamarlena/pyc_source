# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/escalation.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1850 bytes
from ahqapiclient.resources import Resource

class Escalation(Resource):

    def __init__(self, http_client):
        super(Escalation, self).__init__('/escalations', http_client)

    def make_doc(self, name, query, cooldown_time, threshold_count, threshold_time, action=None):
        return {'name': name, 
         'query': query, 
         'cooldown_time': cooldown_time, 
         'threshold_count': threshold_count, 
         'threshold_time': threshold_time, 
         'action': action}

    def create_escalation(self, name, query, cooldown_time, threshold_count, threshold_time, action=None):
        return self.post(path=self.rurl(), data=self.make_doc(name, query, cooldown_time, threshold_count, threshold_time, action))

    def get_escalation(self, _id):
        return self.get(path=self.rurl(_id))

    def update_escalation(self, _id, name, query, cooldown_time, threshold_count, threshold_time, action=None):
        return self.put(path=self.rurl(_id), data=self.make_doc(name, query, cooldown_time, threshold_count, threshold_time, action))

    def delete_escalation(self, _id):
        return self.delete(path=self.rurl(_id))

    def get_escalations(self, limit=10, offset=0, raw=False):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset}, raw=raw)

    def total(self):
        total = self.get_escalations(limit=0, raw=True)
        try:
            return total.headers['x-total']
        except KeyError:
            return