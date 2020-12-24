# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/views/basic/activate.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = 'Registration related views.'
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPRedirection
from pyramid.security import NO_PERMISSION_REQUIRED
from sqlalchemy.orm.exc import NoResultFound
import pyramid_basemodel
from pyramid_fullauth.views import BaseView
from pyramid_fullauth.models import User
from pyramid_fullauth.events import AfterActivate

@view_config(route_name='register:activate', permission=NO_PERMISSION_REQUIRED, renderer='pyramid_fullauth:resources/templates/activate.mako')
class ActivateView(BaseView):
    """Activate account views."""

    def __call__(self):
        """Process account activation."""
        activate_hash = self.request.matchdict.get('hash')
        user = None
        response = {}
        response['status'] = True
        if activate_hash:
            try:
                user = pyramid_basemodel.Session.query(User).filter(User.activate_key == activate_hash).one()
                if not user.is_active:
                    user.is_active = True
            except NoResultFound:
                response['status'] = False

        try:
            self.request.registry.notify(AfterActivate(self.request, user))
        except HTTPRedirection as e:
            return e

        return response