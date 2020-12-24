# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beautifulpredicates/views.py
# Compiled at: 2013-01-13 00:09:48
from django.views.generic import View

class PredicateProcessView(View):
    dispatch_config = {}

    def get(self, request, *args, **kwargs):
        handler = getattr(self, 'get_default', self.http_method_not_allowed)
        for custom_receiver, predicates in self.dispatch_config:
            for predicate in predicates:
                if not predicate(request, *args, **kwargs):
                    break
            else:
                handler = getattr(self, custom_receiver)
                break

        return handler(request, *args, **kwargs)