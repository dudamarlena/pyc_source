# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wrapper/http_wrapper.py
# Compiled at: 2019-09-09 09:27:05
# Size of source mod 2**32: 1587 bytes
from django.http import HttpResponse, JsonResponse
http_server_version = 'Apache/2.4.12'

class HttpRsp(HttpResponse):

    def __init__(self, *args, **kwargs):
        super(HttpRsp, self).__init__(*args, **kwargs)
        self['Server'] = http_server_version
        self['Cache-Control'] = 'no-store'


class JsonRsp(JsonResponse):

    def __init__(self, data={}, status=200, *args, **kwargs):
        super(JsonRsp, self).__init__(data, **kwargs)
        self.status_code = status
        if 200 != status:
            self.reason_phrase = 'ERR'
        self['Server'] = http_server_version
        self['Cache-Control'] = 'no-store'
        self['Access-Control-Allow-Origin'] = 'http://localhost:8081'
        self['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        self['Access-Control-Allow-Credentials'] = 'true'
        self['Access-Control-Allow-Headers'] = 'Content-Type,Access-Control-Allow-Credentials, Access-Control-Allow-Headers, Authorization, X-Requested-With, X-CSRF-Token,x-csrftoken'