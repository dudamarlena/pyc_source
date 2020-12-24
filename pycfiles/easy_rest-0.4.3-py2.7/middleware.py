# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/middleware.py
# Compiled at: 2015-05-27 17:59:31
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from easyapi.errors import BadRequestError
__author__ = 'michaelturilin'

class HttpErrorsMiddleware(object):
    """
    This class returns the following HTTP message codes:
    - Bad Request (400) for ValueError and descendants.
    - Not Found (404) for Django's ObjectDoesNotExists
    """

    def process_exception(self, request, exception):
        if isinstance(exception, (ValueError, BadRequestError)):
            return HttpResponse(exception, status=HTTP_400_BAD_REQUEST)
        if isinstance(exception, (ObjectDoesNotExist,)):
            return HttpResponse(exception, status=HTTP_404_NOT_FOUND)
        if isinstance(exception, (MultipleObjectsReturned,)):
            return HttpResponse(exception, status=HTTP_409_CONFLICT)