# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_decoy/views.py
# Compiled at: 2014-12-20 15:40:48
__doc__ = "pyramid_decoy's views definitions."
from pyramid.httpexceptions import HTTPFound

def decoy(request):
    """
    Redirect to given page with 302 HTTP status code.

    :param pyramid.request.Request request: pyramid's request.

    :returns: HTTPFound response
    :rtype: pyramid.httpexceptions.HTTPFound
    """
    decoy_url = request.registry['decoy']['url']
    return HTTPFound(location=decoy_url)