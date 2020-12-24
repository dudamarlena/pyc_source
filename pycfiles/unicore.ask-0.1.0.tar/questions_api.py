# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.ask/unicore/ask/service/questions_api.py
# Compiled at: 2015-03-13 10:41:44
from cornice.resource import resource, view
from pyramid.exceptions import NotFound
from unicore.ask.service.models import Question

def get_app_object(request):
    uuid = request.matchdict['uuid']
    question = request.db.query(Question).get(uuid)
    if question is None:
        raise NotFound
    return question


@resource(collection_path='/questions', path='/questions/{uuid}')
class QuestionResource(object):

    def __init__(self, request):
        self.request = request

    @view(renderer='json')
    def collection_post(self):
        return {}

    @view(renderer='json')
    def get(self):
        question = get_app_object(self.request)
        return question.to_dict()

    @view(renderer='json')
    def put(self):
        return {}