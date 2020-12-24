# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_decoy/views.py
# Compiled at: 2014-12-20 15:40:48
"""pyramid_decoy's views definitions."""
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