# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/postonly.py
# Compiled at: 2008-03-07 17:28:21
from ZPublisher.HTTPRequest import HTTPRequest
from zExceptions import Forbidden

def check(request):
    if isinstance(request, HTTPRequest):
        if request.get('REQUEST_METHOD', 'GET').upper() != 'POST':
            raise Forbidden('Request must be POST')