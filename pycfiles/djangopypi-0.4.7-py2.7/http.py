# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/djangopypi/http.py
# Compiled at: 2015-10-27 08:49:00
from django.http import HttpResponse, QueryDict
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.datastructures import MultiValueDict
from django.contrib.auth import authenticate

class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

    def __init__(self, realm):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % realm


def login_basic_auth(request):
    authentication = request.META.get('HTTP_AUTHORIZATION')
    if not authentication:
        return
    authmeth, auth = authentication.split(' ', 1)
    if authmeth.lower() != 'basic':
        return
    auth = auth.strip().decode('base64')
    username, password = auth.split(':', 1)
    return authenticate(username=username, password=password)