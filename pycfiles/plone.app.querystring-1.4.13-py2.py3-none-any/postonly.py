# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/app/protect/postonly.py
# Compiled at: 2008-03-07 17:28:21
from ZPublisher.HTTPRequest import HTTPRequest
from zExceptions import Forbidden

def check(request):
    if isinstance(request, HTTPRequest):
        if request.get('REQUEST_METHOD', 'GET').upper() != 'POST':
            raise Forbidden('Request must be POST')