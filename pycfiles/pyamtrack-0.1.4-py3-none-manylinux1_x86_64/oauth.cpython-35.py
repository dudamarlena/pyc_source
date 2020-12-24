# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/skin/oauth.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 3433 bytes
__doc__ = 'PyAMS_security.skin.oauth module\n\nThis module provides a login view for OAuth authentication.\nPlease note that this login method requires additional components provided by PyAMS_security_skin\npackage.\n'
from logging import WARNING
from authomatic import Authomatic
from authomatic.adapters import WebObAdapter
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.security import remember
from pyramid.view import view_config
from pyams_security.interfaces import AuthenticatedPrincipalEvent, IOAuthLoginConfiguration, ISecurityManager, LOGIN_REFERER_KEY
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

@view_config(route_name='oauth_login')
def login(request):
    """Login view for Authomatic authentication"""
    manager = query_utility(ISecurityManager)
    if manager is None or not manager.enable_oauth_login:
        raise HTTPNotFound()
    session = request.session
    if LOGIN_REFERER_KEY not in session:
        session[LOGIN_REFERER_KEY] = request.referer
    provider_name = request.matchdict.get('provider_name')
    configuration = IOAuthLoginConfiguration(manager).get_oauth_configuration()
    authomatic = Authomatic(config=configuration, secret=manager.authomatic_secret, logging_level=WARNING)
    response = Response()
    result = authomatic.login(WebObAdapter(request, response), provider_name)
    if result:
        if result.error:
            pass
    else:
        if result.user:
            if not (result.user.id and result.user.name):
                result.user.update()
            oauth_folder = manager.get(manager.oauth_users_folder)
            user_id = '{provider_name}.{user_id}'.format(provider_name=provider_name, user_id=result.user.id)
            request.registry.notify(AuthenticatedPrincipalEvent(plugin='oauth', principal_id=user_id, provider_name=provider_name, user=result.user))
            principal_id = '{prefix}:{user_id}'.format(prefix=oauth_folder.prefix, user_id=user_id)
            headers = remember(request, principal_id)
            response.headerlist.extend(headers)
        if manager.oauth_login_use_popup:
            response.text = result.popup_html()
        response.status_code = 302
        if LOGIN_REFERER_KEY in session:
            response.location = session[LOGIN_REFERER_KEY]
            del session[LOGIN_REFERER_KEY]
        else:
            response.location = '/'
    return response