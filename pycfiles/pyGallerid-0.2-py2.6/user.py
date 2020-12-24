# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/views/user.py
# Compiled at: 2012-01-23 03:50:32
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from ..models import retrieve_gallery
from ..models.user import User

@view_config(context=User)
def user(context, request):
    gallery = retrieve_gallery(context)
    if gallery is not None:
        return HTTPFound(location=request.resource_url(gallery))
    else:
        return HTTPNotFound()
        return