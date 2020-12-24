# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/Projects/DjangoProjects/basitapi/basitapi/decorators.py
# Compiled at: 2013-04-25 13:30:07
from django.core.exceptions import ObjectDoesNotExist
from basitapi.response import ApiResponse

def load_model(model, id_name, access_name):

    def decorator(func):

        def wrapped(self, request, *args, **kwargs):
            if kwargs.has_key(id_name):
                try:
                    setattr(request, access_name, model.objects.get(id=kwargs[id_name]))
                except ObjectDoesNotExist:
                    return ApiResponse.not_found()

            return func(self, request, *args, **kwargs)

        return wrapped

    return decorator