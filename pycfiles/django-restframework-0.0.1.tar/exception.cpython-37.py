# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/django_rest_framework/django_restframework/exceptions/exception.py
# Compiled at: 2019-04-22 15:00:54
# Size of source mod 2**32: 1515 bytes
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        try:
            response.data['success'] = False
            response.data['msg'] = response.data['detail']
            del response.data['detail']
        except:
            pass

    return response


class myException401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED


class myException400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class myException403(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class myException404(APIException):
    status_code = status.HTTP_404_NOT_FOUND


class myException500(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class myException412(APIException):
    status_code = status.HTTP_412_PRECONDITION_FAILED


class myException415(APIException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class myException422(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY