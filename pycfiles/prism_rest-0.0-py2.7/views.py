# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_rest/views.py
# Compiled at: 2013-08-11 18:33:59
"""
Core module for storing common view super class.
"""
import logging
from prism_core.views import lift
from prism_core.views import BaseView
from prism_core.views import view_defaults
log = logging.getLogger('prism.rest.views')

@lift()
@view_defaults(renderer='prism_renderer', route_name='base_api')
class APIView(BaseView):
    """
    Super class for all API related views.
    """
    pass


@lift()
@view_defaults(route_name='base_api_auth', permission='authenticated')
class APIAuthView(APIView):
    """
    Super class for all API views that should require authentication.
    """

    def __init__(self, request):
        BaseView.__init__(self, request)
        if self.request.user:
            user = self.request.user.users[0]
            self.user = self.c.users.getById(user.id)
        else:
            self.user = None
        return