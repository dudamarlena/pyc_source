# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/core/http/methods.py
# Compiled at: 2019-05-11 01:30:13
# Size of source mod 2**32: 422 bytes


class HttpMethod(object):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    PATCH = 'PATCH'
    methods = [
     POST,
     GET,
     PUT,
     DELETE,
     HEAD,
     CONNECT,
     OPTIONS,
     TRACE,
     PATCH]