# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/exception_handler.py
# Compiled at: 2019-10-27 19:02:52
# Size of source mod 2**32: 533 bytes
from rest_framework.views import exception_handler
from rest_framework import serializers
from django.core.exceptions import ValidationError

def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        exc = serializers.ValidationError(exc.message_dict)
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        return response