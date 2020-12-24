# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/views/basic/logout.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'De-authentication related view.'
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid_fullauth.views import BaseView

@view_config(route_name='logout', permission=NO_PERMISSION_REQUIRED)
class LogoutView(BaseView):
    """Logout view."""

    def __call__(self):
        """Logout action."""
        location = '/'
        if self.config.redirects.logout:
            location = self.request.route_path(self.config.redirects.logout)
        self.request.logout()
        return HTTPSeeOther(location=location, headers=self.request.response.headers)