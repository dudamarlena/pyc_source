# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/question_sets.py
# Compiled at: 2015-03-04 21:31:22
QUESTION_SET_PATH = '/question_sets'

class QuestionSets:

    def __init__(self, client):
        self.client = client

    def create(self, person_id, options={}):
        body = options['body'] if 'body' in options else {}
        body['person_id'] = person_id
        response = self.client.post(QUESTION_SET_PATH, body)
        return response

    def score(self, id, answers):
        body = {}
        body['answers'] = answers
        options = {}
        options['request_type'] = 'json'
        response = self.client.post('%s/%s/score' % (QUESTION_SET_PATH, str(id)), body, options)
        return response

    def retrieve(self, id):
        body = {}
        response = self.client.get('%s/%s' % (QUESTION_SET_PATH, str(id)), body)
        return response

    def all(self, count=None, offset=None, options={}):
        body = options['body'] if 'body' in options else {}
        if count:
            body['count'] = count
        if offset:
            body['offset'] = offset
        response = self.client.get(QUESTION_SET_PATH, body)
        return response