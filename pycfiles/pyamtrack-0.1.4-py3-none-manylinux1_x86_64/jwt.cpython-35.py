# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/skin/jwt.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1649 bytes
__doc__ = 'PyAMS_security.skin.jwt module\n\nThis module provides a JWT login view.\n'
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from pyams_security.credential import Credentials
from pyams_security.interfaces import ISecurityManager
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'
from pyams_security import _

@view_config(route_name='jwt_login', renderer='json', xhr=True)
def login(request):
    """AJAX login view for JWT authentication"""
    manager = query_utility(ISecurityManager)
    if manager is None or not manager.enable_jwt_login:
        raise HTTPNotFound()
    params = request.params
    credentials = Credentials('jwt', id=params.get('login'), **params)
    principal_id = manager.authenticate(credentials, request)
    if principal_id is not None:
        return {'status': 'success', 
         'token': request.create_jwt_token(principal_id)}
    return {'status': 'error', 
     'message': request.localizer.translate(_('Invalid credentials!'))}