# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_rest/views.py
# Compiled at: 2013-08-11 18:33:59
__doc__ = '\nCore module for storing common view super class.\n'
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