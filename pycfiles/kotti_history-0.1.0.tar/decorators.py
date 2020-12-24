# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_history/kotti_history/decorators.py
# Compiled at: 2017-01-06 10:20:39
from pyramid import httpexceptions as httpexc

def login_required(wrapped):

    def wrapper(context, request):
        if request.user is not None:
            response = wrapped(context, request)
        else:
            raise httpexc.HTTPForbidden()
        return response

    return wrapper