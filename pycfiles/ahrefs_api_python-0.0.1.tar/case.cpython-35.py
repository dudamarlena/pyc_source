# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/case.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1013 bytes
from ahqapiclient.resources import Resource

class Case(Resource):

    def __init__(self, http_client):
        super(Case, self).__init__('/cases', http_client)

    def get_case(self, _id):
        return self.get(path=self.rurl(_id))

    def get_cases(self, limit=10, offset=0, query='', sort='date:desc', raw=False):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset, 
         'query': query, 
         'sort': sort}, raw=raw)

    def get_transitions(self, case_id):
        return self.get(path=self.rurl('%s/transitions' % case_id), params={})

    def trigger_transition(self, case_id, trans_id, params={}):
        return self.post(path=self.rurl('%s/transitions' % case_id), data={'id': trans_id, 
         'params': params})