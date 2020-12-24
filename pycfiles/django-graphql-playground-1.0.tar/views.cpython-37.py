# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jaydenwindle/Documents/OpenSource/django-graphql-playground/graphql_playground/views.py
# Compiled at: 2019-01-10 16:55:49
# Size of source mod 2**32: 1091 bytes
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import TemplateView

class GraphQLPlaygroundView(TemplateView):
    template_name = 'playground/playground.html'
    endpoint = None
    subscription_endpoint = None
    workspace_name = None
    config = None
    settings = None

    def __init__(self, endpoint=None, subscription_endpoint=None, workspace_name=None, config=None, settings=None, **kwargs):
        (super(GraphQLPlaygroundView, self).__init__)(**kwargs)
        self.options = {'endpoint':endpoint, 
         'subscriptionEndpoint':subscription_endpoint, 
         'workspaceName':workspace_name, 
         'config':config, 
         'settings':settings}

    def get_context_data(self, *args, **kwargs):
        context = (super(GraphQLPlaygroundView, self).get_context_data)(*args, **kwargs)
        context['options'] = json.dumps((self.options), cls=DjangoJSONEncoder)
        return context