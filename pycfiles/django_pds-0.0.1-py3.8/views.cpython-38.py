# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/django_pds/core/rest/views.py
# Compiled at: 2020-05-07 10:24:10
# Size of source mod 2**32: 217 bytes
from rest_framework.views import APIView
from .exceptions import method_not_allowed

class BaseAPIView(APIView):

    def http_method_not_allowed(self, request, *args, **kwargs):
        return method_not_allowed()