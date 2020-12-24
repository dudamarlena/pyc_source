# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/views/home.py
# Compiled at: 2012-02-01 08:19:35
__doc__ = '\nProvides views for the root resource and the favicon of pyGallerid.\n'
import os
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from ..models import retrieve_user, retrieve_gallery, PersistentContainer