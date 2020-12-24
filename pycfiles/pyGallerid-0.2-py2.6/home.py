# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/views/home.py
# Compiled at: 2012-02-01 08:19:35
"""
Provides views for the root resource and the favicon of pyGallerid.
"""
import os
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from ..models import retrieve_user, retrieve_gallery, PersistentContainer