# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/verification.py
# Compiled at: 2014-07-16 22:22:42


class Verification:

    def __init__(self, client):
        self.client = client

    def create(self, date_of_birth, identification, name, address, options={}):
        body = options['body'] if 'body' in options else {}
        body['date_of_birth'] = date_of_birth
        body['identification'] = identification
        body['name'] = name
        body['address'] = address
        response = self.client.post('/verifications', body, options)
        return response

    def retrieve(self, id, options={}):
        body = options['query'] if 'query' in options else {}
        response = self.client.get('/verifications/' + str(id), body, options)
        return response

    def all(self, count=None, offset=None, options={}):
        body = options['query'] if 'query' in options else {}
        if count != None:
            body['count'] = count
        if offset != None:
            body['offset'] = offset
        response = self.client.get('/verifications', body, options)
        return response