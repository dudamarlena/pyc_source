# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/people.py
# Compiled at: 2015-03-04 21:31:22
PEOPLE_PATH = '/people'

class People:

    def __init__(self, client):
        self.client = client

    def create(self, options={}):
        response = self.client.post(PEOPLE_PATH, options)
        return response

    def retrieve(self, id, options={}):
        body = options['query'] if 'query' in options else {}
        response = self.client.get('%s/%s' % (PEOPLE_PATH, str(id)), body)
        return response

    def all(self, count=None, offset=None, options={}):
        body = options['body'] if 'body' in options else {}
        if count != None:
            body['count'] = count
        if offset != None:
            body['offset'] = offset
        response = self.client.get(PEOPLE_PATH, body)
        return response