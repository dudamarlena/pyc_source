# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/views/basic/forbidden.py
# Compiled at: 2017-02-24 16:57:38
"""Forbidden views."""
from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid_fullauth.views import BaseView

class ForbiddenViews(BaseView):
    """Forbidden related views."""

    def __init__(self, request):
        """Set all responses status to 403 by default."""
        super(ForbiddenViews, self).__init__(request)
        self.request.response.status_code = 403

    @forbidden_view_config(renderer='pyramid_fullauth:resources/templates/403.mako')
    def forbidden(self):
        """Forbidden page view."""
        if self.request.authenticated_userid:
            return {}
        loc = self.request.route_path('login', _query=(('after', self.request.path),))
        return HTTPFound(location=loc)

    @forbidden_view_config(xhr=True, renderer='json')
    def forbidden_json(self):
        """Forbidden xhr response."""
        if self.request.authenticated_userid:
            return {'status': False, 'msg': self.request._('forbidden-notallowed', default='You are not allowed to use this function', domain='pyramid_fullauth')}
        return {'status': False, 'msg': self.request._('forbidden-login', default='You have to be logged in to use this function', domain='pyramid_fullauth'), 
           'login_url': self.request.route_path('login')}