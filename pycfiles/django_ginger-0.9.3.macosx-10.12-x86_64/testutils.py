# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/testutils.py
# Compiled at: 2014-10-30 01:17:27
import json
from django import test
from django.contrib.auth.models import AnonymousUser
__all__ = [
 'TestRequestMixin']

class TestRequestMixin(object):

    def request(self, method='GET', path='/', session=None, user=None, data=None, **kwargs):
        factory = test.RequestFactory()
        if data is not None and kwargs.get('content_type', 'application/json'):
            data = json.dumps(data)
        kwargs['data'] = data
        request = getattr(factory, method.lower())(path, **kwargs)
        request.session = {} if session is None else session
        request.user = user or AnonymousUser()
        return request