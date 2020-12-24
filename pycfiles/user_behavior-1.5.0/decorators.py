# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/6z/y737zg156f53v6d096dlmv500000gn/T/pip-build-YeCYrE/user-behavior/user_behavior/decorators.py
# Compiled at: 2016-11-17 22:38:22
from __future__ import absolute_import
from functools import wraps
from datetime import date
from django.contrib.auth.models import User
from .serializers import ApiInfoSerializer
from .services import get_request_data, set_response_data

def user_behavior_extracter(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request = args[1]
        request_data = get_request_data(request)
        serializer = ApiInfoSerializer(data=request_data, partial=True)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            api_info = serializer.save(user=user)
            request.data['api_info'] = api_info
        queryset = func(*args, **kwargs)
        request.data.pop('api_info')
        api_info = set_response_data(api_info, queryset)
        return queryset

    return func_wrapper