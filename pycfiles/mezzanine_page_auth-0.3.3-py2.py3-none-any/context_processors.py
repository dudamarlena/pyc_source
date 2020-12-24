# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/context_processors.py
# Compiled at: 2014-02-07 03:34:32
from __future__ import unicode_literals

def page_auth(request):
    """
    Returns context variables required for check authorizations on Mezzanine
    pages.

    If there is no 'unauthorized_pages' attribute in the request, uses empty
    list (all pages are authorized and accesible).
    """
    unauthorized_pages = []
    if hasattr(request, b'unauthorized_pages'):
        unauthorized_pages = request.unauthorized_pages
    return {b'unauthorized_pages': unauthorized_pages}