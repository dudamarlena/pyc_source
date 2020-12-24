# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/endpoint.py
# Compiled at: 2016-10-17 07:52:17
# Size of source mod 2**32: 1748 bytes
from ahqapiclient.resources import Resource

class Endpoint(Resource):

    def __init__(self, http_client):
        super(Endpoint, self).__init__('/endpoints', http_client)

    def make_doc(self, name, url, auth_method, auth_options, content_type):
        doc = {'name': name, 
         'url': url, 
         'auth_method': auth_method, 
         'auth_options': auth_options}
        if content_type is not None:
            doc['content_type'] = content_type
        return doc

    def create_endpoint(self, name, url, auth_method, auth_options, content_type='JSON'):
        return self.post(path=self.rurl(), data=self.make_doc(name, url, auth_method, auth_options, content_type))

    def get_endpoint(self, _id):
        return self.get(path=self.rurl(_id))

    def update_endpoint(self, _id, name, url, auth_method, auth_options, content_type='JSON'):
        return self.put(path=self.rurl(_id), data=self.make_doc(name, url, auth_method, auth_options, content_type))

    def delete_endpoint(self, _id):
        return self.delete(path=self.rurl(_id))

    def get_endpoints(self, limit=10, offset=0, query='', raw=False):
        return self.get(path=self.rurl(), params={'limit': limit, 
         'offset': offset, 
         'query': query}, raw=raw)

    def total(self):
        total = self.get_endpoints(limit=0, raw=True)
        try:
            return total.headers['x-total']
        except KeyError:
            return