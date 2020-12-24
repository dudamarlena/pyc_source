# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/fbrt/response.py
# Compiled at: 2014-07-25 00:56:03
from django.http import HttpResponse
import json

class JSONResponse(HttpResponse):

    def __init__(self, obj, status=200):
        super(JSONResponse, self).__init__(content=json.dumps(obj), content_type='application/json', status=status)