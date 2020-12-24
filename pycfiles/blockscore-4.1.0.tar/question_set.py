# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johnbackus/Dropbox/coding/blockscore/blockscore-python/blockscore/api/question_set.py
# Compiled at: 2014-09-08 20:10:56
import json

class QuestionSet:

    def __init__(self, client):
        self.client = client

    def create(self, verification_id, options={}):
        body = options['body'] if 'body' in options else {}
        body['verification_id'] = verification_id
        body['time_limit'] = 300
        response = self.client.post('/questions', body, options)
        return response

    def score(self, verification_id, question_set_id, answers, options={}):
        body = options['body'] if 'body' in options else {}
        options['request_type'] = 'json'
        body = {'verification_id': verification_id, 
           'question_set_id': question_set_id, 
           'answers': answers}
        response = self.client.post('/questions/score', body, options)
        return response