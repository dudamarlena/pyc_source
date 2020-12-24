# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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