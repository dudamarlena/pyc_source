# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jlin/virtualenvs/django-rest-framework-queryset/lib/python3.7/site-packages/rest_framework_queryset/views.py
# Compiled at: 2018-10-01 16:04:28
# Size of source mod 2**32: 1090 bytes
from __future__ import unicode_literals
from __future__ import absolute_import

class APISearchableMixin(object):
    search_fields = []

    def __init__(self, *args, **kwargs):
        (super(APISearchableMixin, self).__init__)(*args, **kwargs)
        self._search_params = {}

    def get_context_data(self, *args, **kwargs):
        ctx = (super(APISearchableMixin, self).get_context_data)(*args, **kwargs)
        ctx['search_fields'] = self.get_search_params()
        return ctx

    def get_search_params(self):
        for field in self.search_fields:
            if self.request.method == 'POST':
                self._search_params[field] = self.request.POST.get('__search_{}'.format(field), '')
            if self.request.method == 'GET':
                self._search_params[field] = self.request.GET.get(field, '')

        return self._search_params

    def post(self, request, *args, **kwargs):
        return (self.get)(request, *args, **kwargs)